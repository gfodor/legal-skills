#!/usr/bin/env python3
"""Regression tests for coverage_state.py using only the standard library."""

from __future__ import annotations

import importlib.util
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch


SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPT = SKILL_DIR / "scripts" / "coverage_state.py"
SPEC = importlib.util.spec_from_file_location("coverage_state", SCRIPT)
assert SPEC and SPEC.loader
coverage_state = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coverage_state)


class CoverageStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="coverage-state-test-")
        self.root = Path(self.temp.name)
        self.run_dir = self.root / "run"
        self.ground_truth = self.root / "application.md"
        self.ground_truth.write_text("original application\n", encoding="utf-8")
        self.ground_truth_claims = self._write("claims.md", "original claims\n")
        self.ledger = self._write("coverage-ledger.md", "# Complete ledger\n")
        self.inputs = {
            "application": self.ground_truth,
            "claims": self.ground_truth_claims,
            "intake": self._write("intake.yaml", "run: {}\n"),
            "thesis": self._write("thesis.md", "# Thesis\n"),
            "search": self._write("search.md", "# Search\n"),
            "evidence": self._write("evidence.json", "{}\n"),
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _write(self, name: str, content: str) -> Path:
        path = self.root / name
        path.write_text(content, encoding="utf-8")
        return path

    def _candidate_args(self, entries: dict[str, Path]) -> list[str]:
        result: list[str] = []
        for label, path in entries.items():
            result.extend(["--candidate", f"{label}={path}"])
        return result

    def _run(self, *args: str, success: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )
        if success and result.returncode != 0:
            self.fail(f"command failed: {result.args}\n{result.stderr}\n{result.stdout}")
        if not success and result.returncode == 0:
            self.fail(f"command unexpectedly passed: {result.args}\n{result.stdout}")
        return result

    def _init(self) -> dict:
        result = self._run(
            "init",
            "--run-dir",
            str(self.run_dir),
            *self._candidate_args(self.inputs),
            "--authoritative",
            "application",
            "--authoritative",
            "claims",
        )
        return json.loads(result.stdout)

    def _decision(
        self,
        name: str,
        stage: str,
        decision: str,
        adversary: str,
        version: str,
        packet_hash: str,
        raw_report_hash: str | None = None,
        ledger_hash: str | None = None,
    ) -> Path:
        key = "DECISION" if stage == "raw" else "OUTER_DISPOSITION"
        extra = ""
        if stage == "adjudication":
            extra = (
                f"RAW_REPORT_SHA256: {raw_report_hash}\n"
                f"COVERAGE_LEDGER_SHA256: {ledger_hash}\n"
                "GATE_LEDGER_COMPLETE: YES\n"
                "GATE_SUPPORT_COMPLETE: YES\n"
                "GATE_PRIOR_ART_COMPLETE: YES\n"
                "GATE_CAPTURE_DECISIONS_COMPLETE: YES\n"
                "GATE_NO_UNRESOLVED_MATERIAL_ITEMS: YES\n"
                "GATE_NO_UNSUPPORTED_UMBRELLA_GAPS: YES\n"
            )
        return self._write(
            name,
            f"{key}: {decision}\n"
            f"ADVERSARY_CONTEXT_ID: {adversary}\n"
            f"APPLICATION_VERSION_ID: {version}\n"
            f"APPLICATION_PACKET_SHA256: {packet_hash}\n\n"
            f"{extra}\n"
            "# Decision record\n",
        )

    def _record(
        self,
        stage: str,
        decision_cli: str,
        decision_header: str,
        adversary: str,
        version: str,
        packet_hash: str,
        success: bool = True,
    ) -> dict | None:
        raw_report_hash = None
        if stage == "adjudication":
            state = json.loads((self.run_dir / "state.json").read_text(encoding="utf-8"))
            events = state["versions"][int(version[1:]) - 1]["events"]
            canonical = coverage_state.safe_name(adversary)
            raw_report_hash = next(
                event["document_sha256"]
                for event in reversed(events)
                if event["stage"] == "raw" and event["adversary"] == canonical
            )
        ledger_hash = hashlib.sha256(self.ledger.read_bytes()).hexdigest()
        document = self._decision(
            f"{version}-{adversary}-{stage}-{decision_cli}.md",
            stage,
            decision_header,
            adversary,
            version,
            packet_hash,
            raw_report_hash,
            ledger_hash,
        )
        result = self._run(
            "record",
            "--run-dir",
            str(self.run_dir),
            "--version",
            version,
            "--packet-sha256",
            packet_hash,
            "--adversary",
            adversary,
            "--stage",
            stage,
            "--decision",
            decision_cli,
            "--document",
            str(document),
            *(["--ledger", str(self.ledger)] if stage == "adjudication" else []),
            success=success,
        )
        return json.loads(result.stdout) if success else None

    def test_staged_qualification_and_authoritative_promotion(self) -> None:
        initial = self._init()
        self.assertTrue(initial["promoted"])
        candidate = self._write("proposal.md", "amended application\n")
        candidate_claims = self._write("proposal-claims.md", "amended claims\n")
        proposal = dict(self.inputs, application=candidate, claims=candidate_claims)
        snapshot = self._run(
            "snapshot",
            "--run-dir",
            str(self.run_dir),
            *self._candidate_args(proposal),
        )
        version = json.loads(snapshot.stdout)
        packet_hash = version["packet_sha256"]

        shutil.copy2(candidate, self.ground_truth)
        shutil.copy2(candidate_claims, self.ground_truth_claims)
        self._run(
            "promote",
            "--run-dir",
            str(self.run_dir),
            "--version",
            "v002",
            *self._candidate_args(self.inputs),
            success=False,
        )
        self.ground_truth.write_text("original application\n", encoding="utf-8")
        self.ground_truth_claims.write_text("original claims\n", encoding="utf-8")
        raw = self._record(
            "raw", "gaps-found", "GAPS_FOUND", "Competitor-01", "v002", packet_hash
        )
        self.assertEqual(raw["qualifying_cycles"], 0)
        self._record(
            "adjudication",
            "no-material-gap",
            "NO_MATERIAL_GAP",
            "competitor-01",
            "v002",
            packet_hash,
            success=False,
        )
        first = self._record(
            "adjudication",
            "only-accepted-gaps",
            "ONLY_ACCEPTED_GAPS",
            "competitor-01",
            "v002",
            packet_hash,
        )
        self.assertEqual(first["qualifying_cycles"], 1)
        self._record(
            "raw",
            "no-material-gap",
            "NO_MATERIAL_GAP",
            "competitor-02",
            "v002",
            packet_hash,
        )
        second = self._record(
            "adjudication",
            "no-material-gap",
            "NO_MATERIAL_GAP",
            "competitor-02",
            "v002",
            packet_hash,
        )
        self.assertFalse(second["success"])
        self.assertEqual(second["qualifying_cycles"], 2)

        self._run(
            "promote",
            "--run-dir",
            str(self.run_dir),
            "--version",
            "v002",
            *self._candidate_args(proposal),
            success=False,
        )
        shutil.copy2(candidate, self.ground_truth)
        shutil.copy2(candidate_claims, self.ground_truth_claims)
        promoted = self._run(
            "promote",
            "--run-dir",
            str(self.run_dir),
            "--version",
            "v002",
            *self._candidate_args(self.inputs),
        )
        self.assertTrue(json.loads(promoted.stdout)["success"])
        self.ground_truth_claims.write_text("post-promotion drift\n", encoding="utf-8")
        self._run("status", "--run-dir", str(self.run_dir), success=False)

    def test_metadata_binding_and_latest_raw_reset(self) -> None:
        initial = self._init()
        packet_hash = initial["packet_sha256"]
        wrong = self._decision(
            "wrong.md", "raw", "INCOMPLETE", "competitor-01", "v001", packet_hash
        )
        self._run(
            "record",
            "--run-dir",
            str(self.run_dir),
            "--version",
            "v001",
            "--packet-sha256",
            packet_hash,
            "--adversary",
            "competitor-01",
            "--stage",
            "raw",
            "--decision",
            "no-material-gap",
            "--document",
            str(wrong),
            success=False,
        )
        reusable = self._decision(
            "reused.md",
            "raw",
            "NO_MATERIAL_GAP",
            "competitor-01",
            "v001",
            packet_hash,
        )
        self._run(
            "record",
            "--run-dir",
            str(self.run_dir),
            "--version",
            "v001",
            "--packet-sha256",
            packet_hash,
            "--adversary",
            "competitor-01",
            "--stage",
            "raw",
            "--decision",
            "no-material-gap",
            "--document",
            str(reusable),
        )
        self._run(
            "record",
            "--run-dir",
            str(self.run_dir),
            "--version",
            "v001",
            "--packet-sha256",
            packet_hash,
            "--adversary",
            "competitor-02",
            "--stage",
            "raw",
            "--decision",
            "no-material-gap",
            "--document",
            str(reusable),
            success=False,
        )
        for adversary in ("competitor-01", "competitor-02"):
            self._record(
                "raw",
                "no-material-gap",
                "NO_MATERIAL_GAP",
                adversary,
                "v001",
                packet_hash,
            )
            result = self._record(
                "adjudication",
                "no-material-gap",
                "NO_MATERIAL_GAP",
                adversary,
                "v001",
                packet_hash,
            )
        self.assertTrue(result["success"])
        reset = self._record(
            "raw", "gaps-found", "GAPS_FOUND", "COMPETITOR-01", "v001", packet_hash
        )
        self.assertFalse(reset["success"])
        self.assertEqual(reset["qualifying_cycles"], 1)

    def test_packet_schema_collisions_and_tamper_detection(self) -> None:
        incomplete = {"application": self.ground_truth}
        self._run(
            "init",
            "--run-dir",
            str(self.run_dir),
            *self._candidate_args(incomplete),
            success=False,
        )
        collision = dict(
            self.inputs,
            **{"application.md": self._write("suffixless", "collision\n")},
        )
        self._run(
            "init",
            "--run-dir",
            str(self.root / "collision-run"),
            *self._candidate_args(collision),
            success=False,
        )
        initial = self._init()
        packet_hash = initial["packet_sha256"]
        extra = dict(self.inputs, drawings=self._write("drawings.pdf", "drawing\n"))
        self._run(
            "snapshot",
            "--run-dir",
            str(self.run_dir),
            *self._candidate_args(extra),
            success=False,
        )
        self._record(
            "raw", "no-material-gap", "NO_MATERIAL_GAP", "competitor-01", "v001", packet_hash
        )
        state = json.loads((self.run_dir / "state.json").read_text(encoding="utf-8"))
        Path(state["versions"][0]["files"][0]["snapshot_path"]).write_text(
            "tampered\n", encoding="utf-8"
        )
        self._run("status", "--run-dir", str(self.run_dir), success=False)

    def test_archived_decision_tamper_detection(self) -> None:
        initial = self._init()
        packet_hash = initial["packet_sha256"]
        self._record(
            "raw", "no-material-gap", "NO_MATERIAL_GAP", "competitor-01", "v001", packet_hash
        )
        state_path = self.run_dir / "state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["versions"][0]["events"][0]["decision"] = "gaps-found"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        self._run("status", "--run-dir", str(self.run_dir), success=False)
        state["versions"][0]["events"][0]["decision"] = "no-material-gap"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        record = Path(state["versions"][0]["events"][0]["document_path"])
        record.write_text("tampered decision\n", encoding="utf-8")
        self._run("status", "--run-dir", str(self.run_dir), success=False)

    def test_stale_adjudication_cannot_bind_new_raw_report(self) -> None:
        initial = self._init()
        packet_hash = initial["packet_sha256"]
        raw_one = self._decision(
            "raw-one.md", "raw", "GAPS_FOUND", "competitor-01", "v001", packet_hash
        )
        raw_one.write_text(raw_one.read_text(encoding="utf-8") + "first report\n")
        first = self._run(
            "record",
            "--run-dir",
            str(self.run_dir),
            "--version",
            "v001",
            "--packet-sha256",
            packet_hash,
            "--adversary",
            "competitor-01",
            "--stage",
            "raw",
            "--decision",
            "gaps-found",
            "--document",
            str(raw_one),
        )
        raw_hash = json.loads(first.stdout)["recorded_event"]["document_sha256"]
        ledger_hash = hashlib.sha256(self.ledger.read_bytes()).hexdigest()
        adjudication = self._decision(
            "adjudication-one.md",
            "adjudication",
            "ONLY_ACCEPTED_GAPS",
            "competitor-01",
            "v001",
            packet_hash,
            raw_hash,
            ledger_hash,
        )
        base_args = [
            "record",
            "--run-dir",
            str(self.run_dir),
            "--version",
            "v001",
            "--packet-sha256",
            packet_hash,
            "--adversary",
            "competitor-01",
        ]
        self._run(
            *base_args,
            "--stage",
            "adjudication",
            "--decision",
            "only-accepted-gaps",
            "--document",
            str(adjudication),
            "--ledger",
            str(self.ledger),
        )
        raw_two = self._decision(
            "raw-two.md", "raw", "GAPS_FOUND", "competitor-01", "v001", packet_hash
        )
        raw_two.write_text(raw_two.read_text(encoding="utf-8") + "second report\n")
        self._run(
            *base_args,
            "--stage",
            "raw",
            "--decision",
            "gaps-found",
            "--document",
            str(raw_two),
        )
        self._run(
            *base_args,
            "--stage",
            "adjudication",
            "--decision",
            "only-accepted-gaps",
            "--document",
            str(adjudication),
            "--ledger",
            str(self.ledger),
            success=False,
        )

    def test_incomplete_gates_and_ledger_tamper_are_rejected(self) -> None:
        initial = self._init()
        packet_hash = initial["packet_sha256"]
        self._record(
            "raw", "gaps-found", "GAPS_FOUND", "competitor-01", "v001", packet_hash
        )
        state = json.loads((self.run_dir / "state.json").read_text(encoding="utf-8"))
        raw_hash = state["versions"][0]["events"][0]["document_sha256"]
        ledger_hash = hashlib.sha256(self.ledger.read_bytes()).hexdigest()
        incomplete = self._decision(
            "incomplete-adjudication.md",
            "adjudication",
            "ONLY_ACCEPTED_GAPS",
            "competitor-01",
            "v001",
            packet_hash,
            raw_hash,
            ledger_hash,
        )
        incomplete.write_text(
            incomplete.read_text(encoding="utf-8").replace(
                "GATE_SUPPORT_COMPLETE: YES", "GATE_SUPPORT_COMPLETE: NO"
            ),
            encoding="utf-8",
        )
        args = [
            "record",
            "--run-dir",
            str(self.run_dir),
            "--version",
            "v001",
            "--packet-sha256",
            packet_hash,
            "--adversary",
            "competitor-01",
            "--stage",
            "adjudication",
            "--decision",
            "only-accepted-gaps",
            "--document",
            str(incomplete),
            "--ledger",
            str(self.ledger),
        ]
        self._run(*args, success=False)
        self._record(
            "adjudication",
            "only-accepted-gaps",
            "ONLY_ACCEPTED_GAPS",
            "competitor-01",
            "v001",
            packet_hash,
        )
        state = json.loads((self.run_dir / "state.json").read_text(encoding="utf-8"))
        archived_ledger = Path(state["versions"][0]["events"][1]["ledger_path"])
        archived_ledger.write_text("tampered ledger\n", encoding="utf-8")
        self._run("status", "--run-dir", str(self.run_dir), success=False)

    def test_post_copy_hash_mismatch_cleans_staging(self) -> None:
        entries = coverage_state.parse_candidates([f"application={self.ground_truth}"])
        target_run = self.root / "corrupt-run"
        with patch.object(
            coverage_state.shutil,
            "copy2",
            side_effect=lambda _source, target: Path(target).write_bytes(b"corrupt"),
        ):
            with redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    coverage_state.copy_snapshot(target_run, "v999", entries)
        self.assertFalse((target_run / "versions" / "v999").exists())
        self.assertFalse((target_run / "versions" / ".v999.tmp").exists())


if __name__ == "__main__":
    unittest.main()
