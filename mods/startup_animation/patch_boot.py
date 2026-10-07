#!/usr/bin/env python3
"""Startup animation patcher for Doro PhoneEasy 612.

This script modifies the boot sequence by patching firmware regions that control
the startup animation timing and graphics display.
"""

import argparse
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Patch startup animation in Doro firmware.")
    parser.add_argument("--firmware", required=True, help="Source firmware image")
    parser.add_argument("--skip-animation", action="store_true", help="Disable startup animation")
    parser.add_argument("--speed-up", type=int, help="Speed up animation (milliseconds per frame)")
    parser.add_argument("--output", default="modified_firmware.bin", help="Output firmware image")
    return parser.parse_args()


def main():
    args = parse_args()
    firmware = Path(args.firmware)

    if not firmware.exists():
        raise FileNotFoundError(f"Firmware file not found: {firmware}")

    print(f"[startup] Source firmware: {firmware}")
    print(f"[startup] Output: {args.output}")
    print(f"[startup] Skip animation: {'yes' if args.skip_animation else 'no'}")
    if args.speed_up:
        print(f"[startup] Frame speed: {args.speed_up}ms")
    print("[startup] Placeholder: locate boot animation binary block and modify animation control bytes")
    print("[startup] Remember to recalculate firmware checksums after modification")

    return 0


if __name__ == "__main__":
    sys.exit(main())
