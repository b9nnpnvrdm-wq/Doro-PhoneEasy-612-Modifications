#!/usr/bin/env python3
"""Restore a known-good firmware image to the Doro PhoneEasy 612.

This is intentionally a template. Real implementations must validate checksums and
confirm the device can safely accept an image before writing.
"""

import argparse
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Restore a firmware image to the device.")
    parser.add_argument("--device", default="/dev/ttyUSB0", help="USB device path or OEM target")
    parser.add_argument("--firmware", required=True, help="Firmware file to flash")
    parser.add_argument("--force", action="store_true", help="Ignore non-fatal validation warnings")
    return parser.parse_args()


def main():
    args = parse_args()
    firmware = Path(args.firmware)
    if not firmware.exists():
        raise FileNotFoundError(f"Firmware file not found: {firmware}")

    print(f"[restore] Firmware file: {firmware}")
    print(f"[restore] Device target: {args.device}")
    print("[restore] Placeholder logic. Replace with a verified flashing routine before use.")
    print("[restore] Always start from a known-good backup before attempting any restore.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
