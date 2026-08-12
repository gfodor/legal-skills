#!/usr/bin/env python3
"""Version-lock patent workaround challenges using only the standard library."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = 2
TARGET_QUALIFYING_CYCLES = 2
REQUIRED_PACKET_LABELS = {"application", "intake", "thesis", "search", "evidence"}
RAW_DECISIONS = {"gaps-found", "no-material-gap", "incomplete"}
ADJUDICATION_DECISIONS = {
    "no-material-gap",
    "only-accepted-gaps",
    "blocked",
    "withdrawn",
}
DECISIONS_BY_STAGE = {
    "raw": RAW_DECISIONS,
    "adjudication": ADJUDICATION_DECISIONS,
}
QUALIFYING_PAIRS = {
    ("no-material-gap", "no-material-gap"),
    ("gaps-found", "only-accepted-gaps"),
}
ADJUDICATION_GATE_HEADERS = {
    "GATE_LEDGER_COMPLETE",
    "GATE_SUPPORT_COMPLETE",
    "GATE_PRIOR_ART_COMPLETE",
    "GATE_CAPTURE_DECISIONS_COMPLETE",
    "GATE_NO_UNRESOLVED_MATERIAL_ITEMS",
    "GATE_NO_UNSUPPORTED_UMBRELLA_GAPS",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def die(message: str, code: int = 2) -> None:
    print(json.dumps({"error": message}, indent=2), file=sys.stderr)
    raise SystemExit(code)


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-.")
    return (cleaned or "item").casefold()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_candidates(values: list[str]) -> list[dict[str, str | int]]:
    entries: list[dict[str, str | int]] = []
    labels: set[str] = set()
    destinations: set[str] = set()
    for raw in values:
        if "=" in raw:
            label, raw_path = raw.split("=", 1)
        else:
            raw_path = raw
            label = Path(raw_path).stem
        label = safe_name(label)
        if label in labels:
            die(f"duplicate candidate label: {label}")
        path = Path(raw_path).expanduser().resolve()
        if not path.is_file():
            die(f"candidate is not a file: {path}")
        suffix = "".join(path.suffixes)
        snapshot_filename = f"{label}{suffix}"
        destination_key = snapshot_filename.casefold()
        if destination_key in destinations:
            die(f"candidate snapshot filename collision: {snapshot_filename}")
        labels.add(label)
        destinations.add(destination_key)
        entries.append(
            {
                "label": label,
                "source_path": str(path),
                "filename": path.name,
                "snapshot_filename": snapshot_filename,
                "sha256": sha256_file(path),
                "size": path.stat().st_size,
            }
        )
    if not entries:
        die("at least one --candidate is required")
    entries.sort(key=lambda item: str(item["label"]))
    return entries


def packet_hash(entries: list[dict[str, str | int]]) -> str:
    digest = hashlib.sha256()
    digest.update(b"patent-workaround-packet-v2\0")
    for entry in entries:
        digest.update(str(entry["label"]).encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(str(entry["sha256"])))
        digest.update(b"\0")
    return digest.hexdigest()


def state_path(run_dir: Path) -> Path:
    return run_dir / "state.json"


def load_state(run_dir: Path, verify_authoritative: bool = True) -> dict:
    path = state_path(run_dir)
    if not path.is_file():
        die(f"state not found: {path}")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        die(f"cannot read state: {exc}")
    if state.get("schema_version") != SCHEMA_VERSION:
        die("unsupported state schema version")
    validate_state(run_dir, state, verify_authoritative=verify_authoritative)
    return state


def save_state(run_dir: Path, state: dict) -> None:
    path = state_path(run_dir)
    temp = path.with_suffix(".json.tmp")
    temp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def get_version(state: dict, version_id: str | None = None) -> dict:
    wanted = version_id or state.get("current_version")
    for version in state["versions"]:
        if version["id"] == wanted:
            return version
    die(f"version not found: {wanted}")
    raise AssertionError


def require_packet_labels(
    entries: list[dict[str, str | int]], expected: set[str] | None = None
) -> set[str]:
    labels = {str(entry["label"]) for entry in entries}
    missing = REQUIRED_PACKET_LABELS - labels
    if missing:
        die(f"packet is missing required labels: {', '.join(sorted(missing))}")
    if expected is not None and labels != expected:
        omitted = expected - labels
        added = labels - expected
        details = []
        if omitted:
            details.append(f"omitted: {', '.join(sorted(omitted))}")
        if added:
            details.append(f"added: {', '.join(sorted(added))}")
        die(f"packet labels differ from initialization ({'; '.join(details)})")
    return labels


def validate_state(
    run_dir: Path, state: dict, verify_authoritative: bool = True
) -> None:
    versions = state.get("versions")
    if not isinstance(versions, list) or not versions:
        die("state contains no versions")
    if state.get("current_version") not in {version.get("id") for version in versions}:
        die("current version is missing from state")
    expected_labels = set(state.get("packet_labels", []))
    if not expected_labels:
        die("state contains no packet label schema")
    if not REQUIRED_PACKET_LABELS <= expected_labels:
        die("state packet label schema omits required labels")
    authoritative = state.get("authoritative_destinations")
    if (
        not isinstance(authoritative, dict)
        or "application" not in authoritative
        or not set(authoritative) <= expected_labels
    ):
        die("state authoritative-destination schema is inconsistent")
    for version in versions:
        version_id = version.get("id")
        files = version.get("files")
        if not isinstance(version_id, str) or not isinstance(files, list):
            die("state contains a malformed version")
        if {str(entry.get("label")) for entry in files} != expected_labels:
            die(f"version {version_id} has an inconsistent packet label set")
        snapshot_dir = (run_dir / "versions" / version_id).resolve()
        for entry in files:
            path = Path(str(entry.get("snapshot_path", ""))).resolve()
            if path.parent != snapshot_dir or not path.is_file():
                die(f"archived packet file is missing or misplaced: {path}")
            if path.stat().st_size != entry.get("size"):
                die(f"archived packet size mismatch: {path}")
            if sha256_file(path) != entry.get("sha256"):
                die(f"archived packet hash mismatch: {path}")
        if packet_hash(files) != version.get("packet_sha256"):
            die(f"packet hash mismatch in version {version_id}")
        latest_raw: dict[str, dict] = {}
        raw_hash_owner: dict[str, str] = {}
        for event in version.get("events", []):
            adversary = event.get("adversary")
            stage = event.get("stage")
            decision = event.get("decision")
            if stage not in DECISIONS_BY_STAGE or decision not in DECISIONS_BY_STAGE[stage]:
                die(f"invalid decision event in version {version_id}")
            if event.get("version_id") != version_id:
                die(f"event version binding mismatch: {event.get('event_id')}")
            if event.get("packet_sha256") != version.get("packet_sha256"):
                die(f"event packet binding mismatch: {event.get('event_id')}")
            expected_dir = (run_dir / "records" / version_id / str(adversary)).resolve()
            path = Path(str(event.get("document_path", ""))).resolve()
            if path.parent != expected_dir or not path.is_file():
                die(f"archived decision record is missing or misplaced: {path}")
            if sha256_file(path) != event.get("document_sha256"):
                die(f"archived decision record hash mismatch: {path}")
            headers = parse_decision_document(path, str(stage))
            if safe_name(headers["ADVERSARY_CONTEXT_ID"]) != adversary:
                die(f"archived decision adversary mismatch: {path}")
            if headers["APPLICATION_VERSION_ID"] != version_id:
                die(f"archived decision version mismatch: {path}")
            if headers["APPLICATION_PACKET_SHA256"].casefold() != str(
                version.get("packet_sha256")
            ).casefold():
                die(f"archived decision packet mismatch: {path}")
            if headers["normalized_decision"] != decision:
                die(f"archived decision disposition mismatch: {path}")
            if stage == "raw":
                owner = raw_hash_owner.get(str(event["document_sha256"]))
                if owner is not None and owner != adversary:
                    die("one raw report is credited to multiple adversaries")
                raw_hash_owner[str(event["document_sha256"])] = str(adversary)
                latest_raw[str(adversary)] = event
            else:
                raw = latest_raw.get(str(adversary))
                if raw is None:
                    die(f"adjudication has no preceding raw decision: {path}")
                if headers["RAW_REPORT_SHA256"].casefold() != raw[
                    "document_sha256"
                ].casefold():
                    die(f"adjudication is bound to a stale raw report: {path}")
                if event.get("raw_report_sha256") != raw["document_sha256"]:
                    die(f"adjudication event has a stale raw-report binding: {path}")
                ledger_path = Path(str(event.get("ledger_path", ""))).resolve()
                if ledger_path.parent != expected_dir or not ledger_path.is_file():
                    die(f"archived adjudication ledger is missing: {ledger_path}")
                if sha256_file(ledger_path) != event.get("ledger_sha256"):
                    die(f"archived adjudication ledger hash mismatch: {ledger_path}")
                if headers["COVERAGE_LEDGER_SHA256"].casefold() != str(
                    event.get("ledger_sha256")
                ).casefold():
                    die(f"adjudication ledger header mismatch: {path}")
                if decision in {"no-material-gap", "only-accepted-gaps"} and (
                    raw["decision"], decision
                ) not in QUALIFYING_PAIRS:
                    die(f"invalid qualifying transition in archived record: {path}")
    promoted_version = get_version(state, state.get("promoted_version"))
    if not promoted_version.get("promoted"):
        die("state promoted-version pointer is invalid")
    if verify_authoritative:
        promoted_files = {
            str(entry["label"]): entry for entry in promoted_version["files"]
        }
        for label, destination in authoritative.items():
            path = Path(str(destination)).resolve()
            if not path.is_file():
                die(f"authoritative ground-truth file is missing: {path}")
            if sha256_file(path) != promoted_files[label]["sha256"]:
                die(f"authoritative ground truth differs from promoted packet: {path}")


def parse_decision_document(path: Path, stage: str) -> dict[str, str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        die(f"decision document must be readable UTF-8 text: {exc}")
    nonempty = [line.strip() for line in lines if line.strip()]
    decision_key = "DECISION" if stage == "raw" else "OUTER_DISPOSITION"
    if not nonempty or not nonempty[0].startswith(f"{decision_key}:"):
        die(f"first non-empty line must be {decision_key}: <value>")
    wanted = {
        decision_key,
        "ADVERSARY_CONTEXT_ID",
        "APPLICATION_VERSION_ID",
        "APPLICATION_PACKET_SHA256",
    }
    if stage == "adjudication":
        wanted |= {
            "RAW_REPORT_SHA256",
            "COVERAGE_LEDGER_SHA256",
        }
        wanted |= ADJUDICATION_GATE_HEADERS
    headers: dict[str, str] = {}
    for line in nonempty[:20]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in wanted:
            continue
        if key in headers:
            die(f"duplicate decision header: {key}")
        headers[key] = value.strip()
    missing = wanted - headers.keys()
    if missing:
        die(f"decision document is missing headers: {', '.join(sorted(missing))}")
    if stage == "adjudication":
        incomplete = [key for key in ADJUDICATION_GATE_HEADERS if headers[key] != "YES"]
        if incomplete:
            die(f"adjudication gates are not confirmed YES: {', '.join(sorted(incomplete))}")
    headers["normalized_decision"] = headers[decision_key].casefold().replace("_", "-")
    return headers


def copy_snapshot(
    run_dir: Path,
    version_id: str,
    entries: list[dict[str, str | int]],
) -> None:
    versions_dir = run_dir / "versions"
    target_dir = versions_dir / version_id
    staging_dir = versions_dir / f".{version_id}.tmp"
    if target_dir.exists() or staging_dir.exists():
        die(f"snapshot destination already exists for {version_id}")
    staging_dir.mkdir(parents=True)
    try:
        for entry in entries:
            source = Path(str(entry["source_path"]))
            target = staging_dir / str(entry["snapshot_filename"])
            shutil.copy2(source, target)
            actual = sha256_file(target)
            if actual != entry["sha256"]:
                die(f"snapshot hash mismatch after copying {source}")
            entry["size"] = target.stat().st_size
        staging_dir.replace(target_dir)
    except BaseException:
        shutil.rmtree(staging_dir, ignore_errors=True)
        raise
    for entry in entries:
        target = target_dir / str(entry["snapshot_filename"])
        entry["snapshot_path"] = str(target.resolve())


def new_version(
    run_dir: Path,
    state: dict,
    entries: list[dict[str, str | int]],
    promoted: bool,
) -> dict:
    version_id = f"v{len(state['versions']) + 1:03d}"
    copy_snapshot(run_dir, version_id, entries)
    version = {
        "id": version_id,
        "packet_sha256": packet_hash(entries),
        "created_at": utc_now(),
        "promoted": promoted,
        "promoted_at": utc_now() if promoted else None,
        "files": entries,
        "events": [],
    }
    state["versions"].append(version)
    state["current_version"] = version_id
    return version


def latest_decision_pairs(version: dict) -> dict[str, tuple[dict, dict | None]]:
    pairs: dict[str, tuple[dict, dict | None]] = {}
    for event in version["events"]:
        adversary = event["adversary"]
        if event["stage"] == "raw":
            pairs[adversary] = (event, None)
        elif adversary in pairs:
            raw, _ = pairs[adversary]
            pairs[adversary] = (raw, event)
    return pairs


def qualification_summary(state: dict) -> dict:
    current = get_version(state)
    pairs = latest_decision_pairs(current)
    qualifying = sorted(
        adversary
        for adversary, (raw, adjudication) in pairs.items()
        if adjudication is not None
        and (raw["decision"], adjudication["decision"]) in QUALIFYING_PAIRS
    )
    count = len(qualifying)
    return {
        "current_version": current["id"],
        "packet_sha256": current["packet_sha256"],
        "promoted": current["promoted"],
        "qualifying_adversary_ids": qualifying,
        "qualifying_cycles": count,
        "target_qualifying_cycles": TARGET_QUALIFYING_CYCLES,
        "success": bool(current["promoted"] and count >= TARGET_QUALIFYING_CYCLES),
    }


def command_init(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).expanduser().resolve()
    if state_path(run_dir).exists():
        die(f"state already exists: {state_path(run_dir)}")
    run_dir.mkdir(parents=True, exist_ok=True)
    entries = parse_candidates(args.candidate)
    labels = require_packet_labels(entries)
    authoritative_labels = {safe_name(label) for label in args.authoritative}
    if len(authoritative_labels) != len(args.authoritative):
        die("authoritative labels must be distinct after normalization")
    if "application" not in authoritative_labels:
        die("application must be an authoritative ground-truth label")
    unknown_authoritative = authoritative_labels - labels
    if unknown_authoritative:
        die(
            "authoritative labels are absent from the packet: "
            f"{', '.join(sorted(unknown_authoritative))}"
        )
    by_label = {str(entry["label"]): entry for entry in entries}
    state = {
        "schema_version": SCHEMA_VERSION,
        "created_at": utc_now(),
        "current_version": None,
        "packet_labels": sorted(labels),
        "authoritative_destinations": {
            label: str(by_label[label]["source_path"])
            for label in sorted(authoritative_labels)
        },
        "versions": [],
    }
    version = new_version(run_dir, state, entries, promoted=True)
    state["promoted_version"] = version["id"]
    save_state(run_dir, state)
    print(json.dumps(qualification_summary(state), indent=2))


def command_snapshot(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).expanduser().resolve()
    state = load_state(run_dir)
    entries = parse_candidates(args.candidate)
    require_packet_labels(entries, set(state["packet_labels"]))
    digest = packet_hash(entries)
    current = get_version(state)
    if digest == current["packet_sha256"]:
        result = qualification_summary(state)
        result["snapshot_created"] = False
    else:
        new_version(run_dir, state, entries, promoted=False)
        save_state(run_dir, state)
        result = qualification_summary(state)
        result["snapshot_created"] = True
    print(json.dumps(result, indent=2))


def command_record(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).expanduser().resolve()
    state = load_state(run_dir)
    version = get_version(state, args.version)
    if args.packet_sha256.casefold() != version["packet_sha256"].casefold():
        die(
            "packet hash does not match the selected version: "
            f"expected {version['packet_sha256']}, got {args.packet_sha256}"
        )
    if args.decision not in DECISIONS_BY_STAGE[args.stage]:
        allowed = ", ".join(sorted(DECISIONS_BY_STAGE[args.stage]))
        die(f"decision {args.decision!r} is invalid for {args.stage}; use: {allowed}")
    document = Path(args.document).expanduser().resolve()
    if not document.is_file():
        die(f"record document is not a file: {document}")
    adversary = safe_name(args.adversary)
    headers = parse_decision_document(document, args.stage)
    if safe_name(headers["ADVERSARY_CONTEXT_ID"]) != adversary:
        die("decision document adversary context ID does not match --adversary")
    if headers["APPLICATION_VERSION_ID"] != version["id"]:
        die("decision document version does not match --version")
    if headers["APPLICATION_PACKET_SHA256"].casefold() != version[
        "packet_sha256"
    ].casefold():
        die("decision document packet hash does not match the selected version")
    if headers["normalized_decision"] != args.decision:
        die("decision document decision does not match --decision")
    document_sha256 = sha256_file(document)
    ledger: Path | None = None
    ledger_sha256: str | None = None
    if args.stage == "raw":
        duplicate = next(
            (
                event
                for event in version["events"]
                if event["stage"] == "raw"
                and event["adversary"] != adversary
                and event["document_sha256"] == document_sha256
            ),
            None,
        )
        if duplicate is not None:
            die(
                "raw report is already credited to a different adversary: "
                f"{duplicate['adversary']}"
            )
    if args.stage == "adjudication":
        if not args.ledger:
            die("--ledger is required for an adjudication record")
        ledger = Path(args.ledger).expanduser().resolve()
        if not ledger.is_file():
            die(f"coverage ledger is not a file: {ledger}")
        ledger_sha256 = sha256_file(ledger)
        pairs = latest_decision_pairs(version)
        if adversary not in pairs:
            die(f"no raw decision exists for adversary: {adversary}")
        raw, _ = pairs[adversary]
        if headers["RAW_REPORT_SHA256"].casefold() != raw[
            "document_sha256"
        ].casefold():
            die("adjudication does not identify the latest raw report hash")
        if headers["COVERAGE_LEDGER_SHA256"].casefold() != ledger_sha256.casefold():
            die("adjudication does not identify the supplied coverage-ledger hash")
        pair = (raw["decision"], args.decision)
        if args.decision in {"no-material-gap", "only-accepted-gaps"}:
            if pair not in QUALIFYING_PAIRS:
                die(
                    "invalid qualifying transition: "
                    f"raw {raw['decision']!r} to adjudication {args.decision!r}"
                )
    event_number = len(version["events"]) + 1
    record_dir = run_dir / "records" / version["id"] / adversary
    record_dir.mkdir(parents=True, exist_ok=True)
    target = record_dir / f"{event_number:03d}-{args.stage}-{safe_name(document.name)}"
    staging = target.with_suffix(target.suffix + ".tmp")
    ledger_target = (
        record_dir / f"{event_number:03d}-ledger-{safe_name(ledger.name)}"
        if ledger is not None
        else None
    )
    ledger_staging = (
        ledger_target.with_suffix(ledger_target.suffix + ".tmp")
        if ledger_target is not None
        else None
    )
    destinations = [path for path in (target, staging, ledger_target, ledger_staging) if path]
    if any(path.exists() for path in destinations):
        die(f"decision record destination already exists: {target}")
    try:
        shutil.copy2(document, staging)
        if sha256_file(staging) != document_sha256:
            die(f"decision record hash mismatch after copying {document}")
        if ledger is not None and ledger_staging is not None:
            shutil.copy2(ledger, ledger_staging)
            if sha256_file(ledger_staging) != ledger_sha256:
                die(f"coverage-ledger hash mismatch after copying {ledger}")
        staging.replace(target)
        if ledger_staging is not None and ledger_target is not None:
            ledger_staging.replace(ledger_target)
    except BaseException:
        staging.unlink(missing_ok=True)
        if ledger_staging is not None:
            ledger_staging.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        if ledger_target is not None:
            ledger_target.unlink(missing_ok=True)
        raise
    event = {
        "event_id": f"{version['id']}-e{event_number:03d}",
        "adversary": adversary,
        "stage": args.stage,
        "decision": args.decision,
        "version_id": version["id"],
        "packet_sha256": version["packet_sha256"],
        "created_at": utc_now(),
        "document_sha256": document_sha256,
        "document_path": str(target.resolve()),
        "notes": args.notes,
    }
    if args.stage == "adjudication":
        event.update(
            {
                "raw_report_sha256": raw["document_sha256"],
                "ledger_sha256": ledger_sha256,
                "ledger_path": str(ledger_target.resolve()),
            }
        )
    version["events"].append(event)
    save_state(run_dir, state)
    result = qualification_summary(state)
    result["recorded_event"] = event
    print(json.dumps(result, indent=2))


def command_promote(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).expanduser().resolve()
    state = load_state(run_dir, verify_authoritative=False)
    version = get_version(state, args.version)
    if version["id"] != state["current_version"]:
        die("only the current version may be promoted")
    entries = parse_candidates(args.candidate)
    require_packet_labels(entries, set(state["packet_labels"]))
    by_label = {str(entry["label"]): entry for entry in entries}
    for label, expected_path in state["authoritative_destinations"].items():
        actual_path = Path(str(by_label[label]["source_path"])).resolve()
        if not actual_path.samefile(Path(expected_path).resolve()):
            die(
                f"promotion for {label} must use the initialized authoritative path: "
                f"{expected_path}"
            )
    digest = packet_hash(entries)
    if digest != version["packet_sha256"]:
        die(
            "promotion packet does not match the challenged candidate: "
            f"expected {version['packet_sha256']}, got {digest}"
        )
    summary = qualification_summary(state)
    if not version["promoted"] and summary["qualifying_cycles"] < TARGET_QUALIFYING_CYCLES:
        die(
            "candidate lacks the required qualifying dispositions: "
            f"{summary['qualifying_cycles']}/{TARGET_QUALIFYING_CYCLES}"
        )
    if not version["promoted"]:
        version["promoted"] = True
        version["promoted_at"] = utc_now()
        version["promotion_receipt"] = [
            {
                "label": entry["label"],
                "path": entry["source_path"],
                "sha256": entry["sha256"],
            }
            for entry in entries
        ]
        state["promoted_version"] = version["id"]
    validate_state(run_dir, state, verify_authoritative=True)
    save_state(run_dir, state)
    print(json.dumps(qualification_summary(state), indent=2))


def command_status(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).expanduser().resolve()
    state = load_state(run_dir)
    result = qualification_summary(state)
    result["versions"] = [
        {
            "id": version["id"],
            "packet_sha256": version["packet_sha256"],
            "promoted": version["promoted"],
            "event_count": len(version["events"]),
        }
        for version in state["versions"]
    ]
    print(json.dumps(result, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Track exact patent challenge packets and workaround decisions."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--run-dir", required=True)
    init_parser.add_argument("--candidate", action="append", required=True)
    init_parser.add_argument("--authoritative", action="append", required=True)
    init_parser.set_defaults(func=command_init)

    snapshot_parser = subparsers.add_parser("snapshot")
    snapshot_parser.add_argument("--run-dir", required=True)
    snapshot_parser.add_argument("--candidate", action="append", required=True)
    snapshot_parser.set_defaults(func=command_snapshot)

    record_parser = subparsers.add_parser("record")
    record_parser.add_argument("--run-dir", required=True)
    record_parser.add_argument("--version", required=True)
    record_parser.add_argument("--packet-sha256", required=True)
    record_parser.add_argument("--adversary", required=True)
    record_parser.add_argument(
        "--stage", choices=sorted(DECISIONS_BY_STAGE), required=True
    )
    record_parser.add_argument(
        "--decision",
        choices=sorted(RAW_DECISIONS | ADJUDICATION_DECISIONS),
        required=True,
    )
    record_parser.add_argument("--document", required=True)
    record_parser.add_argument("--ledger")
    record_parser.add_argument("--notes", default="")
    record_parser.set_defaults(func=command_record)

    promote_parser = subparsers.add_parser("promote")
    promote_parser.add_argument("--run-dir", required=True)
    promote_parser.add_argument("--version", required=True)
    promote_parser.add_argument("--candidate", action="append", required=True)
    promote_parser.set_defaults(func=command_promote)

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--run-dir", required=True)
    status_parser.set_defaults(func=command_status)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
