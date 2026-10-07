# Doro PhoneEasy 612 Tools Guide

This document explains each tool in the `scripts/` directory and how to use them together.

## Overview

The toolkit is designed to safely extract, analyze, modify, and restore firmware for the Doro PhoneEasy 612. Each tool is intentionally conservative: it validates inputs, reports errors clearly, and avoids making automatic changes to hardware.

## Scripts

### backup_firmware.py

**Purpose:** Extract the full firmware from the device via USB.

```bash
python3 scripts/backup_firmware.py --device /dev/ttyUSB0 --output backups/my_backup.bin
```

**Important:** This is a template. Real implementations require communication with the device bootloader or an OEM tool.

### analyze_firmware.py

**Purpose:** Parse and display basic metadata about a firmware image.

```bash
python3 scripts/analyze_firmware.py --firmware backups/my_backup.bin
```

This will print:
- File size
- Magic numbers or headers (if recognizable)
- Suggested next steps

### extract_strings.py

**Purpose:** Extract all ASCII strings from a firmware image to aid reverse-engineering.

```bash
python3 scripts/extract_strings.py --firmware backups/my_backup.bin --output strings.txt --min-length 5
```

This generates a text file listing every string found in the firmware. Useful for locating menu labels, error messages, and resource identifiers.

### extract_resources.py

**Purpose:** Attempt to recover embedded resources (images, audio, fonts) from a firmware dump.

```bash
python3 scripts/extract_resources.py --firmware backups/my_backup.bin -o extracted/
```

This is a placeholder that outlines the process. Real implementations depend on knowing the firmware's resource format.

### search_firmware.py

**Purpose:** Find byte patterns, strings, or regex matches in a firmware image.

```bash
# ASCII string search
python3 scripts/search_firmware.py --firmware backups/my_backup.bin --pattern "Doro" --output results.txt

# Hex pattern search
python3 scripts/search_firmware.py --firmware backups/my_backup.bin --pattern "48 8B 45" --hex --output results.txt

# Regex search
python3 scripts/search_firmware.py --firmware backups/my_backup.bin --pattern "re:[a-z]{10,}" --output results.txt
```

Outputs all matching offsets and context.

### hex_patcher.py

**Purpose:** Apply direct hex byte patches to a firmware image at specific offsets.

```bash
python3 scripts/hex_patcher.py --firmware backups/my_backup.bin --offset 0x1000 --patch "90 90 90" --output patched.bin
```

Use this to:
- NOP out instructions
- Modify data table entries
- Patch bytes in resource regions

**Warning:** Always verify the offset is correct before patching.

### checksum_tool.py

**Purpose:** Compute or verify firmware checksums.

```bash
# Compute SHA256 hash
python3 scripts/checksum_tool.py --firmware backups/my_backup.bin

# Recalculate (for a modified file)
python3 scripts/checksum_tool.py --firmware patched.bin --recalculate
```

Many firmware formats embed checksums. After modifying a firmware, you may need to recalculate embedded checksums in addition to verifying the file integrity.

### restore_firmware.py

**Purpose:** Flash a modified firmware image back to the device.

```bash
python3 scripts/restore_firmware.py --device /dev/ttyUSB0 --firmware patched.bin
```

**Critical:** This is also a template. Real implementations must:
1. Verify device identity
2. Validate firmware integrity
3. Ensure device is in bootloader mode
4. Handle communication timeouts and errors
5. Implement progress feedback

### firmware_compiler.py

**Purpose:** Reassemble extracted firmware components into a complete image.

```bash
python3 scripts/firmware_compiler.py --components-dir extracted/ --output rebuilt.bin --recalculate-checksums
```

Useful when you've modified individual components and need to rebuild the full firmware.

## Typical Workflow

1. **Backup:** Extract the original firmware
   ```bash
   python3 scripts/backup_firmware.py --device /dev/ttyUSB0 --output backups/original.bin
   ```

2. **Analyze:** Understand the firmware structure
   ```bash
   python3 scripts/analyze_firmware.py --firmware backups/original.bin
   ```

3. **Extract:** Pull out resources and strings
   ```bash
   python3 scripts/extract_strings.py --firmware backups/original.bin --output strings.txt
   python3 scripts/extract_resources.py --firmware backups/original.bin -o extracted/
   ```

4. **Search:** Locate specific data or code
   ```bash
   python3 scripts/search_firmware.py --firmware backups/original.bin --pattern "Menu" --output menu_offsets.txt
   ```

5. **Modify:** Apply patches or use mod scripts
   ```bash
   python3 scripts/hex_patcher.py --firmware backups/original.bin --offset 0x1234 --patch "00 00" --output patched.bin
   # OR
   python3 mods/custom_ringtones/replace_ringtone.py --firmware backups/original.bin --new-audio tone.wav --output patched.bin
   ```

6. **Verify:** Check integrity
   ```bash
   python3 scripts/checksum_tool.py --firmware patched.bin --recalculate
   ```

7. **Test (optional):** Try in a simulator or test device

8. **Restore:** Flash to the device
   ```bash
   python3 scripts/restore_firmware.py --device /dev/ttyUSB0 --firmware patched.bin
   ```

## Safety Tips

- Always keep the original backup in a safe location
- Test modifications on a copy before flashing to the real device
- Never interrupt a restore operation
- Verify checksums match expected values after editing
- Keep a log of every modification for troubleshooting
- Document the exact firmware version you tested on

## Limitations

These tools are educational and exploratory. Real firmware modification often requires:

- Binary disassembler (IDA Pro, Ghidra)
- Device-specific bootloader documentation
- Manufacturer communication protocols
- Deep understanding of ARM assembly or the device's CPU
- A way to recover a bricked device (JTAG, manufacturer tools)

## Next Steps

After familiarizing yourself with the tools, explore:

1. Firmware format documentation (if available)
2. Partition layout and headers
3. Resource containers and compression
4. Code sections and entry points
5. Boot sequence and initialization code

Good luck, and remember: **always have a working backup before modifying hardware.**
