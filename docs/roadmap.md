# Roadmap & References

Review of this EFI (OpenCore 1.0.5, macOS 26 Tahoe, SMBIOS `MacBookPro16,1`) as of 2026-10.
Priority: P2 important · P3 should do · P4 nice to have.

## Open items

| # | Prio | Finding | Plan |
|---|---|---|---|
| 1 | P2 | No USB map (USBToolBox/UTBMap were removed on 2025-08-26) | Re-map ports with USBToolBox (don't reuse the old map blindly), add `USBToolBox.kext` + `UTBMap.kext` — fixes sleep/wake and port issues |
| 2 | P3 | Outdated kexts: Lilu 1.7.1→1.7.2, AppleALC 1.9.5→1.9.8, WhateverGreen 1.7.0→1.7.1, VirtualSMC 1.3.7→1.3.8, RTL8111 2.5.0→3.0.0 | Upgrade one at a time, read each changelog |
| 3 | P3 | OpenCore 1.0.5 → latest 1.0.8 (schema change: `UEFI/Drivers/*/HideVerbose`) | Upgrade binaries + config + `.opencore-version` together |
| 4 | P3 | GTX 1650 only disabled via `-wegnoegpu` (still draws power) | SSDT `_OFF` for the dGPU → better battery and temperatures |
| 5 | P3 | `AppleXcpmCfgLock=true` (CFG Lock still on in firmware) | Check if it can be unlocked (ControlMsrE2); if so, drop the quirk |
| 6 | P4 | No Bluetooth | IntelBluetoothFirmware + IntelBTPatcher + BlueToolFixup |
| 7 | P4 | Wi-Fi via `itlwm` + HeliPort | Consider `AirportItlwm` (native Wi-Fi menu) once a Tahoe build is available |
| 8 | P4 | `enable-backlight-registers-fix` and `-alternative-fix` both enabled | Keep only the alternative fix (Comet Lake, macOS ≥ 13.4); verify |
| 9 | P4 | Verbose/debug boot-args `-v debug=0x100 keepsyms=1` | Remove `-v` once stable |
| 10 | P4 | Battery: SMCBatteryManager only | Check whether ASUS EC needs a battery SSDT; verify percentage updates |
| 11 | P4 | VoodooPS2Mouse and VoodooPS2Trackpad loaded although the trackpad is I2C | Disable both if keyboard and I2C trackpad still work (avoids input conflicts) |
| 12 | P4 | No tagged releases | Tag + attach `EFI-<tag>.zip` after each boot-tested change |

## Practices used in this repo
- **One pinned OpenCore version** (`.opencore-version`); CI runs that version's `ocvalidate` and checks the
  OpenCore binaries against the official release, so a half-done upgrade fails.
- **Consistency checks** (`scripts/check_efi.py`): every referenced ACPI/kext/driver file exists, Lilu loads first,
  unused files are flagged.
- **Upstream binaries only** — kexts from their official GitHub releases, never from pre-built EFI packs.
- **USB first, ESP second**; always keep a known-good EFI on a USB stick ([runbook](./runbook.md)).
- **One change per commit**, with the reason and a reference, so a boot failure can be bisected.

## macOS on Intel
- macOS 26 Tahoe is the last macOS release for Intel Macs; this EFI targets Tahoe point releases.
- Don't change SMBIOS once iServices are signed in. Turn off automatic macOS updates and check kext
  compatibility (Lilu plugins, AMFIPass, itlwm) before each point update.
- Only the Intel UHD 630 is usable; NVIDIA Turing GPUs have no macOS driver.

## References
- Dortania OpenCore Install Guide — Comet Lake laptop: https://dortania.github.io/OpenCore-Install-Guide/config-laptop.plist/comet-lake.html
- OpenCore `Configuration.pdf` (per version): https://github.com/acidanthera/OpenCorePkg/releases
- Dortania Post-Install (USB mapping, iServices, sleep): https://dortania.github.io/OpenCore-Post-Install/
- Getting Started with ACPI: https://dortania.github.io/Getting-Started-With-ACPI/
- Troubleshooting: https://dortania.github.io/OpenCore-Install-Guide/troubleshooting/troubleshooting.html
- Tools: USBToolBox https://github.com/USBToolBox/tool · SSDTTime https://github.com/corpnewt/SSDTTime ·
  ProperTree https://github.com/corpnewt/ProperTree · GenSMBIOS https://github.com/corpnewt/GenSMBIOS
- OpenIntelWireless (itlwm, Bluetooth): https://openintelwireless.github.io/ · Acidanthera kexts: https://github.com/acidanthera
