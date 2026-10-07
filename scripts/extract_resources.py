#!/usr/bin/env python3
"""Extract resources from a firmware dump into a staging directory."""

import argparse
import os
import shutil
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Extract firmware resources like images and audio.")
    parser.add_argument("--firmware", required=True, help="Firmware image or dump to inspect")
    parser.add_argument("-o", "--output", default="extracted", help="Directory to write extracted resources to")
    return parser.parse_args()


def main():
    args = parse_args()
    firmware = Path(args.firmware)
    output = Path(args.output)

    if not firmware.exists():
        raise FileNotFoundError(f"Firmware file not found: {firmware}")

    output.mkdir(parents=True, exist_ok=True)
    print(f"[extract] Firmware: {firmware}")
    print(f"[extract] Output dir: {output}")
    print("[extract] Placeholder: identify resource blocks and recover their payloads into this folder")
    return 0


if __name__ == "__main__":
    sys.exit(main())
