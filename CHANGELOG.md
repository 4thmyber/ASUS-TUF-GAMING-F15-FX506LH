# Changelog

All notable changes to this EFI. Each release lists the OpenCore version, kext versions,
the macOS version it was tested on, and what was verified on the hardware.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

No EFI changes.

### Added
- `scripts/check.sh`: validates `Config.plist` with `ocvalidate` for the pinned OpenCore version
  (`.opencore-version`), checks the OpenCore binaries against the official release, and checks that every
  referenced ACPI/kext/driver file exists and Lilu loads first. Runs in GitHub Actions on every push and PR.
- `docs/runbook.md` (install, boot-test checklist, recovery) and `docs/roadmap.md` (planned improvements, references).
- `CONTRIBUTING.md` (commit format, OpenCore upgrade procedure, release rules), `LICENSE` (MIT, own content only),
  bug report issue template.

### Changed
- README rewritten: hardware support table, status, full kext/SSDT list with versions and sources, usage steps.
- Renamed `Install/Prosess_0.jpg` → `Install/Process_0.jpg`; stopped tracking `.DS_Store` files.

## [v2025.08.28] — macOS 26 Tahoe

**OpenCore 1.0.5** · SMBIOS `MacBookPro16,1` · tested on macOS 26 Tahoe (build not recorded) ·
[download](https://github.com/4thmyber/ASUS-TUF-GAMING-F15-FX506LH/releases/tag/v2025.08.28)

### Added
- AMFIPass 1.4.1, loaded only on macOS 26 (`MinKernel` 25.0.0) — fixes audio on Tahoe.

### Kexts in this release
| Kext | Version |
|---|---|
| Lilu | 1.7.1 |
| VirtualSMC / SMCBatteryManager | 1.3.7 |
| WhateverGreen | 1.7.0 |
| AppleALC | 1.9.5 |
| NVMeFix | 1.1.3 |
| BrightnessKeys | 1.0.3 |
| VoodooPS2Controller (Keyboard, Mouse, Trackpad) | 2.3.7 |
| VoodooI2C (VoodooGPIO 1.1, VoodooI2CServices 1.0, VoodooInput 1.1.6) | 2.9.1 |
| VoodooI2CHID | 1.0 (VoodooI2C 2.9.1) |
| itlwm | 2.3.0 |
| RealtekRTL8111 | 2.5.0 |
| AMFIPass | 1.4.1 |

Drivers: OpenRuntime (OpenCore 1.0.5), OpenHfsPlus.
ACPI: SSDT-PLUG, SSDT-EC-USBX, SSDT-AWAC-DISABLE, SSDT-PMC, SSDT-PNLF, SSDT-XOSI.

## [2025-08-27]

**OpenCore 1.0.5**

### Added
- Audio: AppleALC `layout-id` 33 for ALC256.
- Wi-Fi: itlwm 2.3.0 (use with HeliPort).
- Trackpad: VoodooI2C 2.9.1 + VoodooI2CHID, SSDT-XOSI with `_OSI → XOSI` rename.
- Brightness keys: BrightnessKeys 1.0.3. Battery status: SMCBatteryManager 1.3.7.
- Boot-args: `-wegnoegpu` (disable NVIDIA dGPU), `-v debug=0x100 keepsyms=1`.

## [2025-08-26] — Minimal working EFI

**OpenCore 1.0.5**

### Changed
- Rebuilt the EFI from a minimal base: custom SSDTs (PLUG, EC-USBX, AWAC-DISABLE, PMC, PNLF) instead of a full `DSDT.aml`.
- `SecureBootModel`: `Default` → `Disabled`.

### Removed
- DSDT.aml, AudioDxe, OpenShell/CleanNvram/ResetSystem tools.
- Kexts: AirportItlwm, AsusSMC, BlueToolFixup, CpuTscSync, HibernationFixup, IntelBTPatcher,
  IntelBluetoothFirmware, NoTouchID, RestrictEvents, SMCLightSensor, SMCProcessor, SMCSuperIO,
  USBToolBox, UTBMap, XHCI-unsupported; VoodooI2C, VoodooI2CHID and SMCBatteryManager (re-added 2025-08-27).

## [2025-08-17 – 2025-08-18] — Initial setup

**OpenCore 1.0.5**
- BIOS configuration screenshots, installation screenshots, hardware list.
- First EFI targeting macOS Ventura.
