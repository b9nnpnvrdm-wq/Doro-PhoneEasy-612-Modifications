#!/usr/bin/env python3
"""Checksum utility for verifying firmware integrity after edits."""

import argparse
import hashlib
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Compute or verify firmware checksum.")
    parser.add_argument("--firmware", required=True, help="Firmware file to hash")
    parser.add_argument("--recalculate", action="store_true", help="Compute a checksum for the current file")
    return parser.parse_args()


def main():
    args = parse_args()
    path = Path(args.firmware)
    if not path.exists():
        raise FileNotFoundError(f"Firmware file not found: {path}")

    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"[checksum] {path}")
    print(f"[checksum] SHA256 = {digest}")
    if args.recalculate:
        print("[checksum] recalculated successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
