"""Synthetic contract/state tests. Tiny PNG fixtures are NOT image-generation evidence."""
import base64
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import execution_guard as g

PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jA1sAAAAASUVORK5CYII=")


def task(key="A", **kwargs):
    value = dict(id=key, stage="anchor", subject=key, prompt="Keep the approved symmetric eye rule.",
                 requirements=[{"id": "eyes", "text": "Both eyes follow the same approved grammar."},
                               {"id": "hands", "text": "No unintended limb duplication."}],
                 references=[], dependencies={}, identity_locked=False, requires_user_approval=False)
    value.update(kwargs)
    return value


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.output = self.file("figure.png", PNG)
        self.seq = 0

    def file(self, name, data):
        (self.root / name).write_bytes(data)
        return {"path": name, "sha256": hashlib.sha256(data).hexdigest()}

    def state(self, *tasks):
        return g.initialize({"run_id": "unit-fixture", "tasks": list(tasks) or [task()]})

    def ctx(self, hashes=None):
        self.seq += 1
        return dict(id=f"fixture-context-{self.seq}", isolated=True, inherits_parent_conversation=False,
                    runtime_receipt=f"mock-dispatch-{self.seq}", image_hashes=hashes or [])

    def event(self, s, kind, key="A", **data):
        return g.apply_event(s, dict(type=kind, task_id=key, **data), self.root)

    def generated(self, s, key="A"):
        packet = g.generation_packet(s, key, self.root)
        s = self.event(s, "reserve", key, context=self.ctx([r["sha256"] for r in packet["images"]]))
        return self.event(s, "output", key, output=self.output)

    def review(self, s, key="A", passed=True, issue="execution"):
        packet = g.review_packet(s, key, self.root)
        checks = {r["id"]: {"status": "pass" if passed else "fail", "observation": "Synthetic test observation, not a visual finding."}
                  for r in s["jobs"][key]["task"]["requirements"]}
        return self.event(s, "review", key, context=self.ctx([r["sha256"] for r in packet["images"]]),
                          checks=checks, issue=issue, repair_note="Fix only the required eye alignment.")

    def host(self, passed):
        outer = self
        class FakeHost:
            calls = 0
            def fresh_context(self, role, image_hashes):
                return outer.ctx(image_hashes)
            def generate(self, packet, receipt):
                self.calls += 1
                return {"output": outer.output}
            def review(self, packet, receipt):
                ok = passed(self.calls)
                return {"checks": {r["id"]: {"status": "pass" if ok else "fail", "observation": "Mock observation."} for r in packet["requirements"]},
                        "issue": "execution", "repair_note": "Fix eye alignment; preserve other approved details."}
        return FakeHost()

    def test_bounded_loop_retries_and_succeeds(self):
        host = self.host(lambda n: n == 2)
        saved = []
        s = g.run_task(self.state(), "A", self.root, host, lambda s: saved.append(copy.deepcopy(s)))
        self.assertEqual(host.calls, 2)
        self.assertEqual(s["jobs"]["A"]["status"], "accepted")
        self.assertEqual(saved[0]["jobs"]["A"]["status"], "running")
        self.assertEqual(len(s["contexts"]), 4)

    def test_exactly_three_calls_share_patch_rerender_budget(self):
        s = self.state()
        for issue in ("execution", "identity_drift", "execution"):
            s = self.review(self.generated(s), passed=False, issue=issue)
        self.assertEqual(g.next_action(s, "A")["action"], "exhausted")
        with self.assertRaises(g.GuardError):
            self.event(s, "reserve", context=self.ctx())
        self.assertEqual(len(s["jobs"]["A"]["attempts"]), 3)

    def test_automatic_loop_never_calls_fourth_time(self):
        host = self.host(lambda _: False)
        s = g.run_task(self.state(), "A", self.root, host, lambda _: None)
        self.assertEqual(host.calls, 3)
        self.assertEqual(s["jobs"]["A"]["status"], "exhausted")

    def test_unclean_context_is_blocked_before_count(self):
        s = self.state()
        ctx = self.ctx()
        ctx["inherits_parent_conversation"] = True
        with self.assertRaises(g.GuardError):
            self.event(s, "reserve", context=ctx)
        self.assertFalse(s["jobs"]["A"]["attempts"])

    def test_missing_runtime_receipt_is_rejected(self):
        ctx = self.ctx()
        ctx["runtime_receipt"] = ""
        with self.assertRaises(g.GuardError):
            self.event(self.state(), "reserve", context=ctx)

    def test_reviewer_cannot_reuse_generator_context(self):
        s = self.generated(self.state())
        ctx = dict(s["jobs"]["A"]["attempts"][0]["context"], image_hashes=[self.output["sha256"]])
        with self.assertRaises(g.GuardError):
            self.event(s, "review", context=ctx, checks={})

    def test_reviewer_must_bind_actual_output(self):
        s = self.generated(self.state())
        with self.assertRaises(g.GuardError):
            self.event(s, "review", context=self.ctx(), checks={})

    def test_partial_recheck_cannot_pass(self):
        s = self.generated(self.state())
        with self.assertRaises(g.GuardError):
            self.event(s, "review", context=self.ctx([self.output["sha256"]]),
                       checks={"eyes": {"status": "pass", "observation": "Fixed"}})

    def test_unknown_is_not_pass(self):
        s = self.generated(self.state())
        checks = {r["id"]: {"status": "unknown", "observation": "Occluded"} for r in s["jobs"]["A"]["task"]["requirements"]}
        s = self.event(s, "review", context=self.ctx([self.output["sha256"]]), checks=checks,
                       issue="identity_drift", repair_note="Show unobscured identity.")
        self.assertEqual(s["jobs"]["A"]["status"], "retry")

    def test_failed_image_cannot_be_user_approved(self):
        s = self.review(self.generated(self.state()), passed=False)
        with self.assertRaises(g.GuardError):
            self.event(s, "approve", user_approval_ref="user-turn")

    def test_locked_design_change_waits_for_user(self):
        s = self.review(self.generated(self.state(task(identity_locked=True))), passed=False, issue="design")
        self.assertEqual(g.next_action(s, "A")["action"], "awaiting_design_approval")

    def test_unlocked_design_can_reexplore(self):
        s = self.review(self.generated(self.state()), passed=False, issue="design")
        self.assertEqual(g.next_action(s, "A")["action"], "redesign")

    def test_spec_conflict_stops_instead_of_overriding_user(self):
        s = self.review(self.generated(self.state()), passed=False, issue="spec_conflict")
        self.assertEqual(g.next_action(s, "A")["action"], "blocked_spec")

    def test_user_selection_is_not_replaced_by_qc_pass(self):
        s = self.review(self.generated(self.state(task(requires_user_approval=True))))
        self.assertEqual(s["jobs"]["A"]["status"], "awaiting_user_approval")
        s = self.event(s, "approve", user_approval_ref="actual-user-turn-required-in-production")
        self.assertEqual(s["jobs"]["A"]["status"], "accepted")

    def test_safety_rejection_does_not_retry(self):
        s = self.event(self.state(), "reserve", context=self.ctx())
        s = self.event(s, "error", reason="safety")
        self.assertEqual(g.next_action(s, "A")["action"], "blocked_safety")
        self.assertEqual(len(s["jobs"]["A"]["attempts"]), 1)

    def test_tool_error_consumes_reserved_attempt(self):
        s = self.event(self.state(), "reserve", context=self.ctx())
        s = self.event(s, "error", reason="tool_error")
        self.assertEqual(g.next_action(s, "A"), {"action": "rerender", "remaining": 2})

    def test_crash_preserves_reservation_and_prevents_blind_retry(self):
        host = self.host(lambda _: True)
        def crash(*_):
            raise RuntimeError("simulated transport ambiguity")
        host.generate = crash
        saved = []
        with self.assertRaises(RuntimeError):
            g.run_task(self.state(), "A", self.root, host, lambda s: saved.append(copy.deepcopy(s)))
        self.assertEqual(g.next_action(saved[-1], "A")["action"], "running")
        self.assertEqual(len(saved[-1]["jobs"]["A"]["attempts"]), 1)

    def test_output_requires_reservation(self):
        with self.assertRaises(g.GuardError):
            self.event(self.state(), "output", output=self.output)

    def test_fake_filename_is_not_reference(self):
        bad = dict(self.output, path="absent.png", id="input", role="user_reference", origin="user_supplied")
        s = self.state(task(references=[bad]))
        with self.assertRaises(g.GuardError):
            self.event(s, "reserve", context=self.ctx([bad["sha256"]]))

    def test_hash_change_is_detected(self):
        ref = dict(self.output, id="input", role="user_reference")
        s = self.state(task(references=[ref]))
        (self.root / "figure.png").write_bytes(PNG + b"new version")
        with self.assertRaises(g.GuardError):
            self.event(s, "reserve", context=self.ctx([ref["sha256"]]))

    def test_text_disguised_as_png_is_rejected(self):
        bad = self.file("fake.png", b"not an image")
        s = self.event(self.state(), "reserve", context=self.ctx())
        with self.assertRaises(g.GuardError):
            self.event(s, "output", output=bad)

    def test_path_escape_is_rejected(self):
        with self.assertRaises(g.GuardError):
            g.asset(self.root, dict(path="../outside.png", sha256="fake"))

    def test_route_cannot_inherit_another_candidate(self):
        with self.assertRaises(g.GuardError):
            self.state(task("R1", stage="route", requires_user_approval=True, dependencies={"R2": 1}),
                       task("R2", stage="route", requires_user_approval=True))

    def test_route_cannot_bind_identity_as_sibling_reference(self):
        ref = dict(self.output, id="sibling", role="identity", approved=True, approval_ref="fixture")
        with self.assertRaises(g.GuardError):
            self.state(task("R1", stage="route", requires_user_approval=True, references=[ref]))

    def test_missing_group_and_position_map_rejected(self):
        with self.assertRaises(g.GuardError):
            self.state(task(stage="individual"))

    def test_duplicate_logical_task_rejected(self):
        with self.assertRaises(g.GuardError):
            self.state(task("A", subject="same"), task("B", subject="same"))

    def test_new_name_cannot_create_fresh_budget(self):
        with self.assertRaises(g.GuardError):
            self.event(self.state(), "reserve", "A-renamed", context=self.ctx())

    def test_dependency_cycle_rejected(self):
        with self.assertRaises(g.GuardError):
            self.state(task("A", dependencies={"B": 1}), task("B", dependencies={"A": 1}))

    def test_stale_propagates_transitively(self):
        s = self.state(task("A"), task("B", dependencies={"A": 1}), task("C", dependencies={"B": 1}))
        s = self.event(s, "invalidate", reason="Approved source superseded")
        self.assertEqual({j["status"] for j in s["jobs"].values()}, {"stale"})

    def test_unaccepted_upstream_blocks_generation(self):
        s = self.state(task("A"), task("B", dependencies={"A": 1}))
        self.assertEqual(g.next_action(s, "B")["action"], "blocked_upstream")
        with self.assertRaises(g.GuardError):
            self.event(s, "reserve", "B", context=self.ctx())

    def test_refresh_does_not_reset_three_attempts(self):
        s = self.state()
        for _ in range(3):
            s = self.review(self.generated(s), passed=False)
        s = self.event(s, "invalidate", reason="Reference update")
        s = self.event(s, "refresh", task=task(), user_approval_ref="revision-approval")
        self.assertEqual(g.next_action(s, "A")["action"], "exhausted")

    def test_patch_sees_failure_but_rerender_does_not(self):
        s = self.review(self.generated(self.state()), passed=False)
        self.assertEqual(g.generation_packet(s, "A", self.root)["images"][-1]["role"], "failed_output")
        s = self.review(self.generated(s), passed=False, issue="identity_drift")
        self.assertFalse(g.generation_packet(s, "A", self.root)["images"])

    def test_review_pack_has_no_creator_explanation_or_repair_note(self):
        s = self.review(self.generated(self.state()), passed=False)
        packet = g.review_packet(self.generated(s), "A", self.root)
        self.assertNotIn("prompt", packet)
        self.assertNotIn("correction", packet)
        self.assertNotIn("attempts", packet)

    def test_state_is_transactional_on_rejected_event(self):
        s = self.state()
        before = copy.deepcopy(s)
        with self.assertRaises(g.GuardError):
            self.event(s, "output", output=self.output)
        self.assertEqual(s, before)

    def test_position_map_bound_to_actual_group_hash(self):
        identity = dict(self.output, id="anchor", role="identity", approved=True, approval_ref="fixture")
        group = dict(self.output, id="group", role="group", source_task="G", source_revision=1)
        mapping = self.file("map.json", json.dumps({"group_sha256": "wrong", "inspected": True, "positions": {"V1": "left"}}).encode())
        mapping.update(id="map", role="position_map", source_task="G", source_revision=1)
        s = self.state(task("G", stage="group", references=[identity]),
                       task("I", stage="individual", subject="V1", references=[identity, group, mapping], dependencies={"G": 1}))
        s["jobs"]["G"].update(status="accepted", revision=1, output=self.output)
        with self.assertRaises(g.GuardError):
            self.event(s, "reserve", "I", context=self.ctx([self.output["sha256"]] * 2))

    def route_batch(self):
        s = self.state(*[task(f"R{i}", stage="route", requires_user_approval=True) for i in range(1, 5)])
        for key in list(s["jobs"]):
            s = self.review(self.generated(s, key), key)
        keys = sorted(s["jobs"])
        pairs = [{"a": a, "b": b, "different_dimensions": ["silhouette", "proportion", "face_grammar"],
                  "observation": "Synthetic comparison; no real visual claim."}
                 for n, a in enumerate(keys) for b in keys[n + 1:]]
        return s, dict(type="route_batch_review", context=self.ctx([self.output["sha256"]] * 4), pairs=pairs)

    def test_route_cannot_be_selected_without_batch_review(self):
        s, _ = self.route_batch()
        with self.assertRaises(g.GuardError):
            self.event(s, "approve", "R1", user_approval_ref="fixture")

    def test_full_pairwise_batch_review_unlocks_selection(self):
        s, event = self.route_batch()
        s = g.apply_event(s, event, self.root)
        s = self.event(s, "approve", "R1", user_approval_ref="fixture")
        self.assertEqual(s["jobs"]["R1"]["status"], "accepted")

    def test_failed_pairwise_review_retries_only_named_route(self):
        s, event = self.route_batch()
        event["pairs"][0]["different_dimensions"] = ["silhouette"]
        event.update(rework_ids=["R1"], repair_note="Find a different proportion and face grammar within the user's brief.")
        s = g.apply_event(s, event, self.root)
        self.assertEqual(g.next_action(s, "R1")["action"], "redesign")
        self.assertEqual(len(s["jobs"]["R1"]["attempts"]), 1)
        self.assertEqual(s["jobs"]["R2"]["status"], "awaiting_user_approval")

    def test_partial_pairwise_review_is_rejected(self):
        s, event = self.route_batch()
        event["pairs"] = event["pairs"][:1]
        with self.assertRaises(g.GuardError):
            g.apply_event(s, event, self.root)

    def test_batch_review_becomes_stale_after_source_change(self):
        s, event = self.route_batch()
        s = g.apply_event(s, event, self.root)
        s = self.event(s, "invalidate", "R2", reason="Superseded candidate")
        with self.assertRaises(g.GuardError):
            self.event(s, "approve", "R1", user_approval_ref="fixture")

    def test_extend_plan_preserves_old_budget(self):
        s = self.generated(self.state())
        s = g.apply_event(s, {"type": "extend_plan", "tasks": [task("B")], "user_approval_ref": "phase-authorization"}, self.root)
        self.assertEqual(len(s["jobs"]["A"]["attempts"]), 1)
        self.assertIn("B", s["jobs"])

    def test_extend_plan_cannot_rename_existing_subject(self):
        with self.assertRaises(g.GuardError):
            g.apply_event(self.state(), {"type": "extend_plan", "tasks": [task("B", subject="A")], "user_approval_ref": "fixture"}, self.root)

    def test_refresh_drops_obsolete_correction(self):
        s = self.review(self.generated(self.state()), passed=False, issue="spec_conflict")
        s = self.event(s, "refresh", task=task(prompt="New approved brief."), user_approval_ref="revision")
        self.assertIsNone(g.generation_packet(s, "A", self.root)["correction"])

    def test_output_cannot_overwrite_previous_attempt(self):
        s = self.review(self.generated(self.state()), passed=False, issue="identity_drift")
        s = self.event(s, "reserve", context=self.ctx())
        changed = self.file("figure.png", PNG + b"changed")
        with self.assertRaises(g.GuardError):
            self.event(s, "output", output=changed)

    def test_cli_init_cannot_overwrite_existing_ledger(self):
        plan = self.root / "plan.json"
        plan.write_text(json.dumps({"run_id": "fixture", "tasks": [task()]}))
        ledger = self.root / "ledger.json"
        command = [sys.executable, str(Path(g.__file__)), "init", str(ledger), str(plan)]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        first = ledger.read_bytes()
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
        self.assertEqual(ledger.read_bytes(), first)


if __name__ == "__main__":
    unittest.main()
