#!/usr/bin/env python3
"""Firmware pattern search utility for Doro PhoneEasy 612.

Searches a firmware image for byte patterns, ASCII strings, or regex matches
to locate specific code, data, or resource regions.
"""

import argparse
import re
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Search firmware for patterns.")
    parser.add_argument("--firmware", required=True, help="Firmware image to search")
    parser.add_argument("--pattern", required=True, help="Search pattern (string or regex if prefixed with 're:')")
    parser.add_argument("--output", default="search_results.txt", help="Output results file")
    parser.add_argument("--hex", action="store_true", help="Treat pattern as hex bytes")
    return parser.parse_args()


def main():
    args = parse_args()
    firmware = Path(args.firmware)

    if not firmware.exists():
        raise FileNotFoundError(f"Firmware file not found: {firmware}")

    print(f"[search] Firmware: {firmware}")
    print(f"[search] Pattern: {args.pattern}")
    print(f"[search] Hex mode: {'yes' if args.hex else 'no'}")

    data = firmware.read_bytes()
    matches = []

    if args.pattern.startswith('re:'):
        # Regex search
        pattern = args.pattern[3:]
        try:
            for match in re.finditer(pattern.encode(), data):
                matches.append((match.start(), match.group()))
        except re.error as e:
            print(f"[search] Regex error: {e}")
            return 1
    elif args.hex:
        # Hex pattern search
        pattern_bytes = bytes.fromhex(args.pattern.replace(' ', ''))
        start = 0
        while True:
            pos = data.find(pattern_bytes, start)
            if pos == -1:
                break
            matches.append((pos, pattern_bytes))
            start = pos + 1
    else:
        # ASCII string search
        pattern_bytes = args.pattern.encode()
        start = 0
        while True:
            pos = data.find(pattern_bytes, start)
            if pos == -1:
                break
            matches.append((pos, pattern_bytes))
            start = pos + 1

    print(f"[search] Found {len(matches)} match(es)")

    with open(args.output, 'w') as f:
        for offset, match_data in matches:
            f.write(f"Offset 0x{offset:08x}: {match_data}\n")

    print(f"[search] Results written to: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
