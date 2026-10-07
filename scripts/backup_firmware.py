#!/usr/bin/env python3
"""Backup script for a low-end Doro phone firmware image.

This is a lightweight starter utility meant to model a safe firmware backup flow.
It does not access real hardware by itself; it is intended as a template for a
more complete implementation.
"""

import argparse
import os
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Backup Doro PhoneEasy 612 firmware image.")
    parser.add_argument("--device", default="/dev/ttyUSB0", help="USB device path or OEM connection target")
    parser.add_argument("--output", default="backups/firmware_backup.bin", help="Output firmware image path")
    parser.add_argument("--include-nvm", action="store_true", help="Include non-volatile memory region")
    return parser.parse_args()


def main():
    args = parse_args()
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print("[backup] Starting firmware backup")
    print(f"[backup] Device target: {args.device}")
    print(f"[backup] Output: {out_path}")
    print(f"[backup] Include NVM: {'yes' if args.include_nvm else 'no'}")

    # Placeholder: real implementation would talk to the phone and write a binary dump.
    # For safety, do not fabricate a valid firmware image here.
    print("[backup] This is a starter template. Connect your device and replace the placeholder logic with your actual extraction flow.")
    print("[backup] IMPORTANT: Keep a copy of the original firmware before experimenting.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
