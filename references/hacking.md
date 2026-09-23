# Kindle Hacking

For jailbreak developers: how jailbreaking works under hood.

## Jailbreak mechanism

Root code execution achieved → jailbreak does:
1. Mount rootfs rw.
2. Install developer keys in /etc/uks or /etc/uks.sqsh.
3. Create /PRE_GM_DEBUGGING_FEATURES_ENABLED__REMOVE_AT_GMC (enables debugging features).
4. Create /MNTUS_EXEC (makes Kindle mount /mnt/us).
5. Mount rootfs ro.

Prepares system for hotfix.

## Debug commands

Run in search bar: `;dm`, `;kmclog`, `;711`, `;log mrpi`. Usually start with `;` — not required (freset needs none).

Defined in three files:
- /app/kpp_app_cmds.json
- /usr/share/app/kpp_sys_cmds.json
- /usr/share/webkit-1.0/pillow/debug_cmds.json (no longer exists)

Type command, hit enter → Kindle looks it up, runs mapped script. Arguments passed like shell (`;test 1 2 3` → `$1`,`$2`,`$3` = 1,2,3).

;log used as MRPI install command (old firmware shipped stock ;log, overwritten by jailbreak; now added/installed entirely by hotfix).

### kpp_sys_cmds

| Search Command | Command | Description |
|---|---|---|
| `;enter_demo` | `/usr/bin/createDemoModeFlagFile.sh` | Enter demo mode |
| `;exit_demo` | `/usr/bin/deleteDemoModeFlagFile.sh` | Exit demo mode |
| `;vfd` | `/usr/bin/verifyDemo.sh` | |
| `;dm` | `/usr/bin/dm.sh` | Dumps system messages and logs to /mnt/us/documents |
| `;311` | `/usr/bin/311.sh` | Change carrier settings |
| `;411` | `/usr/bin/411.sh` | Server information |
| `;611` | `/usr/bin/611.sh` | WAN information (3G) |
| `;711` | `/usr/bin/711.sh` | WiFi information |
| `;st` | `/usr/bin/dateTime.sh` | Set date: `date -D "%F %H:%M" +%s -d "$1 $2"` |
| `;shpm` | `/usr/sbin/shipping_mode` | Shipping mode |
| `;un` | `/usr/local/bin/usbnetwork.sh start` | |
| `;uns` | `/usr/local/bin/usbnetwork.sh stop` | |
| `;debugOn` | `/usr/bin/debugOn.sh` | |
| `;debugOff` | `/usr/bin/debugOff.sh` | |
| `;bsalogoff` | `/usr/bin/bsaLogOff.sh` | |
| `;bsalogon` | `/usr/bin/bsaLogOn.sh` | |
| `;wmtlog` | `/usr/bin/wmtLog.sh` | |
| `;uzb` | `/usr/bin/enableUSBInDemo.sh` | Enable USB file management in demo mode |
| `;dsts` | `/usr/bin/startSettingsInDemo.sh` | Open settings in demo mode |
| `;updateCamp` | `/usr/bin/updateCamp.sh` | |
| `;wwreset` | `/usr/bin/wwReset.sh` | |
| `;demo` | `/usr/bin/demoConfig.sh` | |
| `;duzb` | `/usr/bin/disableUSBInDemo.sh` | |
| `;chkup` | `/usr/bin/checkUpdate.sh` | |
| `;ledon` | `/usr/bin/turnOnLed.sh` | |
| `freset` | `/bin/sh -c /usr/sbin/factory_reset` | Factory reset, no `;` needed |

### kpp_app_cmds

/app/tools only ships on internal-use prototype Kindles.

| Search Command | Command |
|---|---|
| `;framer` | `/app/tools/framerTool.sh` |
| `;launcher` | `/app/tools/launcher.sh` |
| `;ui` | `/app/tools/altNLevel.sh` |
| `;term` | `/app/tools/kterm.sh` |
| `;kppchrome2` | `/app/tools/switchChrome.sh kpp 2` |
| `;kppstore` | `/app/tools/switchChrome.sh kppstore` |
| `;debugon` | `/app/tools/enableKPPDebugMenu.sh true` |
| `;debugoff` | `/app/tools/enableKPPDebugMenu.sh false` |
| `;lightbox` | `/app/tools/lightboxMode.sh` |
| `;odac` | `/app/tools/switchODAC.sh` |
| `;cpuProfilerOn` | `/app/tools/cpuProfiler/start_polling.sh` |
| `;cpuProfilerOff` | `/app/tools/cpuProfiler/stop_polling.sh` |
| `;kidsjava` | `/app/tools/enableKPPAmazonKids.sh false` |
| `;kidskpp` | `/app/tools/enableKPPAmazonKids.sh true` |
| `;enable2x` | `/app/tools/enable2xScaling.sh true` |
| `;disable2x` | `/app/tools/enable2xScaling.sh false` |
| `;default2x` | `/app/tools/enable2xScaling.sh default` |
| `;enablePerPageExport` | `/app/tools/enablePerPageExport.sh gamma` |
| `;disablePerPageExport` | `/app/tools/enablePerPageExport.sh prod` |
| `;enableHiddenPDF` | `/app/tools/enableHiddenPDF.sh gamma` |
| `;disableHiddenPDF` | `/app/tools/enableHiddenPDF.sh prod` |
| `;stylusDataOn` | `/app/tools/stylusDataPoints.sh true` |
| `;stylusDataOff` | `/app/tools/stylusDataPoints.sh false` |
| `;stroke` | `/app/tools/strokeSampleApps.sh` |
| `;kppreader` | `/app/tools/useKPPReader.sh true` |
| `;javareader` | `/app/tools/useKPPReader.sh false` |
| `;defaultreader` | `/app/tools/useKPPReader.sh default` |
| `;syncweblab` | `/app/tools/syncweblab.sh` |
| `;summaryon` | `/app/tools/useScribeAI.sh summary true` |
| `;formaton` | `/app/tools/useScribeAI.sh format true` |
| `;summaryoff` | `/app/tools/useScribeAI.sh summary false` |
| `;formatoff` | `/app/tools/useScribeAI.sh format false` |
| `;aion` | `/app/tools/useScribeAI.sh ai true` |
| `;aioff` | `/app/tools/useScribeAI.sh ai false` |
| `;fabricDemo` | `/app/tools/launchKppFabricDemoApp.sh` |

## Hotfix

Essential to jailbreaking. Distributed as OTA file — why jailbreaks install new OTA keys first. Homebrew OTA signing private key in KindleTool create.c L49 (URL in firmware draft).

Universal Hotfix layout:
```
.
├── install.sh
├── kmc.tar
├── libotautils6
├── mkk.tar
├── update-filelist.dat
```
Special OTA type: Kindle runs every .sh file inside when installing. Here: install.sh.

install.sh sources libotautils6 helpers, then:
- Measures space used by /var/local/kmc and /var/local/mkk (if exist).
- Checks enough free space (kmc/mkk subtracted since replaced). Errors out if not.
- Creates /var/local/kmc and /var/local/mkk.
- Extracts mkk.tar and kmc.tar into /var/local.
- Sets permissions for libs/binaries in /var/local/kmc.
- Deletes old bridge.conf upstart file.
- Copies kmc.conf upstart file (runs on framework_ready; runs /mnt/us/emergency.sh if exists, else verifies/fixes /var/local/kmc permissions).
- Symlinks /var/local/kmc/armhf/bin → /var/local/kmc/bin, /var/local/kmc/armhf/lib → /var/local/kmc/lib.
- Links gandalf → su (gandalf = busybox build; must be named su to work as privesc).
- Links gandalf to MKK persistent storage (/var/local/mkk/).
- Copies dispatch.sh debug command to /usr/bin/logThis.sh.
- chmod +x /var/local/kmc/KMCLog.sh.
- Replaces old run_bridge.sh with Run Hotfix.run_hotfix.
- Modifies appreg.db: installs hotfix booklet + sh_integration.

Run Hotfix booklet (final stage, can't run in OTA env): checks Kindle arch, runs correct su binary to elevate hotfix job runner. Job runner: iterates every job, runs it, restarts lab126_gui. Jobs: https://github.com/KindleModding/Hotfix/tree/rewrite-lite/src/kmc/hotfix/jobs. Notable: install_mkk_dev_keystore.sh (Java keystore for legacy booklets like KUAL), install_mkk_kindlet_jb.sh (legacy jar for Kindlets, no longer needed), setup_fbink.sh (copies fbink binaries to expected location).

## appreg.db

/var/local/appreg.db — sqlite3. Stores file-application relations and config. Tables: associations, extenstions (spelt that way in db), handlerIds, interfaces, mimetypes, properties.

associations: links handlers ↔ content/interface. Scanner uses it to pick extractor; also picks app for opening booklet.

Handler → interface mappings (selected): com.lab126.adRotationManager|kaf-service, com.lab126.purchaseManager|kaf-service, com.lab126.todo.handler.PurchaseConfirmation|todo|TP:legacy.SET.PRCH, com.amazon.kindle.booklet.ad|application, com.lab126.adManager|kaf-service, com.lab126.todo.handler.AdReset|todo|TP:legacy.SET.ADRS, com.lab126.todo.handler.AdPackage|todo|TP:legacy.DOWNLOAD.ADPK and TP:legacy.REMOVE.ADPK, com.lab126.sdk.addressbook|kaf-service, com.lab126.booklet.oobe.tutorial|application, com.lab126.audible.WSMarketplaceService|kaf-service.

Extractor mappings: com.lab126.audible.extractor→GL:*.aax, com.lab126.generic.extractor→GL:*.txt, com.lab126.mobi.extractor→GL:*.mobi, GL:*.pobi, GL:*.prc, GL:*.azw, com.lab126.mobi8.extractor→GL:*.azw3, com.lab126.pdf.extractor→GL:*.pdf, com.lab126.topaz.extractor→GL:*.tpz, GL:*.azw1, com.lab126.yj.extractor→GL:*.yj, GL:*.azw8, GL:*.kfx, org.kindlemodding.hd_extractor→GL:*.DO_NOT_DELETE, com.lab126.generic.extractor→GL:*.run_persistence, com.notmarek.shell_integration.extractor→GL:*.sh, com.lab126.generic.extractor→GL:*.run_hotfix. All defaultAssoc=true.

Application mappings: com.lab126.booklet.reader→MT:application/pdf, MT:application/x-kfx-ebook, MT:application/x-mobi8-ebook, MT:application/x-mobipocket-ebook, MT:application/x-topaz-ebook; com.lab126.booklet.test→MT:application/x-amazon-testrunner; com.lab126.booklet.periodicals→MT:application/x-mobipocket-subscription, -feed, -magazine.

handlerIds: single-column table (com.lab126.adRotationManager, com.notmarek.shell_integration.launcher, com.notmarek.shell_integration.extractor, com.lab126.kft, com.lab126.oobe, ... — not exhaustive).

interfaces (8): kaf-service, todo, application, download, detail, extractor, indexer, amazon-messaging.

extenstions (ext → mimetype): aax→MT:audio/vnd.audible.aax, pobi→MT:application/x-mobipocket-subscription (-subscription-magazine, -subscription-feed), azw→MT:application/x-mobipocket-ebook, mbp→MT:application/x-mobipocket-sidecar, azw3→MT:application/x-mobi8-ebook, azw6→MT:application/x-mobi8-images, kfx→MT:application/x-kfx-ebook, han→MT:application/json, azw1→MT:application/x-topaz-ebook, tan→MT:application/x-topaz-sidecar, pdf→MT:application/pdf, txt→MT:text/plain, jpg→MT:image/jpeg, apnx→MT:application/x-apnx-sidecar, phl→MT:application/xml+phl, sa→MT:application/xml+sa, ea→MT:application/xml+ea, none→MT:application/x-kindle-oobe, MT:application/x-kindle-vocab-builder, MT:application/x-kindle-collection, MT:application/x-kindle-pvc, MT:application/x-kindle-series, runtest→MT:application/x-amazon-testrunner, DO_NOT_DELETE→MT:text/hd_extractor, html→MT:text/html, run_persistence→MT:kindlemodding/run_persistence, sh→MT:text/x-shellscript, run_hotfix→MT:kindlemodding/run_hotfix.

mimetypes: purpose unknown; similar to extenstions. Extra rows vs extenstions: AAX→MT:audio/vnd.audible.aax, mobi→MT:application/x-mobipocket-ebook, prc→MT:application/x-mobipocket-ebook, azw8→MT:application/x-kfx-ebook, yj→MT:application/x-kfx-ebook, tpz→MT:application/x-topaz-ebook, jpeg→MT:image/jpeg, htm→MT:text/html.

properties: handler properties. Also stores dconf under dcc/dcd handlerIds.

sh_integration props (com.notmarek.shell_integration.launcher): extend-start=Y, unloadPolicy=unloadOnPause, maxGoTime=60, maxPauseTime=60, maxUnloadTime=60, maxLoadTime=60, command=/var/local/kmc/bin/sh_integration_launcher. Extractor: lib=/var/local/kmc/lib/sh_integration_extractor.so, entry=load_extractor.

mobi8 extractor (com.lab126.mobi8.extractor): lib=/usr/lib/ccat/libmobi8extractorE.so, entry=load_mobi8_extractor.

Home booklet (com.lab126.booklet.home): lipcId=com.lab126.booklet.home, jar=/opt/amazon/ebook/booklet/home.jar, supportedOrientation=U, default-chrome-style=TSB, maxExecTime=22, maxLoadTime=40, maxGoTime=30, defaultContext=context=0, extend-start=Y, detailFactoryPath=/opt/amazon/ebook/booklet/home.jar, detailFactoryClass=com.amazon.kindle.home.detail.HomeDetailViewFactory, whisper-touch=supported, asr=supported.

tardis (com.lab126.tardis): lipcId=com.lab126.tardis, jar=/opt/amazon/ebook/booklet/tardis.jar, supportedOrientation=U.

Reader booklet (com.lab126.booklet.reader): asr=supported, default-chrome-style=NH, detailFactoryClass=com.amazon.ebook.booklet.reader.impl.detail.ReaderDetailViewFactory, detailFactoryPath=/opt/amazon/ebook/lib/detail_view.jar, downloadHandlerClass=com.amazon.ebook.booklet.reader.impl.todo.handler.ContentToDoHandler, downloadHandlerPath=/opt/amazon/ebook/lib/ReaderSDK-impl.jar, extend-start=Y, grip-suppression=supported, jar=/opt/amazon/ebook/booklet/Reader.jar, lipcId=com.lab126.booklet.reader, maxGoTime=30, maxPauseTime=60, searchbar-mode=transient, supportedOrientation=URL, whisper-touch=supported.

dconf props: dcc wan.proxy.non_proxy_hosts.http/https = *.amazon.com.au|*.amazon.com|*.images-amazon.com|*.amazon.co.uk|*.amazon.de|*.amazon.fr|*.amazon.es|*.amazon.it|*.amazon.co.jp|*.amazon.ca|*.amazon.com.br|*.amazon.cn|*.amazon.in|*.amazon.eu|*.amazon.com.mx; dcd url.kindlestore.kcw.metrics=/mn/kcw/workflow/log-metrics; dcd url.store=https://www.amazon.com/gp/digital/juno/index.html; dcd url.unifiedsearch.kindlestore.voltron=$WEBSITE/kindle-dbs/ekws/?action=search&query=$SEARCH_TERM&locale=$LOCALE&page=$OFFSET&size=$SIZE&styleCode=$STYLE_CODE.

## cc.db

/var/local/cc.db — used by com.lab126.ccat. Stores indexed books and collections. Page draft, details pending.

## Usermode boot process

Kindle usermode boot = upstart. Diagram generated from PW6's upstart services.

upstart-diagram.py: mermaid generator. Reads .conf files in ./mnt/etc/upstart. Parses `start on` statements: handles and/or, parenthesized groups (recursive), RESULT tokens, job-reference events (started/starting/stopped/stopping — param = job name), parameter events (started/starting/stopped/stopping + runlevel — param captured). Parses `emits` lines and f_emit/initctl emit invocations to map events → emitting job. Writes ./upstart.md: `flowchart TD` with one node per job and edges eventSource -->|eventName[_param][ - RESULT]| jobName. Non-job events resolve via emits register, else raw event name as source.

## Prototype Kindles

Developer-only Kindles exist; some team members found and purchased them (thanks scam.net, Marek, Ygjsz).

Developer firmware ships /app/tools — lab126 internal tools, incl. kterm. Utilities like screenControl came from here.

Firmware dumps:
- scribe_diags_full_dump.7z (Ygjsz): https://archive.org/details/scribe_diags_full_dump.7z, https://hackerdude.tech/vault/kindle-firmwares/scribe_diags/scribe_diags_full_dump.7z
- PW5_Dev_5.14.0_3741660014_initialdumpfromlinux.img.xz (scam.net): https://archive.org/details/pw-5-dev-5.14.0-3741660014-initialdumpfromlinux.img, https://hackerdude.tech/vault/kindle-firmwares/PW5_dev_firmware/PW5_Dev_5.14.0_3741660014_initialdumpfromlinux.img.xz

## Models table

Page placeholder: table rendered client-side by ../modelsTable.js (KindleTool info). No static content.
