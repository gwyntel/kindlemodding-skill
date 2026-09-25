# Kindle jailbreaks — condensed reference

Source: kindlemodding site content. All jailbreaks converge on same goal. Wizard picks method. Never "update" a jailbreak.

Relative `./file` download URLs below = hosted on kindlemodding.github.io alongside the guide pages; verbatim as in source.

Modern jailbreaks (WinterBreak, WinterBreak2, SpringBreak, Sanctuary, SpiderCat, Nosebleed, Vera, AdBreak) use `hdnext` stack. Jailbreak auto-installs package manager KPM + update blocking. Post-jailbreak: install scriptlets/homebrew/KOReader.

Jailbreak = run external code (KOReader etc), not OS/firmware. Other features stay.

## Rules before any jailbreak

- Read lander page first. No support otherwise.
- Fill storage before connecting to internet: leave only 50-90 MB free. Prevents OTA download killing jailbreak mid-process. Delete any `update-whatever.bin` / `update.bin.tmp.partial` / stray `.bin` files in root. Airplane Mode on.
- Never factory reset without experienced person's advice.

## WinterBreak

Released New Year's Day 2025 by Hackerdude. Based on Mesquito. Registration required.

Targets (wizard mapping): PW, PW2, KV, KT2, PW3, KOA, KT3, KOA2, PW4, KT4, KOA3, PW5, KT5, KS, KT6, PW6, KS2, CS. Firmware 5.6.1.1 - 5.18.0.2 (denied: none). NOT work on `5.18.1` and beyond.

How: exploits Kindle Store via Mesquito sandbox. Files copied to Kindle incl hidden folder `.active_content_sandbox`; opening Store loads exploit from `LocalStorage`.

Steps:
1. Fill device (prevent-auto-update), read overview.
2. Download `https://github.com/KindleModding/WinterBreak/releases/latest/download/WinterBreak.tar.gz`
3. Airplane Mode on. Reboot.
4. Extract `WinterBreak.tar.gz` on PC (not directly to Kindle), copy files to Kindle. Linux/MacOS: ensure hidden folder `.active_content_sandbox` copied. Replace files if prompted.
5. Eject. Open Kindle Store (cart icon). Click `Yes` when prompted to turn off Airplane mode (Mesquito loads).
6. Click WinterBreak icon. Wait ~30s; text spews; GUI restarts.
7. Done -> whats-next. Delete filler files. Updates auto-blocked. Remove any `.bin` update files in root.

Troubleshooting: "Unexpected error" on Store login or only Store homepage shown -> LocalStorage replacement: register+fill, plug in, delete `.active_content_sandbox`, reboot, disable Airplane + Wi-Fi, browse Store few minutes (browse categories, download free sample), enable Airplane, plug in, delete `.active_content_sandbox/store/resource/LocalStorage`, copy WinterBreak files, delete stray `update-bin-whatever.bin` or `update.bin.tmp.partial`, reboot, open Store, click Yes. Alternative: Factory Reset: reset, before registering copy WinterBreak files to root, login, enable Airplane ASAP, plug in, delete `.active_content_sandbox/store/resource/LocalStorage` (skip if absent), reboot, open Store, click Yes.

## WinterBreak2

Released by Scam.Net + Penguins184. Browser-based. No Amazon registration needed.

Targets (wizard mapping): PW, PW2, KV, KT2, PW3, KOA, KT3, KOA2, PW4, KT4, KOA3, PW5, KT5, KS. Firmware 5.6.1.1 - 5.16.3, outlier accepted `5.16.5`. Guide says: firmware below 5.16.4 try original WinterBreak instead if WB2 fails (requires registration).

How: files on Kindle root (`winterbreak2` folder); experimental browser visits hosted exploit page, presses Jailbreak button.

Steps:
1. Fill device, read overview.
2. Download `https://github.com/KindleModding/Winterbreak2/releases/latest/download/wb2.zip`
3. Extract `wb2.zip` contents to root of Kindle storage. `winterbreak2` folder must sit on root.
4. Eject. Connect to Wi-Fi.
5. Open Experimental Browser: `Menu → Experimental Browser` (or `Settings → Device Options → Advanced → Experimental Browser`).
6. Navigate to `https://penguins184.xyz/wb2`
7. Press **Jailbreak** button. Dialog opens; wait for completion.
8. Delete filler files. Updates auto-blocked. Remove `.bin` update files in root.

## SpringBreak

Released 22/06/26 by Penguins184. Registration required. Credits: Hhhhhhhhh (initial LPE, core ideas), Hackerdude (filler files vector), Scam.net (exploit discovery pointers).

Targets (wizard mapping): KT5, PW5 firmware 5.18.1 - 5.19.2.0.1; KT4, PW4 firmware 5.18.1 - 5.18.1.1.1. (Table also lists SpringBreak for KT4/PW4 at 5.18.1.1.1, KT5/PW5 at 5.19.2(.0.1).)

How: PC binary writes thousands of nested folders (filler files) to Kindle over USB, then Kindle Store becomes exploit vector. **Filler files make this process FAIL if space too low — leave plenty of space, don't pre-fill like other methods.** Run fast. Cleanup step mandatory after (else 15+ min boot).

Steps:
1. Download `https://github.com/KindleModding/SpringBreak/releases/latest/download/springbreak.zip`
2. Airplane Mode on. Reboot.
3. Connect Kindle to PC via USB. Screen must match guide's USB screen exactly; 'disconnect' button = unsupported Kindle.
4. Unzip SpringBreak on computer.
5. Run binary: Windows double-click `springbreak.exe`; Linux `chmod +x ./springbreak-linux && ./springbreak-linux`; MacOS run whole snippet:
```
curl -L https://github.com/KindleModding/SpringBreak/releases/latest/download/springbreak.zip -o springbreak.zip && unzip springbreak.zip && cd springbreak && chmod +x ./springbreak-darwin && ./springbreak-darwin
```
(MacOS snippet auto-handles filling; no manual filler step.)
6. Select Kindle from device list (type number, enter). Kindle must be plugged in and mounted (Linux: open in file explorer to mount).
7. Binary fills Kindle with filler files. Windows takes longer than Linux.
8. Unplug. Home screen -> store icon. Turn off aeroplane when prompted — Wi-Fi needed for SpringBreak to load; turn off right after loaded.
9. Text appears; success screen follows.
10. Cleanup: plug Kindle back in at homepage after UI restarted, run binary again, select Kindle, it cleans up. **Skip = 15+ minute boots.**
11. Remove any `.bin` update files in root.

Troubleshooting: Store says 'Application Error' -> unplug/re-plug until works. Kindle not listed -> mount on Linux. Fill fails (space) -> delete some fillers, re-run script to delete old partial fillers, retry.

## Sanctuary

Released 30/06/2026 by Ava, Alysa (Sky), sparklerfish. No registration needed.

Targets (wizard mapping): PW4, KT4, KOA3, PW5, KT5, KS, KT6, PW6, KS2, CS. Firmware 5.16.4 - 5.18.3, denied outlier `5.16.5`. Credits: Ava found/engineered privesc (PW4 5.18.1.1.1 testing), sparklerfish JS+webpage (PW4 5.18.1 testing), Alysa JS dev + CS SE testing, Scam.net POC help + PW5 testing, HackerDude JB.sh help.

How: browser exploit. Port scan on hosted page reveals ID; enter ID; page downloads `appreg.db`, `appreg.db.bak`, `privesc.sh`; then Settings -> Help -> Getting Started triggers jailbreak. Application Errors expected.

Steps:
1. Fill device, read overview.
2. Kindle browser: `3 Dots → Web Browser`. Navigate to `http://sanctuary.skyvincent.com/scroll` — must be `http`, not `https`.
3. Wait for scrollbar to appear right. Compare to guide images. Left scrollbar = proceed. Right scrollbar = manually update firmware to latest jailbreakable version (firmware-and-flashing/downloading-updates.html).
4. Navigate to `http://sanctuary.skyvincent.com/`. Port scan starts automatically; up to 20 min, no interaction. Wait for ID.
5. Type exact ID into box (site auto-capitalizes; "0" = zeroes; chars only `0123456789ABCDEF`). Click "Connect".
6. Confirm "Downloads Done" at top + notifications for `appreg.db`, `appreg.db.bak`, `privesc.sh`. 1-2 popups only = normal.
7. Exit browser (X top right). **Do not disable Wi-Fi yet — needed until final step.**
8. 3 dots -> Settings -> Help menu.
9. Click "Getting Started". Text appears = success. Application Errors expected, ignore.
10. Delete filler files. Updates auto-blocked. Remove `.bin` update files in root.

## SpiderCat

Released 01/09/26 by sparklerfish. No PC needed. Entry point shared by fabrissou; privesc discovered by ava; Marek improved exploit.

Targets (wizard mapping): PW4, KT4, KOA3, PW5, KT5, KT6, PW6, CS, KS, KS2. Firmware 5.16.3 - 5.19.5. Guide summary: firmwares between 5.16.3 and 5.19.5.

How: malicious book. Book renders exploit; text flows from top; GUI restarts.

Steps:
1. Fill device, read overview.
2. Get book: sideload via USB — download `https://kindlemodding.org/spidercat/spidercat.azw3`, place in Kindle `documents` folder. Or Kindle browser — navigate to `https://kindlemodding.org/spidercat` and download.
3. Open book from Library. **Keep Wi-Fi on until final step.**
4. Wait. Blank page several seconds normal. Text flows down from top = exploit running. "Application error" popups = irrelevant.
5. "Restarting GUI" screen appears; may take several minutes; white screen normal. Returns to home = jailbroken.
6. Delete filler files. Updates auto-blocked. Remove `.bin` files in root.

Troubleshooting: "Restarting GUI" >=10 min -> hold power button, Restart. Nothing on first open -> ensure Wi-Fi on at open.

## Nosebleed

Released 02/03/2026 by hhhhhhhhh. Jailbreak guide by Penguins184; modified JB script by Hackerdude. Reported to work on some blacklisted devices. Ad-free kindles fine (guide flagged `adfree: true`).

Targets (wizard mapping): KT5, PW5, KOA3 firmware 5.16.4 - 5.18.6; PW6, KT6 firmware 5.16.4 - 5.17.1.0.4. Registration NOT required.

How: hosted page `https://kindlemodding.org/nosb` + two files copied to Kindle root. Press the "L" on Jeff Bezos' forehead on the page = trigger. Application Errors expected.

Steps:
1. Fill device, read overview.
2. Download `./nosebleed.zip` (hosted alongside guide on kindlemodding site).
3. Plug in Kindle, extract `nosebleed.zip` on PC, copy the two files inside to Kindle root.
4. Open browser (top right menu).
5. Navigate to `https://kindlemodding.org/nosb`.
6. Press the L on Jeff Bezos' forehead. Bang! Application Errors expected, ignore.
7. Delete filler files. Updates auto-blocked. Remove `.bin` files in root.

## Vera

Released 10/08/26 by Ava + sparklerfish. Website by sparklerfish; initial site idea by scam.net.

Targets: KT5, PW5, KT6, PW6, CS, KS, KS2. All firmwares up to 5.19.6 (wizard: 5.17.1 - 5.19.6; firmware above 5.17 below 5.19.6 missing from dropdown -> try nearest listed, not guaranteed). Port to KS3(NFL) and KSC firmware <=5.19.6 planned future.

How: two books downloaded from `https://kindlemodding.org/vera` — "Font Calibration" book + device-specific Véra book. Font/theme manipulation in "Aa" menu triggers exploit when Véra book opened.

Steps:
1. Fill device, read overview.
2. Note exact firmware: `3 Dots → Settings → Device options → Device info`. Value after "Kindle".
3. Browser `3 Dots → Web Browser` -> `https://kindlemodding.org/vera`.
4. Choose device if prompted. Select firmware from dropdown. (Firmware above 5.17 below 5.19.6 not listed -> try nearest above/below.)
5. Two download links appear. Click "Font Calibration" book link -> "Ok". Click device-specific Véra book link -> "Ok". Quit browser (X top right). Wait 2-3s after closing browser before next step. **Keep Wi-Fi on until final step.**
6. Open "Font Calibration" book in library. Tap top of screen; overlay appears; click "Aa".
7. Font menu at bottom: Font Family = Bookerly. Bold = 0. Size = maximum.
8. Layout menu (or Spacing): medium Spacing option; or Line Spacing = 2, then tap arrow top-left of spacing menu.
9. Themes menu (or Spacing): "Save current settings", "Save" to save theme. Exit book: tap top left corner 3x ("Home"/"Library").
10. Open "Véra" book in library. Text flows from top left; "RESTARTING GUI" screen pops up. Delete both books after. "Application error" popups = irrelevant. Stuck -> safe to hold power and reboot.
11. Delete filler files. Updates auto-blocked. Remove `.bin` files in root.

Book naming on server: `https://kindlemodding.org/vera/books/<device>-<firmware>-jb.azw3` (device slugs: cs, ks, ks2, kt5, kt6, pw5, pw6; font calibration book = `fontcal.azw3`; kt6 5.19.6 also ships `-touch.azw3` variant).

## AdBreak

Released 24/09/2025 by hhhhhhhhh. Based on CVE-2012-3748. Registration required. **Ad-enabled Kindle required** (wizard `ads: true`). Guide includes re-enabling ads on ad-free kindle (not permanent, can disable after).

Targets (wizard mapping): KOA3, PW5, KT5, KS, KT6, PW6 firmware 5.18.1 - 5.18.5.0.1; PW4, KT4 firmware exactly 5.18.1. (Summary: 5.18.1 - 5.18.5.0.1.)

How: replaces lockscreen ad `details.html` files in `.assets` folder with exploit HTML; clicking ad triggers jailbreak. jb.sh + patchedUks.sqsh must be present in `.assets`.

Steps:
1. Fill device, read overview.
2. Download `https://github.com/KindleModding/AdBreak/releases/latest/download/adbreak.zip`
3. Leave Kindle online so it downloads ads. Press lock button — ad should display. No ads after while -> factory reset may help.
4. Verify ads on lockscreen, then Airplane Mode on.
5. Top right menu -> "View all ads" (multiple "special offers").
6. Plug in. Open `system` folder; copy `.assets` folder to computer. (Mass-storage kindles: `system` hidden — navigate manually or show protected system folders.)
7. Unzip AdBreak; place extracted contents inside on-PC `.assets` copy.
8. Run replace script: Windows double-click `replace.bat`; MacOS/Linux terminal: `find . -name 'details.html' -exec cp adbreak.html {} \;`
9. Delete original `.assets` on Kindle; replace with modified copy.
10. Unplug. Click an ad, go through popups; click Close on "Bang!" -> jailbreak script runs. "Application error" popups = irrelevant. If "Bang!" shows but no jailbreak -> check `.assets` on Kindle contains `jb.sh` and `patchedUks.sqsh`.
11. Delete filler files. Updates auto-blocked. Remove `.bin` files in root.

Enabling ads (for ad-free kindle): Amazon account -> Manage Your Content and Devices -> Preferences -> Country/Region Settings -> Change; select US, UK, DE, FR, IT, ES, JP, CN, AU; valid details (address, phone, email). Add default credit card + billing address matching region (no charge expected). Enable Special Offers for Kindle. Sync kindle; Wi-Fi on; ads appear on lockscreen.

## LanguageBreak

Mobileread thread t=356872 by Marek. Exploits `langpicker-nativebridge` (discovered by GeorgeYellow + bulltricks). NOT work on firmwares newer than `5.16.2.1.1`. Check wizard compatibility. Factory reset involved (erases data — back up). Demo mode used.

How: factory reset -> enter demo mode -> sideload LanguageBreak files via demo menu -> pick Chinese language -> exploit triggers on language switch. Own hotfix (`update_hotfix_languagebreak.bin`) must install before other post-jailbreak items.

Steps:
1. Download LanguageBreak from `https://github.com/notmarek/LanguageBreak/releases/latest`. Extract `tar.gz` on PC.
2. Factory reset Kindle.
3. Language selection: any language. Skip Wi-Fi: select network then back out.
4. Type `;enter_demo` in searchbar, enter. Reboot (hold button -> reboot). Boots into demo mode.
5. Skip Wi-Fi, enter fake info. Skip demo payload search. Select `standard` demo type. `Done` at "sideload content".
6. Bypass `misconfiguration` error: two-finger tap, then swipe left (video: `https://www.youtube.com/watch?v=JzuIGbGPpig`).
7. Searchbar: `;demo`, enter. Select "sideload content".
8. Connect PC. Copy LanguageBreak folder contents to Kindle, merge + replace.
9. Eject/unplug. Demo menu: "Resell Device" -> Yes/Resell.
10. Wait for `press power button` message; immediately plug into PC, copy LanguageBreak folder contents again, overwrite, eject.
11. Hold power as instructed. Language menu appears in seconds.
12. Choose Chinese (second-last on right list, above `p s e u d o`).
13. Kindle reboots; log messages; jailbroken.

LanguageBreak hotfix (mandatory before other post-jailbreak):
1. `;uzb` in searchbar, enter. Connect PC.
2. Copy `update_hotfix_languagebreak.bin` from extracted tar.gz to Kindle root.
3. Eject/unplug. `;dsts` in searchbar, enter.
4. Select `Update Your Kindle`.

Troubleshooting: demo mode fails -> alternative: plug in, create empty file `DONT_CHECK_BATTERY` at root, `;demo` in searchbar, continue from initial-setup step 5. Reset while in demo mode: `;uzb`, plug in, create empty file `DO_FACTORY_RESTORE` at root, reboot.

## KindleBreak

Mobileread thread t=338268 by tryol; guide by Neon. Uses KindleDrip webkit exploit (writeup: `https://medium.com/realmodelabs/kindledrip-from-your-kindles-email-address-to-using-your-credit-card-bb93dbfb2a08`). NOT work on firmware `5.12.2.2`.

How: zip extracted to root + crafted `file__0.localstorage` planted in browser LocalStorage dir; open Experimental Browser -> freeze/crash -> reboot -> jailbroken.

Steps:
1. Airplane Mode on.
2. Download `jb-kindlebreak.zip` (hosted with guide). `MD5: 0215C36CC1E3AD8136A67DAEBE369452`.
3. Plug in Kindle. Extract zip to root (files next to documents folder).
4. Download `file__0.localstorage` (hosted with guide).
5. Place in `/.active_content_sandbox/browser/resource/LocalStorage/` on Kindle (create folders if missing; replace existing file).
6. Eject/unplug. Open Experimental Browser.
7. Browser freezes, crashes; Kindle reboots (up to 5 min). Error popup `Application Error` or `Collecting Debug Info` = expected.
8. Jailbroken -> Post Jailbreak section.

## Popcorn (KT2/KT3/KV/PW2/PW3)

Mobileread thread t=345655 by katadelos; guide by Neon. **Hardware** jailbreak: works on any firmware on supported hardware. Requires electronics experience; soldering iron recommended; steady hands; jumper cable; PC Linux or Windows (MacOS not supported). KV supports WatchThis on every firmware — prefer WatchThis over Popcorn when possible.

Models: PW3, KV, KT2, PW2, KT3 only.

Getting started Windows: install 7-Zip (`https://www.7-zip.org/`). PW2/PW3/KT2/KV files: `https://www.mobileread.com/forums/showpost.php?p=4217167&postcount=17`. KT3 files: `https://www.mobileread.com/forums/showpost.php?p=4288479&postcount=60`. Extract.
Getting started Linux: install `imx_usb_loader` via distro package manager. Download Popcorn Files: `https://www.mobileread.com/forums/attachment.php?attachmentid=198921&d=1673376193`. Extract.

Common flow all models: short test pads with wire, hard reboot (hold power 15s) while shorted, plug into PC -> device in `SDP Mode` ready to flash. Windows: double-click `MFGTool.exe` -> Start, wait. Linux: terminal in folder containing `imx_usb_loader` folder; `ls` should show it; run flash command below per model; wait.

- KT2: tear down to step 5 per `https://www.ifixit.com/Guide/Kindle+7th+Generation+Motherboard+Replacement/37917`. Wire `TP1706` to `TM401`. Linux: `sudo imx_usb -c imx_usb_loader/wario`
- KT3: tear down to 4:48 per `https://youtu.be/LVt2hyPBrnA`. Wire `TP1706` to `TM401`. **KT3 uses different Windows files than other models.** Linux: `sudo imx_usb -c imx_usb_loader/heisenberg`
- KV: tear down to step 5 per `https://www.ifixit.com/Guide/Kindle+Voyage+Screen+Replacement/37464`. Remove motherboard: unscrew from chassis, gently disconnect cables + battery. Wire `TM501` to `TM500`. Linux: `sudo imx_usb -c imx_usb_loader/wario`
- PW2: tear down to step 4 per `https://www.ifixit.com/Guide/Kindle+Paperwhite+2nd+Generation+Motherboard+Replacement/71196`. **DO NOT remove battery.** Wire right pad of `CR501` to `TP508` (ignore additional wires in image). Linux: `sudo imx_usb -c imx_usb_loader/wario`
- PW3: tear down to step 4 per `https://www.ifixit.com/Guide/Kindle+Paperwhite+3rd+Generation+Motherboard+Replacement/61696`. **DO NOT remove battery.** Wire right pad of `CR501` to `TP508`. Linux: `sudo imx_usb -c imx_usb_loader/wario`

Then Post Jailbreak section.

## WatchThis

Mobileread thread t=346037 by katadelos; guide by Neon. Demo payload exploit. **Erases all Kindle data — back up.**

How: factory reset -> demo mode -> sideload `[YOUR_DEVICE]-[YOUR_FIRMWARE].zip` (unextracted) + `demo.json` into `.demo/` -> install from demo menu -> trigger via Help -> Get Started. Own hotfix (`update_hotfix_watchthis_custom.bin`) mandatory before other post-jailbreak items.

Steps:
1. Factory reset.
2. Language: `en_GB` / English (United Kingdom). Skip Wi-Fi: select network, back out.
3. `;enter_demo` in searchbar, enter. Reboot (hold button -> reboot). Demo mode.
4. Skip Wi-Fi, fake info. Skip payload search. `standard` demo type. `Done` at "sideload content".
5. Bypass misconfiguration: two-finger tap + swipe left (video `https://www.youtube.com/watch?v=JzuIGbGPpig`).
6. `;demo` in searchbar, enter. "Sideload content".
7. Connect PC. Create `.demo` directory at Kindle root.
8. Download `watchthis-jailbreak-r03.zip` from `https://mega.nz/file/2ahlQKZS#jXyYLEp9rvRQCOzv7LNYBF-9fOfPhpigaLZMHZkN7fg`. Extract **on computer, not Kindle**.
9. Copy matching `[YOUR_DEVICE]-[YOUR_FIRMWARE].zip` into `.demo/` — **DO NOT EXTRACT**. Copy `demo.json` into `.demo/`. Create empty folder `.demo/goodreads`.
10. Eject/unplug. Select `Done` -> installs jailbreak. Application error -> hard reboot (hold power 15s+), re-enter demo mode, sideload content again; don't re-copy files.
11. Exit demo mode.
12. KT2 or PW2: press store button. All other models: `;dsts` in searchbar.
13. Help & User Guides -> Get Started. Reboots jailbroken.

WatchThis hotfix: `;uzb` searchbar -> connect PC -> copy `update_hotfix_watchthis_custom.bin` from extracted WatchThis zip to root -> eject/unplug -> `;dsts` -> Update Your Kindle.

Troubleshooting demo mode: empty file `DONT_CHECK_BATTERY` at root, `;demo`, continue from initial-setup step 7. Reset in demo mode: `;uzb`, empty file `DO_FACTORY_RESTORE` at root, reboot.

## NiLuJe K2/DX/DXG/K3 Jailbreak

By NiLuJe. Device codes: K2=02, K2I=03, DX=04, DXI=05, DXG=09, K3G=06, K3W=08, K3GB=0A. K2/DX/DXI/DXG/K2I: any firmware. K3*: firmware 3.0 - 3.4.3 (min inclusive, max exclusive): 3.0-3.2 builds `Update_jailbreak_k3{g,w,gb}_3.0-to-3.2_install.bin`; 3.3-3.4.3 builds `Update_jailbreak_k3{g,w,gb}_install.bin`.

How: serial-specific signed `.bin` installer applied through Settings -> Update Your Kindle.

Files hosted with guide:
- `k2/Update_jailbreak_k2_install.bin`, `k2/Update_jailbreak_k2i_install.bin`, `k2/Update_jailbreak_dx_install.bin`, `k2/Update_jailbreak_dxi_install.bin`, `k2/Update_jailbreak_dxg_install.bin` (+ `*_uninstall.bin` for each)
- `k3_3.0-3.2/Update_jailbreak_k3{g,w,gb}_3.0-to-3.2_install.bin`, `k3_3.0-3.2/Update_jailbreak_k3{g,w,gb}_uninstall.bin`
- `k3_3.2.1/Update_jailbreak_k3{g,w,gb}_install.bin`

Steps: page has serial+firmware search that highlights matching row. Copy `Update_jailbreak_0.13.N_[whatever]_install.bin` to Kindle. Delete any other `.bin` / `update.bin.tmp.partial`. Eject/unplug. `[HOME]` -> `[MENU]` -> Settings -> `[MENU]` -> Update Your Kindle. Reboot = jailbroken. Error `U006` normal on firmware 2.x, ignore.

No VERSION/README files present in k2/, k3_3.0-3.2/, k3_3.2.1/ dirs — only .bin installers/uninstallers.

## NiLuJe K4 Jailbreak

By NiLuJe. Payload mostly identical to yifanlu's jailbreak. K4 only (last firmware 4.1.4).

How: diags-mode exploit. Copy files, reboot into diagnostics via `ENABLE_DIAGS`, exit diags through menu sequence.

Steps:
1. Download `https://github.com/KindleModding/K4-Jailbreak/releases/latest/download/K4-Jailbreak.zip`
2. Extract; plug in Kindle; copy to Kindle: `data.tar.gz`, `ENABLE_DIAGS`, `diagnostic_logs`.
3. Eject/unplug.
4. Restart: `[MENU]` -> Settings -> `[MENU]` -> Restart. Boots into diagnostics mode.
5. 5-way keypad: `D) Exit, Reboot or Disable Diags` -> `R) Reboot System` -> `Q) To continue`.
6. ~20s restart; book titled `You are Jailbroken` in library = done.

## NiLuJe K5 Jailbreak

By NiLuJe. K5 (Kindle Touch) firmware 5.0.x - 5.4.4.2. Payload based on yifanlu's, Touch/PaperWhite tweaks, delivery by yossarian17.

How: update-package style jailbreak triggered via Settings -> Update Your Kindle.

Steps:
1. Download `./kindle-5.4-jailbreak.zip` (hosted with guide).
2. Extract; plug in; copy **ALL** extracted files to Kindle root.
3. Eject/unplug.
4. `[HOME]` -> `[MENU]` > Settings -> `[MENU]` > Update Your Kindle. `**** JAILBREAK ****` at bottom = jailbroken.
5. Manual reboot recommended for MKK components: `[HOME]` -> `[MENU]` > Settings -> `[MENU]` > Restart.
6. Next: setting-up-a-hotfix page.

## Post-jailbreak: hotfix

Hotfix = jailbreak persists after update. Two hotfixes exist; method determines which. **Skip if jailbroke via WinterBreak, SpringBreak, Sanctuary — hotfix pre-installed.** LanguageBreak/WatchThis need their own hotfix first (above). K5 jailbreak -> its hotfix page next.

Universal hotfix steps:
1. Download `https://github.com/KindleModding/Hotfix/releases/latest/download/Update_hotfix_universal.bin`
2. Plug in; copy `Update_hotfix_universal.bin` to Kindle root. Delete other `.bin` / `update.bin.tmp.partial`. Airplane Mode on.
3. If updates blocked via `renametobin` set to Rename: revert first (Restore), else hotfix won't install via Settings.
4. Eject/unplug. Settings -> three dots -> `Update Your Kindle`.
5. Confirm `Update`. Installs as update.
6. Run `Run Hotfix` booklet in library. Then install KUAL + MRPI. **Re-run hotfix booklet after every OTA update.**

Hotfix won't install (OTA disabled): 1) Airplane on. 2) KUAL -> Rename OTA binaries -> Restore. 3) Install hotfix. 4) KUAL -> Rename OTA binaries -> Rename.

## Post-jailbreak: KUAL + MRPI

KUAL (Kindle Unified Application Launcher) + MRPI (MobileRead Package Installer) run homebrew. Need 220 MB free to install (Airplane Mode on before freeing space, else OTA downloads). KUAL obsolete on modern hdnext jailbreaks — KPM/scriptlets replace it; but this legacy page still documents it.

Steps:
1. K5 and newer: download PEKI `https://github.com/KindleTweaks/PEKI/releases/latest/download/PEKI.zip`. K4 and older: download `./KUAL-KDK-1.0.azw2` (hosted with guide), place in documents, skip to KOReader install.
2. Download MRPI: modern devices `./kual-mrinstaller-khf.zip` (hosted with guide, provided by `https://fw.notmarek.com/khf/`); legacy pre-K5 devices `./kual-mrinstaller-1.7.N-r19303.zip`.
3. Extract MRPI; copy `extensions` and `mrpackages` folders to Kindle.
4. Unzip `PEKI.zip`; copy `KUAL.sh` + `KUAL.jar` to `documents` folder.
5. Eject/unplug. Open KUAL from library.

Troubleshooting: needs 220 MB free (fill-storage method users). Folders in right locations. Restart Kindle if `;log mrpi` not responding. Strip browser-added `(1)` suffixes from filenames.

## Post-jailbreak: disabling OTA (legacy)

Kindles auto-update on Wi-Fi; updates cause instability or remove jailbreak despite hotfix. **Skip if jailbroke via WinterBreak, SpringBreak, Sanctuary — OTA pre-blocked.**

Check firmware: Home → Menu → Settings → Device options → Device Info.

Firmware <=5.10.x: plug in; create folder named `update.bin.tmp.partial` in Kindle root; eject. Done. Restore: delete the folder.

Firmware >=5.11.x: download `./renameotabin.zip` extension (hosted with guide). Plug in. Unzip; copy `renameotabin` folder (inner-most if nested) to `extensions` on Kindle. Delete any `update.bin.tmp.partial`-like or `.bin` files. Eject/unplug. Open KUAL -> `Rename OTA Binaries` -> `Rename`. Kindle reboots. Restore (before factory reset/downgrade/update): KUAL -> `Rename OTA Binaries` -> `Restore`.

## Prevent auto-update (modern): fill storage

Updates download when free space suffices. Triggers: open Kindle Store, register, Wi-Fi even briefly, reboot while online. Fill disk to 50-90 MB free blocks update downloads.

Steps:
1. Airplane Mode on. Delete `update-whatever.bin` / `update.partial.bin`.
2. USB connect. Kindle appears as USB drive.
3. Download filler script: `https://github.com/bastianmarin/Kindle-Filler-Disk/` — Windows `Filler.ps1`, macOS/Linux `Filler.sh`. (11th gen and newer = MTP not USB storage: script won't work. Manually copy dummy files from `https://github.com/Crosunt223/Kindle-Filler-Disk/tree/main/MTP` matching storage size to root; leave 50-90 MB free.)
4. Copy script to Kindle root.
5. Run: Windows right-click `Filler.ps1` -> Run with PowerShell; execution-policy error -> `powershell -ExecutionPolicy Bypass -File .\Filler.ps1`. macOS/Linux: `chmod +x Filler.sh` then `./Filler.sh`.
6. Eject. Settings > Device Options > Device Info: available storage 50-90 MB or less.
7. Can now Wi-Fi/register; update can't fully download. Always delete `.bin` / `update.bin.tmp.partial` files.

After jailbreak: delete `fill_disk` folder to reclaim space (or some files to stay near-full). Linux/macOS: `rm -rf fill_disk`.

## Backing up (8th gen and older only)

Works: PW2, PW3, KT2, KT3, KV, KOA. KT4/PW4 and newer excluded: different partition layout + secure boot.

Prereqs: PC, jailbroken Kindle + KUAL, kterm (`https://github.com/bfabiszewski/kterm`), knc1's Kindle Backup Script (`https://www.mobileread.com/forums/showthread.php?t=289690`).

Steps:
1. Plug in. Download latest kterm (`https://github.com/bfabiszewski/kterm/releases/latest`); extract `kterm` folder into `extensions` on Kindle.
2. Extract `backup-0.3.tar.gz` on PC. Copy `esys` and `unjail` folders to Kindle root.
3. Eject/unplug. KUAL -> kterm:
```
cd /mnt/us/unjail
./mkbackup.sh
exit
```
(`./mkbackup.sh` takes minutes.)
4. Plug in. `backups` folder holds system images — copy somewhere safe.

## Restoring (8th gen and older only)

Prereqs: PC, soldering/electronics expertise, `1.8v` serial-to-USB adapter on Kindle, serial software e.g. PuTTY (`https://www.putty.org/`).

Steps:
1. Install PuTTY. Serial connection, baud `115200bps`.
2. Boot Kindle; interrupt boot: mash enter until `uboot >`.
3. `uboot >`: enter `boom 0xE41000` -> DIAGS.
4. DIAGS: `usb export` (exports userpace partition).
5. Copy RootFS image to Kindle, named `rootfs.img`. **Do NOT flash/write directly — just copy file.**
6. Eject but **DO NOT UNPLUG**.
7. Exit DIAGS: `x` at prompt, then `exit login` for shell.
8. `dd if=/mnt/us/rootfs.img of=/dev/mmcblk0p1 bs=4096`
9. `reboot`.

## Jailbreak wizard logic (jailbreak-wizard.html + jailbreakFinder.js)

Wizard: 4-step cards. Requires reading lander first: `localStorage.readLander` unset -> "Halt!" dialog.

1. Serial: enter first 8 digits (`Three Dots > Settings > Device options > Device info`). `getSerialInfo`: 2-3 char input -> old serial_version 0 / base32 serial_version 1; `G...` prefix (len>=6): serial_version 1, device_code = chars 3-6; hex-first-char (len>=4): serial_version 0, device_code = chars 2-4. Matches against `models.json` `device_codes` keys where `kindle.serial_version >= info.serial_version`. Sets `window.info.model` = generation_nickname. Enables Next on match.
2. Firmware: input sanitized to `[0-9.]`, validated `/^\d{1,2}(\.\d{1,2}){1,5}$/` (X.XX.[XX.XX.XX.XX]), major <= 5. Stored as string.
3. Blacklisted: can Kindle register? Yes -> `blacklisted=false`; No -> `true`.
4. Ads: lockscreen ads? Yes -> `ads=true`; No/unsure -> `false`.

`fillResults()`: fetches `jailbreaks.json`, filters:
- `jb.models` includes model nickname
- `jb.registration` true + user blacklisted -> excluded
- `jb.ads` true + user no ads -> excluded
- firmware rules: rule applies if `rule.models` includes "all" or model; denied outliers -> excluded; accepted outliers -> included; else `min <= firmware <= max` via segment-wise `versions()` compare.
First match = recommendation; rest listed as alternatives. No match -> "no jailbreaks available".

jailbreaks.json entries (name, models, firmware min-max, registration/ads flags): WinterBreak2 (PW PW2 KV KT2 PW3 KOA KT3 KOA2 PW4 KT4 KOA3 PW5 KT5 KS; 5.6.1.1-5.16.3, accepted 5.16.5; no reg/ads), SpiderCat (PW4 KT4 KOA3 PW5 KT5 KT6 PW6 CS KS KS2; 5.16.3-5.19.5), Véra (PW5 KT5 KT6 PW6 CS KS KS2; 5.17.1-5.19.6), Nosebleed (KT5 PW5 KOA3 5.16.4-5.18.6; PW6 KT6 5.16.4-5.17.1.0.4), Sanctuary (PW4 KT4 KOA3 PW5 KT5 KS KT6 PW6 KS2 CS; 5.16.4-5.18.3, denied 5.16.5), WinterBreak (PW PW2 KV KT2 PW3 KOA KT3 KOA2 PW4 KT4 KOA3 PW5 KT5 KS KT6 PW6 KS2 CS; 5.6.1.1-5.18.0.2; registration true), SpringBreak (KT5 PW5 5.18.1-5.19.2.0.1; KT4 PW4 5.18.1-5.18.1.1.1; registration true), AdBreak (KOA3 PW5 KT5 KS KT6 PW6 5.18.1-5.18.5.0.1; PW4 KT4 exactly 5.18.1; registration + ads true), NiLuJe K2/DX/DXG/K3 (K2 DX K3; 2.0.0-4.0.0), NiLuJe K4 (K4; 2.0.0-5.0.0), NiLuJe K5 (KT; 5.0.0-5.4.4.2), LEGACY (K1; 0.0.0-2.0.0), Android methods (KM; 0.0.0-999.0.0).

## Kindle models table logic (modelsTable.js + models_json_generator.py)

`models_json_generator.py` builds `models.json` from two sources: `model_tuples` (KindleTool commit 708d71a: kindletool name, hex device code, Amazon model ID) + `generationMap` (per generation: release year/firmware, generation_nicknames e.g. PW5/KT6/CS/KS2, amazon_name, last_firmware, platform, board, jailbreak links). Serial codes: 2-digit hex -> old serial_version 0; 3-digit -> base32 serial_version 1 via katadelos magic-int reverser (`serial_to_int`/`int_to_serial`, CHARS=`0123456789ABCDEFGHJKLMNPQRSTUVWX`). Output per model: generation_nickname, nicknames, serial_version, device_codes {code: {kindletool_name, amazon_model_id}}, jailbreak HTML links.

`modelsTable.js`: fetches `models.json`, builds table columns: Amazon Name, Kindle Nickname, Latest Firmware, Recommended Jailbreak, KindleTool Variants (device_codes JSON). Appends to `#fullModelTable`. kindle-models.html currently just redirects to jailbreak-wizard.html.

Generation -> recommended jailbreaks (from generationMap): KT6/PW6: Sanctuary 5.16.4-5.18.3, WinterBreak <5.18.1, AdBreak 5.18.1-5.18.5.0.1 (KS2/CS add WinterBreak, no AdBreak for CS? CS: Sanctuary + WinterBreak). KS (Scribe 2022): Sanctuary, WinterBreak2 <5.16.4, WinterBreak <5.18.1, AdBreak 5.18.1-5.18.5.0.1. KT5/PW5: Sanctuary, WinterBreak2 <5.16.4, WinterBreak <5.18.1, SpringBreak 5.19.2(.0.1), AdBreak 5.18.1-5.18.5.0.1. KOA3: Sanctuary, WinterBreak2 <5.16.4, WinterBreak <5.18.1. KT4/PW4: Sanctuary, WinterBreak2 <5.16.4, WinterBreak <5.18.1, SpringBreak 5.18.1.1.1, AdBreak 5.18.1-5.18.5.0.1. KOA2/KT3/KOA/PW3/KV/KT2/PW2/PW: WinterBreak2 <5.16.4, WinterBreak. K5: K5 JailBreak 5.0.x-5.4.4.2. K4: NiLuJe K4. K3/DX/K2: NiLuJe K2/DX/DXG/K3. K1: LEGACY. KM (Kindle x Migu): runs Android, try Android methods.

## Bypassing OOBE

Some Kindles (Scribe, Colorsoft) can't skip registration at setup. Blacklisted/unregistered device stuck in OOBE.

Steps: go to captive-portal WiFi (coffee shop). Don't connect yet. In portal browser searchbar type `;demo`, submit. Press **NO** on demo mode dialog (YES = stuck in demo limbo). Hit Home tab. Kindle usable: settings, WiFi, browser — jailbreak per wizard. Fill storage before WiFi if applicable. After jailbreak: run `./disable_oobe.sh` scriptlet (removes `/var/local/decanter/RESUME_OOBE_FOR_OTA` + `/var/local/decanter/OTA_START_FOR_METRIC`, reboots). Skip scriptlet = repeat captive-portal trick every reboot.

`disable_oobe.sh`:
```sh
#!/bin/sh
# Name: Disable OOBE
# Author: KindleModding

echo "Removing OOBE marker files..."
rm -f /var/local/decanter/RESUME_OOBE_FOR_OTA
rm -f /var/local/decanter/OTA_START_FOR_METRIC
echo "Rebooting... (5s)" 
sleep 5
reboot
```

## Recovering from reset

Factory reset with blocked updates prevents installing official updates (needed to fully remove jailbreak traces). Install `./ota.sh` scriptlet first.

`ota.sh` (Restore Updates): finds chattr (`/bin/chattr`, or `/bin/chattr.e2fsprogs` on KT6 5.18.1.5+ and PW6/KS/KS2 5.18.5+); `mntroot rw`; `chattr -i /usr/bin/otaupd.bck /usr/bin/otav3.bck`; `mv /usr/bin/otaupd.bck /usr/bin/otaupd`; `mv /usr/bin/otav3.bck /usr/bin/otav3`; `mntroot ro`; reboot.

Stuck on "Update Failed" after foolish reset: FTVDB `https://ftvdb.com/kindle/firmware/` (FTVDB names differ: KT6 = Basic 5; PW numbers same). Download .bin -> USB root. Eject/unplug. Reboot, update installs. Kindle fully unjailbroken; re-jailbreak via wizard.

Un-jailbreak proper: re-enable updates (renametobin Restore), factory reset, install same-or-higher firmware update file (FTVDB), update button.

## FAQ notes

- Firmware newer than any jailbreak: no jailbreak; wait weeks/months. Forget saved networks, Airplane Mode, wait.
- Downgrade without jailbreak: no (Amazon provides no downgrade path on stock).
- Unregistered/blacklisted: Nosebleed works for some. FW <=5.16.2.1.1: try Legacy methods.
- Deregister after jailbreak: stays jailbroken; deletes documents folder (KUAL booklet, scriptlets) — back up first.
- Amazon account bans: none reported. Don't tell support device modified.
- Soft-float vs hard-float: 5.16.3+ = hard-float (on-chip FPU). Many MobileRead/Discord extensions unusable across boundary (NiLuJe Screensaverhack exception). No screensaver extensions on hard-float; soft-float: NiLuJe screensaver hack (`https://www.mobileread.com/forums/showthread.php?t=195474`).
- Check jailbroken: type `;log` in searchbar; popup = jailbroken.
- KUAL dead: `;log` popup -> reinstall hotfix+KUAL from scratch; no popup -> re-jailbreak via wizard; else factory reset + start over.
- `Failed to remount rootfs RO, waiting`: expected; manual reboot fine.
- Random `KPPMainAppV2` books: Kindle generates after errors (common exiting KOReader frameworkless); safe to delete. Disable: create empty file `DISABLE_CORE_DUMP` at USB storage root.
- "Update Your Kindle" greyed / can't update after reset: renametobin left enabled -> see recovering-from-a-reset.
- Root directory = first dir on USB; `/mnt/us/` over SSH.
- Update/factory reset/downgrade after jailbreak: Airplane Mode on + re-enable updates (renametobin Restore) first; ensure target firmware has jailbreak; reinstall hotfix after; KUAL/extensions may need reinstall.
- Long airplane mode then WiFi reconnect: Amazon may delete sideloaded books (internal tag) — back up books.

## Modern post-jailbreak: scriptlets, KPM, KOReader

Scriptlets: `.sh` files in documents folder appear as books; click to run. Malware warning: unknown sources can brick.

KPM: on-device package manager via searchbar commands: `;kpm install`, `;kpm update`, etc. Repo: `https://repo.kindlemodding.org/`. Popular homebrew list: `https://github.com/KindleTweaks/Awesome-Kindle`.

KOPlugins: copy into `/koreader/plugins` over USB, or AppStore KOPlugin (e.g. Storefront `https://github.com/ultimatejimmy/storefront.koplugin`).

Getting KOReader: reboot if just jailbroke; Wi-Fi on. `;kpm update` in searchbar. `;kpm install koreader`. Click booklet or `;kpm launch koreader`. Uninstall: `;kpm uninstall koreader`.

KOReader launch options: "Start KOReader" (normal), "Start KOReader (no framework)" (kills Kindle UI for resources), "Start KOReader (ASAP)" (skips checks). KOReader lacks USBMS — only charges; exit KOReader for file transfer. KOReader doesn't read Amazon KFX/AZW3 (limited MOBI) — use EPUB. KOR booklet launcher (yparitcher): `https://github.com/yparitcher/KUAL_Booklet/releases/`. Mareks launcher/scriptlets: `https://scriptlets.notmarek.com/`. Check OTA status scriptlet: `https://scriptlets.notmarek.com/`.

## Serial checker (serial_checker.py)

Offline Python mirror of site jailbreak wizard. Serial -> model. Optional firmware -> jailbreak matches. No network, stdlib only, `screen()` importable.

Serial parse (mirrors `getSerialInfo`): len 2/3 = whole serial is device code (version 0/1). Starts `G`: chars 3-5 = code, version 1. Starts 0-9/A-F: chars 2-3 = code, version 0. Else invalid. Uppercase, strip spaces.

Usage: `python3 serial_checker.py SERIAL [FIRMWARE] [--blacklisted] [--ads] [--json]`. `--blacklisted` = can't register to Amazon (drops registration-required jailbreaks). `--ads` = lockscreen ads (AdBreak needs it). Exit 0 model found, 1 not.

190 device codes, 28 models, 13 jailbreak rule sets embedded. Data snapshot 2026-09-25 from site source. Refresh: rerun models_json_generator.py + compose step.
