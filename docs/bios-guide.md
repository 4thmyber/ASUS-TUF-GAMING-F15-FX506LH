# BIOS Guide — ASUS TUF Gaming F15 FX506LH

Recommended BIOS settings for running macOS with the OpenCore EFI in this repository.
Based on the [Dortania Comet Lake laptop guide](https://dortania.github.io/OpenCore-Install-Guide/config-laptop.plist/comet-lake.html#intel-bios-settings)
and tested on the hardware listed in the [README](../README.md).

- **Tested BIOS version:** 310 (2021-11-26)
- **Last reviewed:** 2026-10-15 — see [Recommendation history](#recommendation-history) for what changed

> Settings marked **Required** must match, or macOS will not boot or devices will be missing.
> **Recommended** settings improve the experience but are not needed to boot.

---

## Quick reference

| Menu | Setting | Value | Level | Why |
|---|---|---|---|---|
| Advanced | Internal Pointing Device | Enabled | Required | The I2C trackpad needs it |
| Advanced | Hyper-Threading | Enabled | Recommended | Use all 12 threads |
| Advanced | Intel Virtualization Technology (VT-x) | Enabled | Recommended | Needed by VMs/Docker; harmless for macOS |
| Advanced | VT-d | Disabled | Required* | Not needed; the config also sets `Kernel/Quirks/DisableIoMapper` |
| Advanced → Network Stack Configuration | Network Stack | Disabled | Recommended | No PXE network boot; faster startup |
| Advanced → USB Configuration | USB Mass Storage Driver Support | Enabled | Required | Boot from the USB installer |
| Advanced → Graphics Configuration | DVMT Pre-Allocated | 64M | Required | The iGPU framebuffer needs ≥ 64 MB |
| Advanced → SATA Configuration | SATA mode | AHCI — no Intel RST / RAID / VMD | Required | RST/VMD hides the NVMe drives from macOS |
| Boot | Fast Boot | Disabled | Required | Lets OpenCore and USB devices initialize |
| Boot | Boot Option #1 | OpenCore on the macOS drive | Required | See [Boot order](#6-boot-order-after-installing) |
| Security → Secure Boot | Secure Boot Control | Disabled | Required | OpenCore/macOS are not signed for PC Secure Boot |
| Security → I/O Interface Security | Wireless & Bluetooth, LAN, HD Audio | Unlock | Required | Locked devices are invisible to macOS |
| Security → I/O Interface Security → USB Interface Security | External Ports, CMOS Camera | Unlock | Required | Same as above |

\* VT-d may also be Enabled, because the config sets `DisableIoMapper`. Disabled is the simpler, tested setting.

**Not available in this BIOS (nothing to do):**
- **CSM** — the BIOS is UEFI-only, which is what OpenCore needs.
- **CFG Lock** — hidden by ASUS. The config works around it with `Kernel/Quirks/AppleXcpmCfgLock`.
  Unlocking it needs a modded BIOS or UEFI variable editing; not recommended for the small gain.

---

## Step by step

### 0. Before you start
1. Plug in the charger.
2. Note your current settings or take photos — **F9** restores the defaults if something goes wrong.
3. Check for a newer BIOS: see [Updating the BIOS](#updating-the-bios).

### 1. Enter the BIOS
Power on and press **F2** repeatedly. Press **F7** to switch from EZ Mode to Advanced Mode.

| EZ Mode | Main — BIOS version |
|---|---|
| ![EZ Mode](../BIOS_Configuration/BIOS_Configuration.jpg) | ![Main](../BIOS_Configuration/BIOS_Configuration_1.jpg) |

Check **Main → Version** (310 or newer).

### 2. Advanced
Set **Internal Pointing Device**, **Hyper-Threading**, **Intel Virtualization Technology**, **VT-d** as in the table.

| Advanced (top) | Advanced (scrolled) |
|---|---|
| ![Advanced](../BIOS_Configuration/BIOS_Configuration_2.jpg) | ![Advanced scrolled](../BIOS_Configuration/BIOS_Configuration_3.jpg) |

> The screenshots show *Intel Virtualization Technology* **Disabled**; it was taken before this recommendation. Set it to **Enabled**.

Sub-menus:

| Network Stack → Disabled | USB Configuration → Enabled | Graphics → DVMT 64M |
|---|---|---|
| ![Network Stack](../BIOS_Configuration/BIOS_Configuration_6.jpg) | ![USB Configuration](../BIOS_Configuration/BIOS_Configuration_7.jpg) | ![Graphics](../BIOS_Configuration/BIOS_Configuration_8.jpg) |

| NVMe Configuration (both drives visible) | SMART Settings (leave default) | EZ Flash 3 (BIOS update) |
|---|---|---|
| ![NVMe](../BIOS_Configuration/BIOS_Configuration_9.jpg) | ![SMART](../BIOS_Configuration/BIOS_Configuration_5.jpg) | ![EZ Flash](../BIOS_Configuration/BIOS_Configuration_4.jpg) |

Open **SATA Configuration** and make sure no Intel RST / RAID / VMD option is enabled.

### 3. Boot
Set **Fast Boot** → Disabled.

| Boot | Add New Boot Option | Delete Boot Option |
|---|---|---|
| ![Boot](../BIOS_Configuration/BIOS_Configuration_10.jpg) | ![Add boot option](../BIOS_Configuration/BIOS_Configuration_11.jpg) | ![Delete boot option](../BIOS_Configuration/BIOS_Configuration_12.jpg) |

### 4. Security
Set **Secure Boot Control** → Disabled, and every item in **I/O Interface Security** → Unlock.

| Security | I/O Interface Security | USB Interface Security | Secure Boot |
|---|---|---|---|
| ![Security](../BIOS_Configuration/BIOS_Configuration_13.jpg) | ![I/O Interface Security](../BIOS_Configuration/BIOS_Configuration_14.jpg) | ![USB Interface Security](../BIOS_Configuration/BIOS_Configuration_15.jpg) | ![Secure Boot](../BIOS_Configuration/BIOS_Configuration_16.jpg) |

### 5. Save
**Save & Exit → Save Changes and Exit** (or **F10**).

![Save & Exit](../BIOS_Configuration/BIOS_Configuration_17.jpg)

### 6. Boot order after installing
- **Installing:** press **F8** at power-on and choose the USB stick (`UEFI: <your USB>`).
- **After installing** and copying the EFI to the internal drive (see the [runbook](./runbook.md)):
  - **EFI with `LauncherOption = Full`** (planned for the next release): OpenCore adds its own boot entry
    and keeps it first, even after Windows updates. Nothing to do.
  - **EFI v2.0.2 and older** (`LauncherOption = Disabled`): add the entry manually —
    **Boot → Add New Boot Option** → choose the macOS drive → path `\EFI\BOOT\BOOTx64.efi` → name it `OpenCore` →
    **Create**, then set it as **Boot Option #1**.
- **Dual boot with Windows:** keep Windows on its own drive (on the reference laptop Windows is on the Micron
  drive, macOS on the Kingston drive) and start Windows from the OpenCore picker or with **F8**.

---

## Updating the BIOS
1. Check the **BIOS & FIRMWARE** tab on the [ASUS FX506LH support page](https://www.asus.com/supportonly/FX506LH/HelpDesk_Download/).
   Confirm the exact model on the label under the laptop — never flash a BIOS for another model (e.g. FX506HF).
2. Copy the BIOS file to a FAT32 USB stick.
3. Charger plugged in → BIOS → **Advanced → ASUS EZ Flash 3 Utility** → select the file.
4. After updating, **settings are reset to defaults** — go through this guide again.
5. Boot from the USB EFI first. If something breaks, open an issue with the new BIOS version.

---

## Troubleshooting

| Symptom | Check |
|---|---|
| USB stick not in the F8 menu | USB Mass Storage Driver Support = Enabled; stick formatted GUID + FAT32 EFI partition |
| Laptop boots straight into Windows | Boot Option #1 / OpenCore entry ([step 6](#6-boot-order-after-installing)) |
| Installer can't see the NVMe drives | SATA mode: no RST/VMD; NVMe Configuration lists both drives |
| No trackpad | Internal Pointing Device = Enabled |
| No Wi-Fi / Ethernet / audio / camera | I/O Interface Security → all Unlock |
| Black screen or panic at the iGPU | DVMT Pre-Allocated = 64M |
| Settings lost | BIOS update or CMOS reset restores defaults — redo this guide |

More: [runbook](./runbook.md) · [Dortania troubleshooting](https://dortania.github.io/OpenCore-Install-Guide/troubleshooting/troubleshooting.html)

---

## Recommendation history

| Date | Change |
|---|---|
| 2026-10-15 | Guide created. New: **Intel Virtualization Technology (VT-x) → Enabled** (recommended). Documented SATA mode (AHCI), boot-order setup, CSM/CFG Lock not exposed, BIOS update procedure. |
| 2025-08-17 | Original screenshots on BIOS 310. |

Found a setting that works better, or a newer BIOS version? Open an issue with your BIOS version and macOS build.
