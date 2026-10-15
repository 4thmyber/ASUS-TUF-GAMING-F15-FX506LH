# Runbook

## Install / replace the EFI
1. Test first from USB: format a stick as MS-DOS (FAT32), GUID, copy `EFI/` to its root, boot with **F8**.
2. Passed the [boot-test checklist](#boot-test-checklist) → install to the internal ESP:
   ```bash
   sudo diskutil list                    # find the ESP of the macOS disk (e.g. disk0s1)
   sudo diskutil mount disk0s1
   cp -R /Volumes/EFI/EFI ~/EFI-backup-$(date +%F)   # rollback copy
   rsync -a --delete EFI/ /Volumes/EFI/EFI/
   diskutil unmount disk0s1
   ```
3. Rollback: boot the known-good USB, copy `~/EFI-backup-*` back the same way.

## Boot-test checklist
Run after every EFI change, booted from USB first. Always do the first three.
- [ ] Reaches desktop; no panic in `log show --last boot --predicate 'eventMessage contains "panic"'`
- [ ] Sleep/wake (lid + Apple menu), 2 cycles
- [ ] Reboot + shutdown complete without hang
- [ ] Audio: speakers, headphone jack, internal mic
- [ ] Wi-Fi (HeliPort connects) · Ethernet
- [ ] Trackpad gestures · keyboard backlight/brightness keys
- [ ] Battery % updates · display brightness slider
- [ ] Both NVMe drives visible · USB-A and USB-C ports
- [ ] Recovery boots from the picker

## Won't boot — first moves
| Symptom | Try |
|---|---|
| No OpenCore picker | BIOS: Secure Boot off, CSM off, boot order; see `BIOS_Configuration/` |
| Picker shows, macOS hangs | Boot verbose (already `-v`), photo the last lines and open an issue with it |
| Hang after an update | Picker → *Reset NVRAM*, then boot the known-good USB EFI |
| Panic loop | Picker → Space → macOS Recovery; or USB EFI with the last-good tag |

## Debug build (USB only)
Download the DEBUG zip of the version in `.opencore-version`, replace `OpenCore.efi`, `BOOTx64.efi`,
`OpenRuntime.efi` on the USB copy, set `Misc/Debug/Target=67`. Log is written as `opencore-*.txt` to the USB root.

## Useful commands on the laptop
- Loaded third-party kexts: `kmutil showloaded --list-only | grep -v com.apple`
- Last boot panics: `log show --last boot --predicate 'eventMessage contains "panic"'`
- Sleep history: `pmset -g log | grep -E "Sleep|Wake|Failure" | tail -50`
- Running OpenCore version: `nvram 4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102:opencore-version`
