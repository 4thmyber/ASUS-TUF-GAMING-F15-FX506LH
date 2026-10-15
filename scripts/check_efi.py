#!/usr/bin/env python3
"""EFI consistency checks that ocvalidate does not do. Stdlib only.

Fails (exit 1) on: unparsable plist, config entry pointing at a missing file,
Lilu not loaded before its plugins, OpenCore binaries not matching the pinned release.
Warns on: files on disk not referenced by the config, real-looking PlatformInfo.
"""
import hashlib
import pathlib
import plistlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OC = ROOT / "EFI" / "OC"
CONFIG = OC / "Config.plist"
LILU_PLUGINS = {"AppleALC.kext", "WhateverGreen.kext", "VirtualSMC.kext", "NVMeFix.kext",
                "BrightnessKeys.kext", "SMCBatteryManager.kext", "AMFIPass.kext"}

errors, warnings = [], []


def check(cfg, release_dir=None):
    for e in cfg["ACPI"]["Add"]:
        if e["Enabled"] and not (OC / "ACPI" / e["Path"]).is_file():
            errors.append(f"ACPI/Add: missing ACPI/{e['Path']}")

    order = []
    for e in cfg["Kernel"]["Add"]:
        if not e["Enabled"]:
            continue
        bundle = OC / "Kexts" / e["BundlePath"]
        order.append(pathlib.PurePath(e["BundlePath"]).name)
        for key in ("PlistPath", "ExecutablePath"):
            if e.get(key) and not (bundle / e[key]).is_file():
                errors.append(f"Kernel/Add: missing Kexts/{e['BundlePath']}/{e[key]}")
    if "Lilu.kext" in order:
        late = [k for k in order[:order.index("Lilu.kext")] if k in LILU_PLUGINS]
        if late:
            errors.append(f"Kernel/Add: Lilu.kext must load before {', '.join(late)}")

    for d in cfg["UEFI"]["Drivers"]:
        if d["Enabled"] and not (OC / "Drivers" / d["Path"]).is_file():
            errors.append(f"UEFI/Drivers: missing Drivers/{d['Path']}")

    # Orphans: on disk but never referenced (dead weight, or a forgotten config entry).
    used_acpi = {e["Path"] for e in cfg["ACPI"]["Add"]}
    used_kext = {e["BundlePath"].split("/")[0] for e in cfg["Kernel"]["Add"]}
    used_drv = {d["Path"] for d in cfg["UEFI"]["Drivers"]}
    for f in (OC / "ACPI").glob("*.aml"):
        if f.name not in used_acpi:
            warnings.append(f"orphan ACPI/{f.name}")
    for f in (OC / "Kexts").glob("*.kext"):
        if f.name not in used_kext:
            warnings.append(f"orphan Kexts/{f.name}")
    for f in (OC / "Drivers").glob("*.efi"):
        if f.name not in used_drv:
            warnings.append(f"orphan Drivers/{f.name}")

    serial = cfg["PlatformInfo"]["Generic"].get("SystemSerialNumber", "")
    if serial and not serial.startswith(("W00000", "0000", "XXXX")):
        warnings.append("PlatformInfo/Generic holds a real-looking serial — generate your own before sharing this EFI")

    if release_dir:
        rel = pathlib.Path(release_dir) / "X64" / "EFI"
        for ours, theirs in [(OC / "OpenCore.efi", rel / "OC" / "OpenCore.efi"),
                             (ROOT / "EFI" / "BOOT" / "BOOTx64.efi", rel / "BOOT" / "BOOTx64.efi"),
                             (OC / "Drivers" / "OpenRuntime.efi", rel / "OC" / "Drivers" / "OpenRuntime.efi")]:
            if sha(ours) != sha(theirs):
                errors.append(f"{ours.relative_to(ROOT)} differs from the pinned OpenCore release")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    for p in [CONFIG, *(OC / "Kexts").rglob("Info.plist")]:
        try:
            plistlib.loads(p.read_bytes())
        except Exception as ex:  # any parse error is a hard failure
            errors.append(f"bad plist {p.relative_to(ROOT)}: {ex}")
    if not errors:
        check(plistlib.loads(CONFIG.read_bytes()), sys.argv[1] if len(sys.argv) > 1 else None)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}")
    print(f"check_efi: {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
