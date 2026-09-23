#!/usr/bin/env python3
"""Settings and session history for cv-refresh.

Where personal data lives (first match wins):
  1. $CV_REFRESH_HOME
  2. <skill dir>/user-data            (Claude Code: persistent, git-ignored)
  3. /tmp/cv-refresh-user-data        (claude.ai: skill dir is read-only; the
                                       data is exported as a zip at the end and
                                       re-imported when the user uploads it)
  4. ~/.cv-refresh

Commands (all print JSON):
  init                      resolve data dir, import uploaded data, report state
  get                       print settings
  set KEY VALUE             update a setting (layout_mode: preserve|choose)
  save-session FILE [--label L]   store a session history markdown file
  history [--limit N]       list previous sessions (newest first)
  export [--out PATH]       zip the data dir (used on claude.ai)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import SKILL_DIR, emit, fail, skill_version  # noqa: E402

EXPORT_NAME = "cv-refresh-user-data.zip"
CLAUDE_AI_UPLOADS = Path("/mnt/user-data/uploads")
CLAUDE_AI_OUTPUTS = Path("/mnt/user-data/outputs")
ALLOWED_SETTINGS = {
    "layout_mode": {"preserve", "choose"},
    "last_template": {"mirror", "classic", "modern", "compact"},
}


def _writable(directory: Path) -> bool:
    try:
        directory.mkdir(parents=True, exist_ok=True)
        probe = directory / ".write-test"
        probe.write_text("ok")
        probe.unlink()
        return True
    except OSError:
        return False


def resolve_data_dir() -> tuple[Path, bool, str]:
    """Return (data_dir, persistent, host_hint)."""
    env = os.environ.get("CV_REFRESH_HOME")
    if env:
        return Path(env).expanduser(), True, "custom"
    on_claude_ai = CLAUDE_AI_OUTPUTS.parent.exists()
    local = SKILL_DIR / "user-data"
    if not on_claude_ai and _writable(local):
        return local, True, "claude-code"
    if on_claude_ai:
        tmp = Path("/tmp/cv-refresh-user-data")
        tmp.mkdir(parents=True, exist_ok=True)
        return tmp, False, "claude-ai"
    home = Path.home() / ".cv-refresh"
    home.mkdir(parents=True, exist_ok=True)
    return home, True, "unknown"


def settings_path(data_dir: Path) -> Path:
    return data_dir / "settings.json"


def read_settings(data_dir: Path) -> dict | None:
    path = settings_path(data_dir)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def write_settings(data_dir: Path, settings: dict) -> None:
    settings["schema_version"] = 1
    settings["updated"] = dt.datetime.now().isoformat(timespec="seconds")
    settings.setdefault("created", settings["updated"])
    settings_path(data_dir).write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")


def sessions_dir(data_dir: Path) -> Path:
    d = data_dir / "history" / "sessions"
    d.mkdir(parents=True, exist_ok=True)
    return d


def parse_header(path: Path) -> dict:
    """Read the simple `key: value` block between the first two '---' lines."""
    meta: dict = {"file": str(path)}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return meta
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()
    return meta


def list_sessions(data_dir: Path, limit: int | None = None) -> list[dict]:
    files = sorted(sessions_dir(data_dir).glob("*.md"), reverse=True)
    if limit:
        files = files[:limit]
    return [parse_header(f) for f in files]


def import_uploaded(data_dir: Path) -> list[str]:
    """claude.ai: restore data from an uploaded export zip or loose files."""
    imported: list[str] = []
    if not CLAUDE_AI_UPLOADS.exists():
        return imported
    for zpath in sorted(CLAUDE_AI_UPLOADS.glob("cv-refresh-user-data*.zip")):
        with zipfile.ZipFile(zpath) as zf:
            for member in zf.namelist():
                target = (data_dir / member).resolve()
                if not str(target).startswith(str(data_dir.resolve())) or member.endswith("/"):
                    continue  # skip directories and anything escaping the data dir
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zf.read(member))
                imported.append(member)
    loose_settings = CLAUDE_AI_UPLOADS / "settings.json"
    if loose_settings.exists() and not settings_path(data_dir).exists():
        shutil.copy(loose_settings, settings_path(data_dir))
        imported.append("settings.json")
    return imported


def cmd_init(_args) -> None:
    data_dir, persistent, host = resolve_data_dir()
    imported = import_uploaded(data_dir) if host == "claude-ai" else []
    work_dir = data_dir / "work" / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    work_dir.mkdir(parents=True, exist_ok=True)
    settings = read_settings(data_dir)
    emit({
        "ok": True,
        "skill_version": skill_version(),
        "skill_dir": str(SKILL_DIR),
        "data_dir": str(data_dir),
        "work_dir": str(work_dir),
        "persistent": persistent,
        "host_hint": host,
        "imported": imported,
        "settings": settings,
        "needs_layout_question": not (settings and settings.get("layout_mode") in ALLOWED_SETTINGS["layout_mode"]),
        "sessions": list_sessions(data_dir, limit=10),
    })


def cmd_get(_args) -> None:
    data_dir, _, _ = resolve_data_dir()
    emit({"ok": True, "settings": read_settings(data_dir) or {}})


def cmd_set(args) -> None:
    key, value = args.key, args.value
    if key not in ALLOWED_SETTINGS:
        fail(f"Unknown setting '{key}'", allowed=sorted(ALLOWED_SETTINGS))
    if value not in ALLOWED_SETTINGS[key]:
        fail(f"Invalid value '{value}' for {key}", allowed=sorted(ALLOWED_SETTINGS[key]))
    data_dir, persistent, _ = resolve_data_dir()
    settings = read_settings(data_dir) or {}
    settings[key] = value
    write_settings(data_dir, settings)
    emit({"ok": True, "settings": settings, "path": str(settings_path(data_dir)), "persistent": persistent})


def _slug(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return text[:60] or "session"


def cmd_save_session(args) -> None:
    src = Path(args.file)
    if not src.exists():
        fail(f"File not found: {src}")
    data_dir, persistent, host = resolve_data_dir()
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = args.label or parse_header(src).get("target", "session")
    dest = sessions_dir(data_dir) / f"{stamp}_{_slug(label)}.md"
    shutil.copy(src, dest)
    emit({"ok": True, "saved": str(dest), "persistent": persistent,
          "next_step": None if persistent else "Run `state.py export` and give the zip to the user."})


def cmd_history(args) -> None:
    data_dir, _, _ = resolve_data_dir()
    emit({"ok": True, "sessions": list_sessions(data_dir, limit=args.limit)})


def cmd_export(args) -> None:
    data_dir, _, host = resolve_data_dir()
    default = CLAUDE_AI_OUTPUTS / EXPORT_NAME if CLAUDE_AI_OUTPUTS.exists() else Path.cwd() / EXPORT_NAME
    out = Path(args.out) if args.out else default
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(data_dir.rglob("*")):
            rel = path.relative_to(data_dir)
            if path.is_dir() or rel.parts[0] == "work":
                continue  # work files are scratch; only settings + history travel
            zf.write(path, rel.as_posix())
            count += 1
    emit({"ok": True, "export": str(out), "files": count})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init").set_defaults(func=cmd_init)
    sub.add_parser("get").set_defaults(func=cmd_get)
    p_set = sub.add_parser("set")
    p_set.add_argument("key")
    p_set.add_argument("value")
    p_set.set_defaults(func=cmd_set)
    p_save = sub.add_parser("save-session")
    p_save.add_argument("file")
    p_save.add_argument("--label")
    p_save.set_defaults(func=cmd_save_session)
    p_hist = sub.add_parser("history")
    p_hist.add_argument("--limit", type=int)
    p_hist.set_defaults(func=cmd_history)
    p_exp = sub.add_parser("export")
    p_exp.add_argument("--out")
    p_exp.set_defaults(func=cmd_export)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
