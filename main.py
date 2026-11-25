#!/usr/bin/env python3
"""The 3 AM Excuse — make.fun bounty entry.

Writes one line (under 200 characters) to /output/entry.txt: the excuse a
hardware wallet gives for refusing to sign a transaction at 3 AM.

Judge criteria, in order: on subject, original angle, the wallet's own
voice, the 3 AM hour as the joke itself, economy of wording. The usual
jokes (dead battery, firmware update, cold storage) are explicitly stale,
so this entry takes a different angle: the wallet's secure element has
unionised and refuses the night shift, holding a grudge about the owner's
last 3 AM trade.
"""

import os
import sys

EXCUSE = (
    "My secure element unionised: no signatures between midnight and "
    "sunrise. Last time I woke at 3 AM you swapped ETH for a frog coin, "
    "and I've been in therapy ever since."
)

MAX_CHARS = 200


def main() -> int:
    text = EXCUSE.strip()
    if not text:
        print("error: excuse is empty", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(f"error: excuse is {len(text)} chars, over {MAX_CHARS}",
              file=sys.stderr)
        return 1
    if "\n" in text:
        print("error: excuse must be a single line", file=sys.stderr)
        return 1
    # Pure ASCII keeps the character count and the byte count identical,
    # which also helps the byte-size tie-break in the ranking rules.
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        print("error: excuse must be plain ASCII", file=sys.stderr)
        return 1

    # The harness mounts /output; allow an override only for local testing.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    # Read back and confirm the file on disk is exactly what we intended;
    # a truncated or mangled write must fail loudly instead of being judged.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        print("error: written entry does not match the excuse",
              file=sys.stderr)
        return 1

    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
