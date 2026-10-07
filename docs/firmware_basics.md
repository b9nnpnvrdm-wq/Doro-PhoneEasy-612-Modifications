# Doro PhoneEasy 612 Firmware Basics

This document describes the general approach used in a low-end, locked-down flip phone project.

## Important reality check

The Doro PhoneEasy 612 is not an Android-style device with a standard SDK, developer menu, or ADB access. It is a feature phone with a proprietary operating system. That means modifications are usually done at the firmware level instead of at the app level.

## Common research workflow

1. Back up the original firmware.
2. Identify the firmware image type, partitions, and compression format.
3. Extract resources such as fonts, audio, graphics, and text strings.
4. Identify the module that owns the UI strings and boot sequence.
5. Patch the resource or data block in a controlled way.
6. Recalculate checksums and validate the result.
7. Restore carefully, ideally only after testing on a backup copy.

## What to look for

Typical firmware areas to inspect include:

- UI string tables
- ringtone and message tone packs
- startup graphics and boot animation blocks
- menu label resources
- contact and message storage areas

## Safety rules

- Keep the original firmware image untouched.
- Work from copies, not live files.
- Record every change.
- Verify checksums before and after edits.
- Never interrupt a firmware restore.

## Recommended structure for a modding repo

- `scripts/` for backup, restore, checksum, and extract utilities
- `mods/` for transformation scripts and experiments
- `docs/` for notes and findings
- `backups/` for known-good firmware dumps
- `extracted/` for resource dumps

## Practical note

Because the device is locked down, a lot of “modding” in practice is really reverse-engineering the firmware package and replacing resources or adjusting small data tables.

That is realistic, but it is also high-risk. Treat every modification as experimental until it is validated.
