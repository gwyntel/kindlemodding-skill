# Jailbreak FAQ, Recovery, What's Next

## Jailbreak FAQ

Last updated: Apr 09, 2026. Instructions subject to change with new jailbreaks/patches/extensions/firmware.

### General/Account

Kindle updated to firmware with no jailbreak — can I jailbreak? No. Wait for new method (weeks/months). Protect: forget saved connections, Airplane mode. prevent-auto-update guide helps use internet while blocking updates.

Downgrade to jailbreak? No. Must jailbreak first — Amazon never allowed downgrade on stock firmware.

Unregistered/blacklisted Kindle — jailbreakable? Nosebleed jailbreak reportedly works for some blacklisted devices. Firmware 5.16.2.1.1 or below: try Legacy jailbreak methods.

Deregister after jailbreaking? Yes — stays jailbroken logged in or out. Deregistering deletes documents folder (KUAL booklet, scriplets) → may partially break extensions. Back up first.

Un-jailbreak? Yes. Re-enable automatic updates first (Restore in renametobin) to avoid update block. Factory reset, install same or higher firmware update.

Account banned? No reports so far. Don't tell support you modified device.

Warranty void? Probably.

soft-float vs hard-float? 5.16.3+ uses hard-float (on-chip FPU); ≤5.16.2.1.1 soft-float (software-emulated). Internals changed — most jailbreak tools/extensions unusable across the boundary unless stated (e.g. NiLuJe's Screensaverhack).

### Apps and eBooks

Default reader after jailbreak? Yes.

Sideload books? Yes.

Books/highlights deleted? No. Warning: Kindle in Airplane mode long time → Amazon may delete sideloaded books after reconnecting to Wi-Fi (internal book tag). Happens jailbroken or not. Back up books. https://www.mobileread.com/forums/showpost.php?p=4419300&postcount=409

Libby/Readwise/GoodReads/Kindle Unlimited/Send To Kindle? Yes — jailbreak doesn't interfere.

Those apps inside KOReader? No, unless plugin exists.

Android apps (Libby, Nook, Webtoon) on jailbroken Kindle? No, unless extension/port exists.

Amazon ebooks in KOReader? KOReader doesn't (likely never will) support KFX, AZW3, very limited MOBI. Get books as EPUB, separate folder.

Libby books in KOReader? No. Get EPUB from Libby: https://help.libbyapp.com/en-us/6059.htm.

Where download free ebooks? Google it.

### KOReader

Three KOReader launch options: "Start KOReader" = designed way; "Start KOReader (no framework)" = kills Kindle UI temporarily, more resources for KOReader; "Start KOReader (ASAP)" = skips checks, starts ASAP.

Can't transfer files via USB in KOReader? KOReader lacks USBMS mode — only charges. Exit KOReader to transfer.

Launch via KUAL required? No. Alternatives: Marek's scriptlet launcher (https://scriptlets.notmarek.com/), KOR booklet launcher by yparitcher (https://github.com/yparitcher/KUAL_Booklet/releases/). Customize with coversetter extension by Stanner (https://www.mobileread.com/forums/showpost.php?p=4222466&postcount=15).

### Technical

"Root directory"? First directory seen when plugging into computer. SSH: /mnt/us/.

Update/factory reset/downgrade after jailbreaking? Yes, but Airplane mode on + automatic updates re-enabled (Restore in renametobin) to avoid update blocks/unwanted updates. New version must support a jailbreak. After: reinstall hotfix from scratch; KUAL and some extensions may need reinstall.

How downgrade? Downgrading guide (firmware draft).

Where firmware updates? Downloading-updates guide. Find exact model, link, retype numbers for version wanted.

How use scriptlets (.sh)? Copy .sh into documents folder (/documents); in library view, click it.

Check automatic updates disabled after renametobin? Download "Check OTA Status" scriptlet: https://scriptlets.notmarek.com/

Change screensavers in native UI? Hard-float: no extensions. Soft-float: NiLuJe's screensaver hack (https://www.mobileread.com/forums/showthread.php?t=195474). May fail on some final soft-float versions. Do NOT install under hard-float. KOReader can change screensavers (search "screensavers" in https://koreader.rocks/user_guide/).

### Jailbreaking

Check if jailbroken? Type `;log` in search bar. Popup = jailbroken.

KUAL/extensions stopped working? Check ;log. Popup → reinstall hotfix + KUAL from scratch. No popup → re-jailbreak. All failed → factory reset, jailbreak from scratch.

Can't update after factory reset/update? Reset in jailbroken state with renametobin still enabled = locked state. See recovering-from-a-reset.

"Failed to remount rootfs RO, waiting"? Expected. Reboot manually (hold power → Restart).

No reboot after jailbreak popup? Winterbreak: unless Kindle shows "You are now ready to install the hotfix" in small text, safe to continue post-jailbreak instructions. Missing → jailbreak failed, retry. Delete any automatic update file that appeared.

Random "KPPMainAppV2" books in library? Kindle generates after errors (common after exiting KOReader frameworkless). Safe to delete. Disable: create empty file DISABLE_CORE_DUMP in USB storage root. Same for "Collecting Debug Info" message.

Jailbroken — what now? Install KOReader, downgrade Kindle, scriptlets (Marek's: https://scriptlets.notmarek.com/), develop extensions, browse MobileRead (https://www.mobileread.com/forums/forumdisplay.php?f=150) or Kindle Modding Community Discord, install Alpine Linux, support Winterbreak & wiki (https://ko-fi.com/hackerdude).

KFT option in settings? ¯\_(ツ)_/¯

## Bypassing OOBE

Some Kindles (Scribe, Colorsoft) won't skip registration during setup. Blacklisted/no registration → stuck in Out-Of-Box Experience. Bypass to jailbreak/use:

1. Go to captive-portal Wi-Fi (coffee shop type: browser popup agreeing terms). Don't connect yet — just need browser access.
2. In captive portal browser search bar: type `;demo`, submit. Press NO at demo mode dialog. HITTING YES CAN PERMANENTLY STICK YOU IN DEMO LIMBO.
3. Hit Home tab at bottom.
4. Kindle usable: settings, Wi-Fi, browser — jailbreak per Jailbreaking Wizard. Fill storage (prevent-auto-update) before connecting to Wi-Fi.
5. After jailbreaking: run Disable OOBE scriptlet (./disable_oobe.sh). Scriptlets install explained in whats-next/installing-homebrew. Skip this → captive portal trick needed every reboot.

### disable_oobe.sh

Removes /var/local/decanter/RESUME_OOBE_FOR_OTA and /var/local/decanter/OTA_START_FOR_METRIC. Reboots after 5s. Permanently disables OOBE.

## ota.sh / prevent-auto-update

### ota.sh ("Restore Updates" scriptlet)

Restores OTA capability after renametobin blocked updates (renametobin renames binaries to .bck):
- Locates chattr: /bin/chattr, or /bin/chattr.e2fsprogs (KT6 5.18.1.5+ and PW6, KS, KS2 5.18.5+). Falls back to /bin/chattr if neither found.
- mntroot rw.
- chattr -i /usr/bin/otaupd.bck and /usr/bin/otav3.bck (clears immutable).
- mv otaupd.bck → otaupd, otav3.bck → otav3.
- mntroot ro. Sleep 5. Reboot.

### Prevent automatic updates: fill storage

Kindle auto-downloads/installs updates with enough free space — updates block jailbreaks. Triggers: opening Kindle Store, registering, Wi-Fi (even brief), reboot while online.

Leave only 50-90 MB free → update can't download.

How: delete update-whatever.bin or update.partial.bin, Airplane mode on. Script: Kindle-Filler-Disk repo (https://github.com/bastianmarin/Kindle-Filler-Disk/) — Windows: Filler.ps1; macOS/Linux: Filler.sh.

11th gen and newer: MTP instead of USB storage → script won't work. Manually fill: download matching Filler files (https://github.com/Crosunt223/Kindle-Filler-Disk/tree/main/MTP) per Kindle storage size, extract, copy to Kindle root (or folder). Keep 50-90 MB free.

Steps: 1) Airplane mode. 2) USB to computer, wait for Kindle drive. 3) Download Filler script from repo. 4) Copy script to Kindle root. 5) Run: Windows → right-click Filler.ps1, Run with PowerShell (execution policy error → `powershell -ExecutionPolicy Bypass -File .\Filler.ps1`); macOS/Linux → `chmod +x Filler.sh`, `./Filler.sh`. 6) Eject; Settings > Device Options > Device Info → verify ≤50-90 MB free. 7) Connect Wi-Fi/register — update can't fully download. Then jailbreak or wait for jailbreak. Always delete .bin files / update.bin.tmp.partial.

After jailbreak (OTA disabled): delete fill_disk folder to recover space. Linux/macOS: `rm -rf fill_disk`. Can delete some files only to keep disk nearly full.

## Recovering from a reset

Factory reset of jailbroken Kindle with updates blocked → official update files can't install (needed to fully remove jailbreak). Restore ability: install ota.sh scriptlet.

Stuck on "Update Failed" after resetting without restoring OTAs:
1. Find model + firmware version at https://ftvdb.com/kindle/firmware/. Naming differs: KindleModding KT6 = FTVDB "Basic 5"; PW numbers same.
2. Download .bin, place in USB root.
3. Eject, unplug.
4. Reboot, wait for update install.
5. Kindle fully unjailbroken → rejailbreak via Jailbreaking Wizard method.

## What's next after jailbreak

Modern jailbreaks use hdnext stack. KPM package manager preinstalled (explained next). First: delete filler files; remove any .bin update files in root. Updates auto-blocked.

### Installing homebrew

Scriptlets: .sh files in documents folder appear as books. Apps from online come as scriptlets — copy/paste. Warning: unknown sources = malware/brick risk.

KPM: package manager, install scriptlets on-device via searchbar commands: `;kpm install`, `;kpm update`, etc. Like apt-get.

KOPlugins: KOReader plugin mechanism (koreader.rocks). Examples: SimpleUI (https://github.com/doctorhetfield-cmd/simpleui.koplugin), ZenUI (https://github.com/AnthonyGress/zen_ui.koplugin). Manual install: copy into /koreader/plugins. Or on-device via AppStore KOPlugin (e.g. Storefront: https://github.com/ultimatejimmy/storefront.koplugin).

KUAL obsolete — doesn't work. Popular homebrew list: https://github.com/KindleTweaks/Awesome-Kindle.

### Getting KOReader

KOReader = document viewer for E-Ink. Formats: EPUB, PDF, DjVu, XPS, CBT, CBZ, FB2, PDB, TXT, HTML, RTF, CHM, DOC, MOBI, ZIP.

Installed from official KindleModding KPM repo: https://repo.kindlemodding.org/.

1. Reboot if just jailbroken and haven't. Wi-Fi enabled.
2. Searchbar: `;kpm update`. Text at top of screen, returns to homepage.
3. Searchbar: `;kpm install koreader`. Wait — returned to homescreen, new scriptlet appears (icon may lag).
4. Click scriptlet → KOReader runs. Or `;kpm launch koreader`.
5. Uninstall: `;kpm uninstall koreader`. All KPM packages same way.

## nosb scripts

nosb.sh: Nosebleed bootstrap downloader. Logs to /mnt/us/nosb.log, shows progress on-screen (eips) and echo. curls https://kindlemodding.org/nosb/jb → /var/local/jb, chmod +x. curls https://kindlemodding.org/nosb/nosb_jb.sh → /mnt/us/jb.sh, chmod +x. Runs /var/local/jb.

nosb_jb.sh: one-liner. curls https://kindlemodding.org/jb.sh, pipes to sh with JB_HEADER="Nosebleed Jailbreak".

## Vera privesc

static/vera/aprivesc/privesc.sh — privilege escalation for Vera jailbreak. Logs "privesc.sh executed any failure is solely with the privesc now" via logger. curls https://kindlemodding.org/vera/aprivesc/jb.so → /tmp/jb.so, chmod +x. Then `lipc-set-prop com.lab126.system updateWaveform LD_PRELOAD=/tmp/jb.so` — injects jb.so into process via LD_PRELOAD through updateWaveform property. Needed where exploit lands without root.
