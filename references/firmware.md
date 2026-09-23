# Firmware and Flashing

## Downgrading

Only possible on jailbroken Kindle. Update (not downgrade) possible on stock firmware; direct flash with soldered 1.8v serial-to-USB adapter (even Android).

Cannot downgrade below firmware originally installed on device. Update file for different device rejected. Since 5.18.x, some models may not downgrade below 5.18.x or across 5.18.x branch (bootloader hardening). Some models may reject downgrade and return to UI since 5.18.x — retry with closer firmware version; fail again → wait for new downgrade method.

### AllowDowngrade.sh

Scriptlet by Marek. Copies /etc/version.txt to /mnt/us/version.txt.backup. Remounts rootfs rw (mntroot rw). sed rewrites first-line version suffix to 336034:
```sh
sed -i -E "1 s/(-)([0-9]+)$/\1${VER}/g" "/etc/version.txt"
```
Remounts ro. Device then accepts older update package.

### Downgrade steps

1. Airplane mode on. Restore OTA updates (renametobin Restore). Disable USBNetwork (USBMS) if installed.
2. Copy AllowDowngrade.sh into documents folder (Kindle plugged into PC).
3. Eject, unplug. Open library, click "Allow Downgrade" booklet. Text prints seconds, returns to library — downgrading enabled.
4. Copy update_kindle_*.bin to Kindle root. DO NOT eject or unplug — hold power button until restart.
5. Kindle installs copied firmware.

### Post-downgrade

Redo post-jailbreak instructions to keep jailbreak.

White screen after large version jump → plug into PC, sideload empty file named DO_FACTORY_RESTORE (no extension) into root, force reboot (hold power 20-30s). Back up files first.

hard-float (>=5.16.3) vs soft-float (<=5.16.2.1.1) — crossing breaks extensions.

Some devices skip initial setup after restart; others keep prompting → sign in, skip Wi-Fi prompt, delete update.bin.tmp.partial from root if present.

Slower performance after downgrade → factory reset recommended. Back up files. Set up hotfix first.

## Downloading firmware updates

Amazon does not delete old Kindle firmware from servers. Any version downloadable by changing link. Install:
1. Airplane mode.
2. Plug Kindle into PC.
3. Copy update file to root (same place as documents folder).
4. Eject, unplug.
5. Settings → top-right menu → Update Your Kindle.

K1, K2, DX, K3 need serial-number-specific firmware — see https://www.amazon.com/gp/help/customer/display.html?nodeId=GKMQC26VQQMM8XSW

Table below: last jailbreakable firmware per model at time of writing. >PW5 (can't jailbreak) and <PW3 (very old) linked latest firmware at time of writing. Verify before updating.

| Nickname | Model | Link |
|---|---|---|
| K5 | Kindle Touch (4th Generation) | https://s3.amazonaws.com/G7G_FirmwareUpdates_WebDownloads/update_kindle_5.3.7.3.bin |
| K4 / K4B | Kindle (4th and 5th Generation) | https://firmwareupdates.s3.amazonaws.com/1435/Update_2692310002-3543630001.bin |
| PW | Kindle Paperwhite (5th Generation) | https://s3.amazonaws.com/G7G_FirmwareUpdates_WebDownloads/update_kindle_5.6.1.1.bin |
| PW2 | Kindle Paperwhite (6th Generation) | https://s3.amazonaws.com/firmwaredownloads/update_kindle_paperwhite_v2_5.12.2.2.bin |
| KT2 | Kindle (7th Generation) | https://s3.amazonaws.com/firmwaredownloads/update_kindle_5.12.2.2.bin |
| KV | Kindle Voyage (7th Generation) | https://s3.amazonaws.com/firmwaredownloads/update_kindle_voyage_5.13.6.bin |
| PW3 | Kindle Paperwhite (7th Generation) | https://s3.amazonaws.com/firmwaredownloads/update_kindle_all_new_paperwhite_5.14.2.bin |
| KOA1 | Kindle Oasis (8th Generation) | https://s3.amazonaws.com/firmwaredownloads/update_kindle_oasis_5.16.2.1.1.bin |
| KT3 | Kindle (8th Generation) | https://s3.amazonaws.com/firmwaredownloads/update_kindle_8th_5.16.2.1.1.bin |
| KOA2 | Kindle Oasis (9th Generation) | https://s3.amazonaws.com/firmwaredownloads/update_kindle_all_new_oasis_5.16.2.1.1.bin |
| PW4 | Kindle Paperwhite (10th Generation) | https://s3.amazonaws.com/firmwaredownloads/update_kindle_all_new_paperwhite_v2_5.18.1.bin |
| KT4 | Kindle (10th Generation) | https://s3.amazonaws.com/firmwaredownloads/update_kindle_10th_5.18.1.bin |
| KOA3 | Kindle Oasis (10th Generation) | https://s3.amazonaws.com/firmwaredownloads/update_kindle_all_new_oasis_v2_5.18.2.bin |
| PW5/PW5SE | Kindle Paperwhite (11th Generation) / Kindle Paperwhite Signature Edition | https://s3.amazonaws.com/firmwaredownloads/update_kindle_all_new_paperwhite_11th_5.17.1.0.3.bin |
| KT5 | Kindle (11th Generation) - 2022 Release | https://s3.amazonaws.com/firmwaredownloads/update_kindle_11th_5.18.6.bin |
| KS | Kindle Scribe - 2022 Release | https://s3.amazonaws.com/firmwaredownloads/update_kindle_scribe_5.18.5.0.1.bin |
| KT6 | Kindle (11th Generation) - 2024 Release | https://s3.amazonaws.com/firmwaredownloads/update_kindle_11th_2024_5.18.5.0.1.bin |
| PW6 | Kindle Paperwhite (12th Generation) - 2024 Release | https://s3.amazonaws.com/firmwaredownloads/update_kindle_all_new_paperwhite_12th_5.18.5.0.1.bin |
| KS2 | Kindle Scribe - 2024 Release | https://s3.amazonaws.com/firmwaredownloads/update_kindle_scribe_2024_5.17.3.bin |

## Forcing KV to run 5.14+

Extremely advanced. Brick risk. Experimental. Little recovery support.

PW3 and KV nearly identical hardware; identical partition layout → cross-flash PW3 firmware onto KV. Wario hardware family (PW2, PW3, KT2, KV); PW2 excluded (smaller RootFS — Neon found out). ONLY attempt on KV with 512MB RAM. KT2 with 256MB can run 5.14+ but 5.13.7+ React UI memory-hungry → instabilities.

Prerequisites: Kindle Voyage; 1.8v USB-to-Serial adapter soldered to KV; serial software (PuTTY); NiLuJe's KindleTool (https://github.com/NiLuJe/KindleTool); PW3 update file.

Steps:
1. `kindletool extract ~/Downloads/update_kindle_all_new_paperwhite_5.XX.X.bin /tmp/pw3`
2. `gzip -d /tmp/pw3/rootfs.img.gz`
3. PuTTY to serial port, baudrate 115200bps.
4. Boot Kindle, interrupt by hitting enter rapidly until `uboot >`.
5. `uboot > bootm 0xE41000` → DIAGS mode.
6. In DIAGS: `usb export` (exports userspace partition).
7. COPY rootfs.img to Kindle via file manager. DO NOT FLASH IMAGE ONTO KINDLE — just copy.
8. Eject Kindle from PC. DO NOT UNPLUG.
9. Exit USB export: type `x`.
10. Exit DIAGS, get shell: `exit login`
11. Flash: `dd if=/mnt/us/rootfs.img of=/dev/mmcblk0p1 bs=4096`
12. `reboot`

Kindle boots flashed firmware. No boot → try flashing again.

Credits: figured out by katadelos (https://www.mobileread.com/forums/showthread.php?t=343385); guide by Neon.

## OTA files

OTA files page currently placeholder — not yet written.

What sources say: hotfixes distributed as OTA files. Homebrew OTAs signed with private key in KindleTool create.c: https://github.com/KindleModding/KindleTool/blob/4fa6d0ca6c5ec24564e0f0f3a90dbe3618d6346a/KindleTool/create.c#L49. Jailbreaks install new OTA keys first. Special OTA type runs every .sh file in package when installed.
