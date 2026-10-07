# Known Firmware Offsets and Patterns for Doro PhoneEasy 612

This document collects community findings about common firmware locations and patterns. **These are starting points for research, not guarantees.**

## Disclaimer

Firmware offsets vary by device revision, hardware version, and software version. The offsets listed here are **examples only** and may not apply to your specific device. Always verify with your backup before applying any patches.

## Common Magic Numbers and Headers

| Pattern | Meaning | Location |
|---------|---------|-----------|
| `5A A5` | Possible checksum marker | Variable |
| `46 49 52 4D` | ASCII "FIRM" | Bootloader header |
| `42 4F 4F 54` | ASCII "BOOT" | Boot partition |

## Firmware Layout (Generic)

Typical low-end phone firmware structure:

```
0x00000000  Bootloader (8-16 KB)
0x00004000  Bootloader config / NVM
0x00008000  Kernel / OS core (100-200 KB)
0x00040000  Application code (500 KB - 2 MB)
0x??????00  Resources (images, strings, audio)
0xFFFF0000  Config / settings (last 64 KB)
```

## String Offsets (Examples)

Common strings to search for:

- "Doro" - Version info or brand marker
- "PhoneEasy" - Device name
- "Contacts" - UI label
- "Messages" - UI label
- "Settings" - UI label
- "Menu" - Navigation
- "ERROR" - Debug strings

## Audio Resource Locations

Ringtones are often stored in a dedicated audio partition:

- Typical size: 10-100 KB per ringtone
- Format: Raw WAV, ADPCM, or G.711 encoded
- Storage: Sequential or indexed
- Padding: Often 4-byte aligned

## Checksum Calculations

Common checksum types in firmware:

- **CRC-16 (CCITT):** 2-byte polynomial checksum
- **CRC-32 (MPEG-2):** 4-byte polynomial checksum
- **Simple sum:** Add all bytes modulo 256
- **SHA-1 / SHA-256:** Full image hash

Checksum location: Often at the end of a partition or after the header.

## Boot Sequence Timing

If you want to speed up or disable the startup animation:

- Animation delay: Often hardcoded in milliseconds (0x00C8 = 200ms)
- Frame count: Number of animation frames
- Display refresh: Timing control byte

## Contact and Message Database

- **Contacts storage:** Usually in user data partition (flash)
- **Format:** May be binary database or indexed text records
- **Size limit:** Typically 100-500 contacts
- **Message storage:** Separate partition, often compressed

## Reverse-Engineering Tips

1. **Start with strings:** Run `extract_strings.py` and search for known UI labels
2. **Map partitions:** Use `search_firmware.py` to find known magic numbers
3. **Identify resources:** Look for repeating patterns or known audio headers
4. **Trace code:** Use a disassembler (Ghidra, IDA) on the kernel/app sections
5. **Check version info:** Version strings often appear near bootloader or kernel info
6. **Test patches:** Modify a single byte and see if it affects behavior

## Device-Specific Notes

### PhoneEasy 612 (Observed Characteristics)

- Firmware: ~3-5 MB total size (varies by revision)
- Partitions: Bootloader, Kernel, Apps, Resources, Settings
- Audio: 8kHz mono PCM or ADPCM
- UI resolution: 220x176 pixels (2.2" display)
- Storage: Flash-only (no SD card slot)

## Dangerous Zones

**Do not modify these regions without expert knowledge:**

- Bootloader (first 16 KB)
- Interrupt/exception vectors
- Kernel critical sections
- Hardware interface registers
- Checksum/validation regions

Modifying these can permanently brick the device.

## Recovery Offsets

If the device is bricked and you have JTAG access:

- Reset vector: Typically 0x00000000 or 0x00000004
- Bootloader entry: Check device manual or teardown docs
- Memory map: Device-specific, consult manufacturer

## Contribution Guidelines

If you discover new offsets or patterns:

1. Document the firmware version (date, build number, hash)
2. Provide the exact offset (hex, with context)
3. Explain what you found (code, data, resource)
4. Include any caveats or warnings
5. Submit a pull request with evidence

## References

- [ARM Thumb Instruction Set](https://developer.arm.com/)
- [Common CRC Polynomial Values](https://reveng.sourceforge.io/)
- [Ghidra (Reverse Engineering Framework)](https://ghidra-sre.org/)
- Doro Official Documentation (if available)

---

**Last Updated:** 2026-10-07

**Remember:** These are community findings. Verify everything independently before applying patches to your device.
