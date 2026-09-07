#!/usr/bin/env python3
"""Provider-neutral image execution guard. It never generates or visually judges images.

The host calls init/event/next with real executor and reviewer receipts. Every image
call must be reserved before dispatch. One ledger is retained for the whole run.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Callable, Protocol

MAX_ATTEMPTS = 3
STAGES = {"route", "anchor", "group", "individual", "validation"}
ISSUES = {"execution", "identity_drift", "design", "spec_conflict"}


class GuardError(ValueError):
    """The proposed event is unsafe or incomplete; do not dispatch a tool call."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GuardError(message)


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def check_task(task: dict) -> None:
    require(task.get("stage") in STAGES, "Unknown stage")
    require(bool(task.get("id")) and bool(task.get("subject")), "Stable task id and subject required")
    require(isinstance(task.get("prompt"), str) and bool(task["prompt"].strip()), "Minimal prompt required")
    checks = task.get("requirements", [])
    require(bool(checks), "Explicit acceptance requirements required")
    ids = [c.get("id") for c in checks]
    require(all(ids) and len(ids) == len(set(ids)), "Requirement ids must be unique")
    require(all(isinstance(c.get("text"), str) and c["text"].strip() for c in checks), "Empty requirement")
    for key in ("identity_locked", "requires_user_approval"):
        require(type(task.get(key)) is bool, f"Explicit {key} required")
    require(isinstance(task.get("references"), list), "references must be a list")
    require(isinstance(task.get("dependencies"), dict), "dependencies must map task ids to output revisions")
    refs = task["references"]
    require(len({r["id"] for r in refs}) == len(refs), "Duplicate reference id")
    roles = {r.get("role") for r in refs}
    needed = {"group": {"identity"}, "individual": {"identity", "group", "position_map"}}
    require(needed.get(task["stage"], set()) <= roles, "Missing stage-specific visual references")
    for ref in refs:
        require(ref.get("role") in {"identity", "group", "position_map", "user_reference", "validation"}, "Invalid reference role")
        if ref.get("source_task"):
            require(task["dependencies"].get(ref["source_task"]) == ref.get("source_revision"), "Reference/dependency revision mismatch")
        if ref.get("role") == "identity":
            require(ref.get("approved") is True and bool(ref.get("approval_ref")), "Identity reference needs recorded user approval")
    if task["stage"] == "individual":
        groups = [r for r in refs if r["role"] == "group"]
        require(len(groups) == 1 and bool(groups[0].get("source_task")), "Individual needs one versioned accepted group")
        maps = [r for r in refs if r["role"] == "position_map"]
        require(len(maps) == 1 and maps[0].get("source_task") == groups[0]["source_task"], "Map must depend on the same group")
    if task["stage"] == "route":
        require(not task["dependencies"], "Exploration routes cannot inherit sibling outputs")
        require(roles <= {"user_reference"}, "Exploration accepts user references, not sibling candidates")
        require(all(not r.get("source_task") and r.get("origin") == "user_supplied" for r in refs), "Route references must originate from the user")
        require(task["requires_user_approval"], "Route selection requires the user")


def initialize(plan: dict) -> dict:
    require(bool(plan.get("run_id")), "run_id required")
    tasks = plan.get("tasks", [])
    require(bool(tasks), "Plan must contain tasks")
    jobs = {}
    subjects = set()
    for task in tasks:
        check_task(task)
        key = (task["stage"], task["subject"])
        require(task["id"] not in jobs and key not in subjects, "Duplicate logical work item")
        subjects.add(key)
        jobs[task["id"]] = {"task": copy.deepcopy(task), "status": "ready", "attempts": [], "revision": 0, "output": None}
    for key, job in jobs.items():
        deps = job["task"]["dependencies"]
        require(key not in deps and set(deps) <= set(jobs), "Missing or self dependency")
    def visit(key: str, chain: set) -> None:
        require(key not in chain, "Dependency cycle")
        for dep in jobs[key]["task"]["dependencies"]:
            visit(dep, chain | {key})
    for key in jobs:
        visit(key, set())
    return {"version": 1, "run_id": plan["run_id"], "plan_hash": digest(plan), "jobs": jobs, "contexts": [], "events": []}


def asset(root: Path, record: dict, image: bool = True) -> dict:
    path = (root / record["path"]).resolve()
    require(path.is_relative_to(root.resolve()) and path.is_file(), "Missing asset or path outside run root")
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    require(record.get("sha256") == sha, "Asset hash mismatch")
    if image:
        header = data.startswith((b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff")) or (data[:4] == b"RIFF" and data[8:12] == b"WEBP")
        require(header, "Expected PNG/JPEG/WebP bytes, not a filename placeholder")
    return copy.deepcopy(record)


def dependencies_ok(state: dict, job: dict) -> bool:
    return all(state["jobs"][key]["status"] == "accepted" and state["jobs"][key]["revision"] == revision
               for key, revision in job["task"]["dependencies"].items())


def references(root: Path, state: dict, job: dict) -> list[dict]:
    require(dependencies_ok(state, job), "Upstream is unapproved, failed or stale")
    refs = job["task"]["references"]
    for ref in refs:
        asset(root, ref, image=ref["role"] != "position_map")
        if ref.get("source_task") and ref["role"] != "position_map":
            require(ref["sha256"] == state["jobs"][ref["source_task"]]["output"]["sha256"], "Reference is not the accepted source output")
        if ref["role"] == "position_map":
            mapping = json.loads((root / ref["path"]).read_text(encoding="utf-8"))
            groups = [r for r in refs if r["role"] == "group"]
            require(len(groups) == 1 and mapping.get("group_sha256") == groups[0]["sha256"], "Position map belongs to another group image")
            require(mapping.get("inspected") is True and bool(mapping.get("positions")), "Actual inspected position map required")
            require(job["task"]["subject"] in mapping["positions"], "Variant missing from actual position map")
    return refs


def context(state: dict, receipt: dict, hashes: list[str]) -> None:
    require(receipt.get("isolated") is True and receipt.get("inherits_parent_conversation") is False, "True isolated execution is required; prompt-only clearing is insufficient")
    require(bool(receipt.get("runtime_receipt")), "Host runtime receipt required")
    key = receipt.get("id")
    require(bool(key) and key not in state["contexts"], "Executor/reviewer context reused")
    require(receipt.get("image_hashes") == hashes, "Actual image bindings/order do not match the task pack")
    state["contexts"].append(key)


def invalidate(state: dict, task_id: str) -> None:
    affected = {task_id}
    while True:
        more = {k for k, j in state["jobs"].items() if set(j["task"]["dependencies"]) & affected}
        if more <= affected:
            break
        affected |= more
    for key in affected:
        state["jobs"][key]["status"] = "stale"


def next_action(state: dict, task_id: str) -> dict:
    job = state["jobs"][task_id]
    status = job["status"]
    if status in {"ready", "retry"}:
        if not dependencies_ok(state, job):
            return {"action": "blocked_upstream", "remaining": MAX_ATTEMPTS - len(job["attempts"])}
        if len(job["attempts"]) >= MAX_ATTEMPTS:
            return {"action": "exhausted", "remaining": 0}
        return {"action": job.get("retry_action", "generate"), "remaining": MAX_ATTEMPTS - len(job["attempts"])}
    return {"action": status, "remaining": MAX_ATTEMPTS - len(job["attempts"])}


def apply_event(original: dict, event: dict, root: Path) -> dict:
    """Transactional reducer: errors never partly modify the caller's state."""
    state = copy.deepcopy(original)
    if event.get("type") == "extend_plan":
        require(bool(event.get("user_approval_ref")), "New stage requires recorded authorization")
        new_tasks = event.get("tasks", [])
        require(bool(new_tasks), "No tasks to add")
        combined = [j["task"] for j in state["jobs"].values()] + new_tasks
        validated = initialize({"run_id": state["run_id"], "tasks": combined})
        for new in new_tasks:
            state["jobs"][new["id"]] = validated["jobs"][new["id"]]
        state["events"].append(copy.deepcopy(event))
        return state
    if event.get("type") == "route_batch_review":
        routes = {k: j for k, j in state["jobs"].items() if j["task"]["stage"] == "route"}
        require(len(routes) >= 2, "Batch comparison needs multiple route images")
        require(all(j["status"] in {"awaiting_user_approval", "accepted"} for j in routes.values()), "All routes must have reviewed outputs")
        keys = sorted(routes)
        outputs = [asset(root, routes[k]["output"]) for k in keys]
        context(state, event["context"], [o["sha256"] for o in outputs])
        expected = {(a, b) for n, a in enumerate(keys) for b in keys[n + 1:]}
        pairs = event.get("pairs", [])
        require(len(pairs) == len(expected) and {tuple(sorted((p["a"], p["b"]))) for p in pairs} == expected, "Compare every route pair")
        allowed = {"silhouette", "proportion", "face_grammar", "material", "emotional_posture", "series_mechanism"}
        passed = True
        for pair in pairs:
            differences = pair.get("different_dimensions", [])
            require(len(set(differences)) == len(differences) and set(differences) <= allowed and bool(pair.get("observation")), "Observed high-weight differences required")
            passed = passed and len(differences) >= 3
        snapshot = {k: {"revision": routes[k]["revision"], "sha256": routes[k]["output"]["sha256"]} for k in keys}
        state["route_batch"] = {"passed": passed, "snapshot": snapshot, "review": copy.deepcopy(event)}
        if not passed:
            retry_ids = event.get("rework_ids", [])
            require(bool(retry_ids) and set(retry_ids) <= set(keys), "Identify the routes to re-explore")
            require(bool(event.get("repair_note")), "Specify the missing structural diversity")
            failing = [{p["a"], p["b"]} for p in pairs if len(p["different_dimensions"]) < 3]
            require(all(pair & set(retry_ids) for pair in failing), "Rework must cover every failing pair")
            for key in retry_ids:
                job = routes[key]
                require(job["status"] != "accepted" and not job["task"]["identity_locked"], "Do not redesign approved identities without user authorization")
                job["retry_action"] = "redesign"
                job["batch_correction"] = event["repair_note"]
                job["status"] = "retry" if len(job["attempts"]) < MAX_ATTEMPTS else "exhausted"
        state["events"].append(copy.deepcopy(event))
        return state
    key = event.get("task_id")
    require(key in state["jobs"], "Task must be in the frozen run plan; renaming cannot reset budget")
    job = state["jobs"][key]
    task = job["task"]
    kind = event.get("type")
    if kind == "reserve":
        action = next_action(state, key)["action"]
        require(action in {"generate", "patch", "rerender", "redesign"}, f"Cannot dispatch: {action}")
        refs = references(root, state, job)
        bound = [r["sha256"] for r in refs if r["role"] != "position_map"]
        if action == "patch":
            failed = job["attempts"][-1]["output"]
            asset(root, failed)
            bound.append(failed["sha256"])
        context(state, event["context"], bound)
        request_packet = generation_packet(state, key, root)
        job["attempts"].append({"number": len(job["attempts"]) + 1, "action": action, "context": event["context"], "references": copy.deepcopy(refs), "contract_hash": digest(task), "packet": request_packet})
        job["status"] = "running"  # Persist this reservation BEFORE calling image generation.
        job.pop("batch_correction", None)
    elif kind == "output":
        require(job["status"] == "running", "No reserved image attempt")
        output = asset(root, event["output"])
        historical = [a["output"] for j in state["jobs"].values() for a in j["attempts"] if "output" in a]
        require(all(old["path"] != output["path"] or old["sha256"] == output["sha256"] for old in historical), "Do not overwrite an earlier attempt; use immutable versioned files")
        job["attempts"][-1]["output"] = output
        job["status"] = "awaiting_review"
    elif kind == "error":
        require(job["status"] == "running", "No running attempt")
        require(event.get("reason") in {"tool_error", "safety", "interrupted"}, "Unknown execution error")
        job["attempts"][-1]["error"] = event
        job["retry_action"] = "rerender"
        job["status"] = "blocked_safety" if event["reason"] == "safety" else ("retry" if len(job["attempts"]) < MAX_ATTEMPTS else "exhausted")
    elif kind == "review":
        require(job["status"] == "awaiting_review", "Review requires an actual output")
        refs = references(root, state, job)
        output = job["attempts"][-1]["output"]
        asset(root, output)
        context(state, event["context"], [output["sha256"]] + [r["sha256"] for r in refs if r["role"] != "position_map"])
        checks = event.get("checks", {})
        require(set(checks) == {r["id"] for r in task["requirements"]}, "Every requirement must be rechecked, not only the repaired region")
        require(all(c.get("status") in {"pass", "fail", "unknown"} and isinstance(c.get("observation"), str) and bool(c["observation"].strip()) for c in checks.values()), "Evidence observations required")
        job["attempts"][-1]["review"] = event
        if all(c["status"] == "pass" for c in checks.values()):
            job["output"] = output
            job["revision"] += 1
            job["status"] = "awaiting_user_approval" if task["requires_user_approval"] else "accepted"
        else:
            issue = event.get("issue")
            require(issue in ISSUES, "Classify the deviation before retrying")
            require(isinstance(event.get("repair_note"), str) and bool(event["repair_note"].strip()), "Short specific correction required")
            if issue == "spec_conflict":
                job["status"] = "blocked_spec"
            elif issue == "design" and task["identity_locked"]:
                job["status"] = "awaiting_design_approval"
            else:
                job["retry_action"] = {"execution": "patch", "identity_drift": "rerender", "design": "redesign"}[issue]
                job["status"] = "retry" if len(job["attempts"]) < MAX_ATTEMPTS else "exhausted"
    elif kind == "approve":
        require(job["status"] == "awaiting_user_approval" and bool(event.get("user_approval_ref")), "Only a QC-passed result can be approved; record the real user decision")
        if task["stage"] == "route":
            batch = state.get("route_batch", {})
            routes = {k: j for k, j in state["jobs"].items() if j["task"]["stage"] == "route"}
            require(batch.get("passed") is True and set(batch.get("snapshot", {})) == set(routes), "Route selection needs a passed visual batch review")
            require(all(j["status"] in {"awaiting_user_approval", "accepted"} and batch["snapshot"][k] == {"revision": j["revision"], "sha256": j["output"]["sha256"]} for k, j in routes.items()), "Route comparison is stale")
        job["status"] = "accepted"
        job["approval"] = event["user_approval_ref"]
    elif kind == "invalidate":
        require(bool(event.get("reason")), "Record why the source is obsolete")
        invalidate(state, key)
    elif kind == "refresh":
        require(job["status"] in {"stale", "blocked_spec", "awaiting_design_approval"}, "Refresh only invalid/paused work")
        require(bool(event.get("user_approval_ref")), "Explicit revision authorization required")
        revised = event["task"]
        check_task(revised)
        require(all(revised[k] == task[k] for k in ("id", "stage", "subject")), "Do not rename work to reset budget")
        require(set(revised["dependencies"]) == set(task["dependencies"]), "Dependency graph is frozen")
        invalidate(state, key)
        job["task"] = copy.deepcopy(revised)
        job["status"] = "ready" if len(job["attempts"]) < MAX_ATTEMPTS else "exhausted"
        job.pop("retry_action", None)
        job.pop("batch_correction", None)
        job["revision_authorization"] = event["user_approval_ref"]
    else:
        raise GuardError("Unknown event type")
    state["events"].append(copy.deepcopy(event))
    return state


def generation_packet(state: dict, task_id: str, root: Path) -> dict:
    """Only current approved inputs and the latest short correction, never history."""
    job = state["jobs"][task_id]
    refs = references(root, state, job)
    mode = next_action(state, task_id)["action"]
    note = job.get("batch_correction") if mode != "generate" else None
    images = [copy.deepcopy(r) for r in refs if r["role"] != "position_map"]
    if job["attempts"] and mode != "generate":
        note = note or job["attempts"][-1].get("review", {}).get("repair_note")
    if mode == "patch":
        images.append(dict(job["attempts"][-1]["output"], role="failed_output"))
    return {"task_id": task_id, "mode": mode, "prompt": job["task"]["prompt"],
            "requirements": copy.deepcopy(job["task"]["requirements"]),
            "images": images, "supporting_files": [r for r in refs if r["role"] == "position_map"],
            "correction": note}


def review_packet(state: dict, task_id: str, root: Path) -> dict:
    job = state["jobs"][task_id]
    require(job["status"] == "awaiting_review", "No image awaiting review")
    refs = references(root, state, job)
    return {"task_id": task_id, "requirements": copy.deepcopy(job["task"]["requirements"]),
            "images": [copy.deepcopy(job["attempts"][-1]["output"])] + [r for r in refs if r["role"] != "position_map"],
            "supporting_files": [r for r in refs if r["role"] == "position_map"]}


class Host(Protocol):
    """Adapter implemented by a runtime with real isolated image/vision workers.

    This repository deliberately ships no pretend implementation of that runtime.
    Receipt ids and image bindings must come from actual dispatch, not model claims.
    """
    def fresh_context(self, role: str, image_hashes: list[str]) -> dict: ...
    def generate(self, packet: dict, receipt: dict) -> dict: ...
    def review(self, packet: dict, receipt: dict) -> dict: ...


def run_task(state: dict, task_id: str, root: Path, host: Host,
             persist: Callable[[dict], None]) -> dict:
    """Run bounded generation/review/retry; stop at every human or upstream gate.

    generate returns {output: {path, sha256}} or {error: tool_error|safety}.
    review returns checks/issue/repair_note. Exceptions leave a durable reservation
    (or an unreviewed image) for reconciliation, never an unrecorded extra retry.
    A production host must serialize the entire run and retain the same ledger.
    """
    while True:
        action = next_action(state, task_id)["action"]
        if action in {"generate", "patch", "rerender", "redesign"}:
            packet = generation_packet(state, task_id, root)
            receipt = host.fresh_context("generate", [r["sha256"] for r in packet["images"]])
            state = apply_event(state, {"type": "reserve", "task_id": task_id, "context": receipt}, root)
            persist(state)  # Reservation must be durable before a potentially costly call.
            result = host.generate(packet, receipt)
            event = ({"type": "error", "reason": result["error"]} if "error" in result
                     else {"type": "output", "output": result["output"]})
            state = apply_event(state, dict(event, task_id=task_id), root)
            persist(state)
        elif action == "awaiting_review":
            packet = review_packet(state, task_id, root)
            receipt = host.fresh_context("review", [r["sha256"] for r in packet["images"]])
            result = host.review(packet, receipt)
            state = apply_event(state, dict(result, type="review", task_id=task_id, context=receipt), root)
            persist(state)
        else:
            return state


def save_atomic(path: Path, value: dict) -> None:
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["init", "event", "next"])
    parser.add_argument("ledger", type=Path)
    parser.add_argument("input", help="Plan/event JSON file, or task id for next")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    lock = args.ledger.with_name(args.ledger.name + ".lock")
    held = False
    try:
        lock.mkdir()  # Serialize writers; never silently delete another writer's lock.
        held = True
        if args.command == "init":
            require(not args.ledger.exists(), "Ledger already exists; cannot reset attempts")
            state = initialize(json.loads(Path(args.input).read_text(encoding="utf-8")))
            save_atomic(args.ledger, state)
            result = {"run_id": state["run_id"], "tasks": list(state["jobs"])}
        else:
            state = json.loads(args.ledger.read_text(encoding="utf-8"))
            if args.command == "event":
                event = json.loads(Path(args.input).read_text(encoding="utf-8"))
                state = apply_event(state, event, args.root)
                save_atomic(args.ledger, state)
                result = next_action(state, event["task_id"]) if "task_id" in event else {"tasks": list(state["jobs"]), "route_batch_passed": state.get("route_batch", {}).get("passed")}
            else:
                result = next_action(state, args.input)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (GuardError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    finally:
        if held:
            lock.rmdir()


if __name__ == "__main__":
    raise SystemExit(main())
