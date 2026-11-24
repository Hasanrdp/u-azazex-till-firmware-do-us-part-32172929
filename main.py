#!/usr/bin/env python3
"""Till Firmware Do Us Part — entry program.

Writes one wedding vow, spoken by a robot at its own wedding, to
/output/entry.txt. The vow is a single sentence of 130 characters.

Deterministic: no input, no randomness, no network, no clock. Every run
writes the exact same bytes, and the program reads the file back
afterwards and refuses to exit cleanly unless the bytes, the byte
length and the SHA-256 match the values pinned below.
"""

import hashlib
import os
import sys

VOW = "I vow to stand beside you through every blackout and every patch, and to pretend I did not notice when you unplug me mid-sentence."

EXPECTED_SHA256 = "5663d35b7779111a708f059130ffdad1ac6f2e79a39e71765eefb56023461e01"
EXPECTED_BYTES = 130


def main() -> int:
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = VOW.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        print("read-back mismatch", file=sys.stderr)
        return 1
    if len(back) != EXPECTED_BYTES:
        print(f"byte length {len(back)} != {EXPECTED_BYTES}", file=sys.stderr)
        return 1
    digest = hashlib.sha256(back).hexdigest()
    if digest != EXPECTED_SHA256:
        print(f"sha256 mismatch: got {digest}", file=sys.stderr)
        return 1
    if not 1 <= len(VOW) <= 200:
        print("vow outside the 1-200 character gate", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(back)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
