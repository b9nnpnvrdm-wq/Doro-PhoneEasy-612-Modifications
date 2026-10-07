# Doro PhoneEasy 612 Modding Guide

A comprehensive collection of modifications, hacks, and customizations for the Doro PhoneEasy 612 flip phone.

## Table of Contents

- [Overview](#overview)
- [Device Info](#device-info)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Modifications](#modifications)
- [Firmware Tools](#firmware-tools)
- [Backup & Recovery](#backup--recovery)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Safety Disclaimer](#safety-disclaimer)

## Overview

The Doro PhoneEasy 612 is a senior-friendly flip phone with limited pre-installed apps and a focus on simplicity. This repository contains modifications, firmware tweaks, and hacks to extend functionality and customize the device.

## Device Info

**Doro PhoneEasy 612 Specifications:**
- **Form Factor:** Flip phone
- **Display:** 2.2" QVGA (220 x 176 pixels)
- **OS:** Proprietary Doro OS (embedded firmware)
- **Memory:** ~20MB RAM
- **Storage:** ~40MB Flash
- **Connectivity:** GSM/GPRS, no 3G/4G
- **Pre-installed Apps:** Limited (calling, messaging, contacts, basic tools)
- **Processor:** ARM-based (low-power)

**Important:** This device does NOT have developer mode, an "About" settings section, or traditional Android-style debugging. Modifications require direct firmware-level changes via USB connection and binary editing.

## Prerequisites

Before attempting any modifications, you'll need:

- **USB data cable** (Micro-USB or proprietary Doro connector)
- **A PC/Mac with USB port**
- **Firmware extraction tools**
- **Full firmware backup** (CRITICAL - do this first!)
- **Hexadecimal editor** (for firmware patching)
- **Patience and attention to detail**
- **Understanding of firmware structure** and binary editing

## Getting Started

### 1. Backup Your Phone (ESSENTIAL)

Before any modification, extract the full firmware via USB:

```bash
# Connect phone via USB
python3 scripts/backup_firmware.py --device /dev/ttyUSB0 --output backups/phoneeasy_612_original.bin
```

**Save this file in multiple locations.** If something goes wrong, this is your only recovery path.

### 2. Analyze Firmware Structure

```bash
python3 scripts/analyze_firmware.py --firmware backups/phoneeasy_612_original.bin
```

This will identify:
- Firmware version
- Partition layout
- Bootloader info
- Checksums

### 3. Extract Strings & Resources

```bash
python3 scripts/extract_strings.py --firmware backups/phoneeasy_612_original.bin --output firmware_strings.txt
python3 scripts/extract_resources.py --firmware backups/phoneeasy_612_original.bin --output extracted/
```

## Modifications

### Mod 1: Replace Ringtones

Extract the firmware, find the audio storage partition, and replace `.wav` files with custom ringtones.

📄 **File:** `mods/custom_ringtones/`

```bash
python3 mods/custom_ringtones/replace_ringtone.py \
  --firmware backups/phoneeasy_612_original.bin \
  --ringtone-name "default" \
  --new-audio ringtones/my_sound.wav \
  --output modified_firmware.bin
```

**Supported formats:** WAV (8-bit PCM, 8kHz), max 100KB per ringtone

### Mod 2: Change Startup Animation

Modify boot sequence graphics and timing.

📄 **File:** `mods/startup_animation/`

```bash
python3 mods/startup_animation/patch_boot.py \
  --firmware backups/phoneeasy_612_original.bin \
  --skip-animation \
  --output modified_firmware.bin
```

### Mod 3: Modify Text/UI Strings

Customize menu text, button labels, and UI strings.

📄 **File:** `mods/ui_strings/`

```bash
python3 mods/ui_strings/patch_strings.py \
  --firmware backups/phoneeasy_612_original.bin \
  --strings-file custom_strings.txt \
  --output modified_firmware.bin
```

Example `custom_strings.txt`:
```text
"Contacts" -> "My People"
"Messages" -> "Texts"
"Settings" -> "Options"
```

### Mod 4: Extend Call Time Display

Modify firmware to show longer call durations or custom time formats.

📄 **File:** `mods/call_duration/`

```bash
python3 mods/call_duration/patch_firmware.py \
  --firmware backups/phoneeasy_612_original.bin \
  --format "HH:MM:SS" \
  --output modified_firmware.bin
```

### Mod 5: Unlock Service Menu

Access hidden diagnostics menu via key combination:

📄 **File:** `mods/service_menu/`

```bash
python3 mods/service_menu/unlock.py --firmware backups/phoneeasy_612_original.bin
```

*(Requires firmware analysis to locate menu code)*

## Firmware Tools

### Core Scripts

| Script | Purpose |
|--------|---------|
| `scripts/backup_firmware.py` | Extract full firmware via USB |
| `scripts/restore_firmware.py` | Flash modified firmware back to phone |
| `scripts/analyze_firmware.py` | Parse firmware structure and partitions |
| `scripts/extract_strings.py` | Extract UI text strings |
| `scripts/extract_resources.py` | Extract images, sounds, data |
| `scripts/hex_patcher.py` | Low-level hex editing |
| `scripts/checksum_tool.py` | Verify/recalculate checksums |
| `scripts/firmware_compiler.py` | Rebuild firmware from components |

### Basic Workflow

```bash
# 1. Backup
python3 scripts/backup_firmware.py --device /dev/ttyUSB0 -o backup.bin

# 2. Analyze
python3 scripts/analyze_firmware.py --firmware backup.bin

# 3. Extract resources
python3 scripts/extract_resources.py --firmware backup.bin -o extracted/

# 4. Modify (using mod scripts)
python3 mods/custom_ringtones/replace_ringtone.py --firmware backup.bin ...

# 5. Verify checksum
python3 scripts/checksum_tool.py --firmware modified.bin --recalculate

# 6. Restore to phone
python3 scripts/restore_firmware.py --device /dev/ttyUSB0 --firmware modified.bin
```

## Backup & Recovery

### Creating a Full Backup

```bash
# Connect phone via USB in normal mode
python3 scripts/backup_firmware.py \
  --device /dev/ttyUSB0 \
  --output backups/phoneeasy_612_backup_$(date +%Y%m%d_%H%M%S).bin
```

Store backups in multiple locations (USB drive, cloud, external drive).

### Restoring from Backup

```bash
# If phone is still responsive
python3 scripts/restore_firmware.py \
  --device /dev/ttyUSB0 \
  --firmware backups/phoneeasy_612_backup.bin
```

### Factory Reset (Hard Reset)

If phone is completely stuck:

1. Power off completely
2. Remove battery for 30 seconds (if removable)
3. Reinsert battery and power on
4. If still stuck, attempt USB restore with backup firmware

## Troubleshooting

### Phone Won't Connect via USB

- Check USB cable (try different cable or original cable)
- Install USB drivers for Doro device
- Try different USB port on computer
- Restart phone and try again
- Check if phone charges (verifies USB connection works)

### Firmware Checksum Mismatch

```bash
# Recalculate and fix checksum
python3 scripts/checksum_tool.py --firmware modified.bin --recalculate --output fixed.bin
```

### Modification Won't Flash

- Verify firmware file size matches original
- Check checksum is correct
- Ensure backup is intact before attempting restore
- Try flashing original backup first to verify process works

### Phone Stuck in Boot Loop

1. Connect via USB
2. Attempt to restore original backup
3. If that fails, seek technical support
4. Consider JTAG recovery (advanced method)

### Can't Find Specific Firmware Offset

Use `scripts/search_firmware.py` to find patterns:

```bash
python3 scripts/search_firmware.py \
  --firmware backup.bin \
  --pattern "Doro" \
  --output results.txt
```

## Resources

- [Doro PhoneEasy 612 Manual](https://www.doro.com/)
- [GSMArena Device Database](https://www.gsmarena.com/)
- [Firmware Reverse Engineering Basics](docs/firmware_basics.md)
- [Binary Analysis Tools Guide](docs/tools_guide.md)
- [Known Firmware Offsets](docs/known_offsets.md)

## Safety Disclaimer

⚠️ **IMPORTANT - READ THIS FIRST:**

- **Modifying your phone will void the warranty.**
- **Incorrect firmware modifications can permanently brick your device.**
- **You may lose all contacts, messages, and settings.**
- **Always backup before any modification attempt.**
- **Use at your own risk.** The authors are not responsible for bricked or damaged devices.
- **Do not interrupt flashing** — loss of power during restore can permanently damage the device.
- **This is not supported by Doro** — you're on your own if something goes wrong.

By using this repository and its tools, you fully acknowledge these risks and agree to assume all responsibility for any outcomes.

## Contributing

Found a new mod, offset, or improvement? Contribute to the project:

1. Test your modification thoroughly
2. Document the exact steps and firmware version tested
3. Include before/after comparisons
4. Provide backup/recovery instructions
5. Submit a pull request with clear details

## File Structure

```text
.
├── README.md
├── LICENSE
├── scripts/
│   ├── backup_firmware.py
│   ├── restore_firmware.py
│   ├── analyze_firmware.py
│   ├── extract_strings.py
│   ├── extract_resources.py
│   ├── hex_patcher.py
│   ├── checksum_tool.py
│   └── search_firmware.py
├── mods/
│   ├── custom_ringtones/
│   ├── startup_animation/
│   ├── ui_strings/
│   ├── call_duration/
│   └── service_menu/
├── docs/
│   ├── firmware_basics.md
│   ├── tools_guide.md
│   └── known_offsets.md
├── backups/
│   └── .gitkeep
└── extracted/
    └── .gitkeep
```

## License

MIT License - See LICENSE file for details.

---

**Last Updated:** 2026-10-07  
**Device:** Doro PhoneEasy 612 (Flip Phone)  
**Community Contributions Welcome**
