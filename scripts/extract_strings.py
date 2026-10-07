#!/usr/bin/env python3
"""Firmware string extraction utility for Doro PhoneEasy 612.

Extracts all human-readable ASCII and Unicode strings from a firmware image
to aid in reverse-engineering and locating modifiable text resources.
"""

import argparse
import sys
from pathlib import Path


def extract_strings(data, min_length=4):
    """Extract ASCII and Unicode strings from binary data."""
    strings = []
    current = b""
    for byte in data:
        if 32 <= byte <= 126:
            current += bytes([byte])
        else:
            if len(current) >= min_length:
                try:
                    strings.append(current.decode('ascii'))
                except:
                    pass
            current = b""
    return strings


def parse_args():
    parser = argparse.ArgumentParser(description="Extract strings from Doro firmware.")
    parser.add_argument("--firmware", required=True, help="Firmware image to analyze")
    parser.add_argument("--output", default="strings.txt", help="Output file")
    parser.add_argument("--min-length", type=int, default=4, help="Minimum string length to extract")
    return parser.parse_args()


def main():
    args = parse_args()
    firmware = Path(args.firmware)
    output = Path(args.output)

    if not firmware.exists():
        raise FileNotFoundError(f"Firmware file not found: {firmware}")

    print(f"[extract_strings] Reading firmware: {firmware}")
    data = firmware.read_bytes()
    print(f"[extract_strings] Firmware size: {len(data)} bytes")

    strings = extract_strings(data, args.min_length)
    print(f"[extract_strings] Found {len(strings)} strings")

    with open(output, 'w') as f:
        for s in strings:
            f.write(s + '\n')

    print(f"[extract_strings] Wrote to: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
