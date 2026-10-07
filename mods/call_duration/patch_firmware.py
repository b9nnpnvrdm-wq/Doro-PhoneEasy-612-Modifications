#!/usr/bin/env python3
"""Call duration format patcher for Doro PhoneEasy 612.

Modifies the firmware to display call durations in different formats or with
extended precision.
"""

import argparse
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Patch call duration display format.")
    parser.add_argument("--firmware", required=True, help="Source firmware image")
    parser.add_argument("--format", default="HH:MM:SS", help="Time format (HH:MM:SS, H:MM:SS, etc.)")
    parser.add_argument("--output", default="modified_firmware.bin", help="Output firmware image")
    return parser.parse_args()


def main():
    args = parse_args()
    firmware = Path(args.firmware)

    if not firmware.exists():
        raise FileNotFoundError(f"Firmware file not found: {firmware}")

    print(f"[call_duration] Source firmware: {firmware}")
    print(f"[call_duration] Time format: {args.format}")
    print(f"[call_duration] Output: {args.output}")
    print("[call_duration] Placeholder: find call timer display code and format string, apply new format string")
    print("[call_duration] This may require patching multiple locations if format is hardcoded in multiple places")

    return 0


if __name__ == "__main__":
    sys.exit(main())
