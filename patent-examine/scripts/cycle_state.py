#!/usr/bin/env python3
"""Version-lock simulated patent examination cycles using only the standard library."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = 1
CLEARANCE_DECISIONS = {"conditional-allowable", "allowable"}
DECISIONS = [
    "office-action",
    "continued-rejection",
    "conditional-allowable",
    "allowable",
    "incomplete",
    "withdrawn",
    "blocked",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def die(message: str, code: int = 2) -> None:
    print(json.dumps({"error": message}, indent=2), file=sys.stderr)
    raise SystemExit(code)


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-.")
    return cleaned or "item"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_candidates(values: list[str]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    labels: set[str] = set()
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
        labels.add(label)
        entries.append(
            {
                "label": label,
                "source_path": str(path),
                "filename": path.name,
                "sha256": sha256_file(path),
                "size": path.stat().st_size,
            }
        )
    if not entries:
        die("at least one --candidate is required")
    entries.sort(key=lambda item: item["label"])
    return entries


def packet_hash(entries: list[dict[str, str]]) -> str:
    digest = hashlib.sha256()
    digest.update(b"patent-examine-packet-v1\0")
    for entry in entries:
        digest.update(entry["label"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(entry["sha256"]))
        digest.update(b"\0")
    return digest.hexdigest()


def state_path(run_dir: Path) -> Path:
    return run_dir / "state.json"


def load_state(run_dir: Path) -> dict:
    path = state_path(run_dir)
    if not path.is_file():
        die(f"state not found: {path}")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        die(f"cannot read state: {exc}")
    if state.get("schema_version") != SCHEMA_VERSION:
        die("unsupported state schema version")
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


def copy_snapshot(run_dir: Path, version_id: str, entries: list[dict[str, str]]) -> None:
    target_dir = run_dir / "versions" / version_id
    target_dir.mkdir(parents=True, exist_ok=False)
    for entry in entries:
        source = Path(entry["source_path"])
        suffix = "".join(source.suffixes)
        target = target_dir / f"{entry['label']}{suffix}"
        shutil.copy2(source, target)
        entry["snapshot_path"] = str(target.resolve())


def new_version(
    run_dir: Path,
    state: dict,
    entries: list[dict[str, str]],
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


def clearance_summary(state: dict) -> dict:
    current = get_version(state)
    latest: dict[str, dict] = {}
    for event in current["events"]:
        latest[event["examiner"]] = event
    qualifying = sorted(
        examiner
        for examiner, event in latest.items()
        if event["decision"] in CLEARANCE_DECISIONS
    )
    count = len(qualifying) if current["promoted"] else 0
    target = state["target_clearances"]
    return {
        "current_version": current["id"],
        "packet_sha256": current["packet_sha256"],
        "promoted": current["promoted"],
        "qualifying_examiner_ids": qualifying if current["promoted"] else [],
        "qualifying_clearances": count,
        "target_clearances": target,
        "success": bool(current["promoted"] and count >= target),
    }


def command_init(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).expanduser().resolve()
    if state_path(run_dir).exists():
        die(f"state already exists: {state_path(run_dir)}")
    if args.target_clearances < 2:
        die("target clearances must be at least 2")
    run_dir.mkdir(parents=True, exist_ok=True)
    entries = parse_candidates(args.candidate)
    state = {
        "schema_version": SCHEMA_VERSION,
        "created_at": utc_now(),
        "target_clearances": args.target_clearances,
        "current_version": None,
        "versions": [],
    }
    new_version(run_dir, state, entries, promoted=True)
    save_state(run_dir, state)
    print(json.dumps(clearance_summary(state), indent=2))


def command_snapshot(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).expanduser().resolve()
    state = load_state(run_dir)
    entries = parse_candidates(args.candidate)
    digest = packet_hash(entries)
    current = get_version(state)
    if digest == current["packet_sha256"]:
        if args.ground_truth and not current["promoted"]:
            current["promoted"] = True
            current["promoted_at"] = utc_now()
            current["ground_truth_files"] = entries
            save_state(run_dir, state)
        result = clearance_summary(state)
        result["snapshot_created"] = False
    else:
        version = new_version(run_dir, state, entries, promoted=args.ground_truth)
        if args.ground_truth:
            version["ground_truth_files"] = entries
        save_state(run_dir, state)
        result = clearance_summary(state)
        result["snapshot_created"] = True
    print(json.dumps(result, indent=2))


def command_record(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).expanduser().resolve()
    state = load_state(run_dir)
    version = get_version(state, args.version)
    document = Path(args.document).expanduser().resolve()
    if not document.is_file():
        die(f"record document is not a file: {document}")
    examiner = safe_name(args.examiner)
    event_number = len(version["events"]) + 1
    record_dir = run_dir / "records" / version["id"] / examiner
    record_dir.mkdir(parents=True, exist_ok=True)
    target = record_dir / f"{event_number:03d}-{safe_name(document.name)}"
    shutil.copy2(document, target)
    event = {
        "event_id": f"{version['id']}-e{event_number:03d}",
        "examiner": examiner,
        "decision": args.decision,
        "created_at": utc_now(),
        "document_sha256": sha256_file(document),
        "document_path": str(target.resolve()),
        "notes": args.notes,
    }
    version["events"].append(event)
    save_state(run_dir, state)
    result = clearance_summary(state)
    result["recorded_event"] = event
    print(json.dumps(result, indent=2))


def command_promote(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).expanduser().resolve()
    state = load_state(run_dir)
    version = get_version(state, args.version)
    if version["id"] != state["current_version"]:
        die("only the current version may be promoted")
    entries = parse_candidates(args.candidate)
    digest = packet_hash(entries)
    if digest != version["packet_sha256"]:
        die(
            "ground-truth hash does not match the examiner-cleared candidate: "
            f"expected {version['packet_sha256']}, got {digest}"
        )
    version["promoted"] = True
    version["promoted_at"] = utc_now()
    version["ground_truth_files"] = entries
    save_state(run_dir, state)
    print(json.dumps(clearance_summary(state), indent=2))


def command_status(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).expanduser().resolve()
    state = load_state(run_dir)
    result = clearance_summary(state)
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
        description="Track exact application versions and independent examiner clearances."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--run-dir", required=True)
    init_parser.add_argument("--candidate", action="append", required=True)
    init_parser.add_argument("--target-clearances", type=int, default=2)
    init_parser.set_defaults(func=command_init)

    snapshot_parser = subparsers.add_parser("snapshot")
    snapshot_parser.add_argument("--run-dir", required=True)
    snapshot_parser.add_argument("--candidate", action="append", required=True)
    snapshot_parser.add_argument(
        "--ground-truth",
        action="store_true",
        help="Mark this snapshot as already applied to the ground truth.",
    )
    snapshot_parser.set_defaults(func=command_snapshot)

    record_parser = subparsers.add_parser("record")
    record_parser.add_argument("--run-dir", required=True)
    record_parser.add_argument("--version")
    record_parser.add_argument("--examiner", required=True)
    record_parser.add_argument("--decision", choices=DECISIONS, required=True)
    record_parser.add_argument("--document", required=True)
    record_parser.add_argument("--notes", default="")
    record_parser.set_defaults(func=command_record)

    promote_parser = subparsers.add_parser("promote")
    promote_parser.add_argument("--run-dir", required=True)
    promote_parser.add_argument("--version")
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
