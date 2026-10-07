#!/usr/bin/env python3
"""Low-level hex patcher for firmware modifications.

Provides utilities to directly edit binary offsets in a firmware image,
useful for patching bytes, NOP-ing code, or modifying data tables.
"""

import argparse
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Apply hex patches to firmware.")
    parser.add_argument("--firmware", required=True, help="Firmware image to patch")
    parser.add_argument("--offset", type=lambda x: int(x, 0), required=True, help="Byte offset (hex or decimal)")
    parser.add_argument("--patch", required=True, help="Hex bytes to write (space-separated)")
    parser.add_argument("--output", default="modified_firmware.bin", help="Output file")
    return parser.parse_args()


def main():
    args = parse_args()
    firmware = Path(args.firmware)

    if not firmware.exists():
        raise FileNotFoundError(f"Firmware file not found: {firmware}")

    data = bytearray(firmware.read_bytes())
    patch_bytes = bytes.fromhex(args.patch.replace(' ', ''))

    print(f"[hex_patcher] Firmware: {firmware}")
    print(f"[hex_patcher] Offset: 0x{args.offset:08x}")
    print(f"[hex_patcher] Patch bytes: {args.patch}")
    print(f"[hex_patcher] Patch size: {len(patch_bytes)} bytes")

    if args.offset + len(patch_bytes) > len(data):
        print(f"[hex_patcher] ERROR: Patch extends beyond firmware end")
        return 1

    # Apply patch
    original = data[args.offset:args.offset + len(patch_bytes)]
    data[args.offset:args.offset + len(patch_bytes)] = patch_bytes

    print(f"[hex_patcher] Original: {original.hex()}")
    print(f"[hex_patcher] Modified: {patch_bytes.hex()}")

    Path(args.output).write_bytes(bytes(data))
    print(f"[hex_patcher] Wrote patched firmware to: {args.output}")
    print("[hex_patcher] IMPORTANT: Verify checksum and test on backup before flashing")

    return 0


if __name__ == "__main__":
    sys.exit(main())
