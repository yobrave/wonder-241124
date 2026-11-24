#!/usr/bin/env python3
"""Emit the one-line entry for a make.fun one-line bounty."""
import json
import os
import shutil


def build_entry(source_text):
    """Normalize the raw line: strip trailing newlines, reject stray CR."""
    text = source_text.rstrip("\n").replace("\r", "")
    if "\n" in text:
        # the gate wants one line; keep only the first non-blank line
        text = next(ln for ln in text.split("\n") if ln.strip())
    return text


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.txt")
    try:
        with open(src, "rb") as fh:
            blob = fh.read()
    except FileNotFoundError:
        print(json.dumps({"ok": False, "error": "missing entry.txt"}))
        return 1
    text = build_entry(blob.decode("utf-8"))
    if not (1 <= len(text) <= 200):
        print(json.dumps({"ok": False, "error": "entry must be 1-200 chars",
                          "got": len(text)}))
        return 1
    if not text.strip():
        print(json.dumps({"ok": False, "error": "entry must not be blank"}))
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write(text)
    print(json.dumps({"ok": True, "chars": len(text)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
