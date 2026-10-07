#!/usr/bin/env python3
"""UI string patcher for Doro PhoneEasy 612.

This script replaces menu labels, button text, and other UI strings in the firmware
by identifying and modifying the firmware's string table regions.
"""

import argparse
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Patch UI strings in Doro firmware.")
    parser.add_argument("--firmware", required=True, help="Source firmware image")
    parser.add_argument("--strings-file", required=True, help="Text file with string replacements (format: 'old' -> 'new')")
    parser.add_argument("--output", default="modified_firmware.bin", help="Output firmware image")
    return parser.parse_args()


def parse_strings_file(path):
    """Parse simple string replacement file."""
    replacements = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ' -> ' in line:
                old, new = line.split(' -> ', 1)
                replacements[old.strip().strip('"')] = new.strip().strip('"')
    return replacements


def main():
    args = parse_args()
    firmware = Path(args.firmware)
    strings_path = Path(args.strings_file)

    if not firmware.exists():
        raise FileNotFoundError(f"Firmware file not found: {firmware}")
    if not strings_path.exists():
        raise FileNotFoundError(f"Strings file not found: {strings_path}")

    replacements = parse_strings_file(strings_path)

    print(f"[ui_strings] Source firmware: {firmware}")
    print(f"[ui_strings] Strings file: {strings_path}")
    print(f"[ui_strings] Output: {args.output}")
    print(f"[ui_strings] Replacement count: {len(replacements)}")
    for old, new in list(replacements.items())[:5]:
        print(f"  '{old}' -> '{new}'")
    if len(replacements) > 5:
        print(f"  ... and {len(replacements) - 5} more")
    print("[ui_strings] Placeholder: locate string table in firmware, apply replacements, pad to original size")
    print("[ui_strings] String lengths must match or padding strategy must be defined")

    return 0


if __name__ == "__main__":
    sys.exit(main())
