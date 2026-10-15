# Contributing

Thanks for helping. This EFI boots real hardware, so every change follows the same rules.

## Before you open a PR
1. `./scripts/check.sh` passes (also runs in CI).
2. You booted the change **from a USB stick** on an FX506LH and ran the
   [boot-test checklist](./docs/runbook.md#boot-test-checklist). Say what you tested in the PR.
3. No personal data: remove serial, MLB, SystemUUID and ROM from logs, screenshots and any new config.

## One change per commit
A boot failure is easiest to find when each commit does one thing. Message format:

```text
<area>: <what changed> (<component> <old> → <new>)

<why, and a link to the upstream changelog or Dortania page>
```

Areas: `opencore`, `kext`, `acpi`, `config`, `audio`, `wifi`, `trackpad`, `graphics`, `power`, `usb`, `docs`, `ci`, `repo`.
Examples: `kext: AppleALC 1.9.5 → 1.9.8`, `acpi: add SSDT to power off NVIDIA dGPU`.

## Kexts and drivers
- Only official RELEASE builds from the upstream repository listed in the README. Replace the whole
  `.kext` bundle, never single files.
- Update the README kext table and `CHANGELOG.md` ([Unreleased]) in the same commit.

## Upgrading OpenCore
Binaries and config always move together, in one commit:
1. Read OpenCore's `Docs/Changelog.md` for every version you skip.
2. Replace `EFI/BOOT/BOOTx64.efi`, `EFI/OC/OpenCore.efi`, `EFI/OC/Drivers/OpenRuntime.efi` from the RELEASE zip.
3. Add/remove `Config.plist` keys to match the new `Docs/Sample.plist`.
4. Write the new version to `.opencore-version`.
5. `./scripts/check.sh` — it fails if the binaries, config schema and pinned version don't match.

## Editing Config.plist
Use ProperTree, OCAT or Python `plistlib`. Avoid editors that reorder or drop keys.

## Releases
After a change passes the boot test, it is tagged `vMAJOR.MINOR.PATCH` — MAJOR: new macOS target or EFI rebuild,
MINOR: new working feature, PATCH: fix — and published as a GitHub release with
`EFI-<tag>.zip`. Each CHANGELOG entry lists the OpenCore version, kext versions and the **macOS build tested**.
