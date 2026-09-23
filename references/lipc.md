# Kindle LIPC services

LIPC = Kindle's lightweight IPC, custom system built on DBus. Services expose named properties.

## Usage

- `lipc-set-prop <service> <property> <value>` — set property
- `lipc-get-prop <service> <property>` — read property
- Dump values wrapped in `[]` — strip brackets when writing
- `lipc-set-prop com.lab126.powerd preventScreenSaver 1` disables screensaver
- `lipc-set-prop com.lab126.appmgrd start app://com.lab126.booklet.home` opens home app
- `lipc-get-prop com.lab126.btfd isBtchRunning` checks BT state
- Find owning pid: `dbus-send --system --print-reply --dest=org.freedesktop.DBus / org.freedesktop.DBus.GetConnectionUnixProcessID string:<service>` then `ps -p <pid>`

## Source notes

- `_lipc.txt` — raw lipc-probe dump: service names + property rows (access r/rw/w, type, value). No descriptions.
- `_lipcParser.py` — parses `_lipc.txt`, fills `_template.md` per service, writes one `.md` doc each. Zero-property services marked `APP/SERVICE DOES NOT USE LIPC`. All descriptions `TODO` in source — purposes below derived from property names.

## Device (power, volume, hardware)

- `com.lab126.powerd` — power daemon: suspend/wake, battery state/level/temp, frontlight intensity, screensaver timeout, power button
- `com.lab126.volumd` — volume daemon: userstore mount/unmount, free/total space, drive mode, USB networking
- `com.lab126.deviced` — hardware events: USB audio connect, touch enable
- `com.lab126.quickactions` — quick-settings actions: airplane-mode toggle, sync-and-check

## Network (wifi, connection)

- `com.lab126.wifid` — wifi daemon: profiles, connect/disconnect, scan, signal strength, certificates
- `com.lab126.cmd` — connection manager: interfaces, wireless enable, active interface
- `com.lab126.linux.arm.connectionutilities` — connection-event hooks: wifi popup, captive portal, wireless on
- `com.lab126.tphv3` — TPHv3 session/state debug counters

## Ads (soda / special offers)

- `com.lab126.adManager` — special-offers ad lifecycle: impressions, clicks, ad-file ingest, forced visible ad
- `com.lab126.adRotationManager` — screensaver ad rotation: current/next ad, rotation controller
- `com.lab126.blanket.ad_screensaver` — ad screensaver blanket: showing state, active button coordinate

## Content (bookstore, library, downloads)

- `com.lab126.merchant` — merchant entries: remove, removeAll, shuffle
- `com.lab126.wishlist` — wishlist cache refresh
- `com.lab126.archive` — cloud archive: transfer progress, todo handling
- `com.lab126.bookcacher` — book caching trigger
- `com.lab126.coverArtService` — cover art download/refresh, dimensions
- `com.lab126.contentpackd` — content packs: font install/scan, keyboard install, fonts mounted state
- `com.lab126.readnow` — open book ("read now")
- `com.lab126.booklet.home` — home library booklet: sort/view/filter controls, go/load/unload
- `com.lab126.booklet` — run/kill generic booklets
- `com.lab126.sharing` — book sharing: share events, text, messages
- `com.lab126.scanner` — watches /mnt/us, indexes books via extractors registered in appreg.db
- `com.lab126.extractor.java` — manage Java scanner extractors: add/delete/update
- `com.lab126.indexer` — full-text indexer: pause/resume, state dump, index-and-search
- `com.lab126.yjlipclistener` — disable YJ indexer
- `com.lab126.transfer` — transfer queue: downloads/uploads, dequeue, queue dump, obliterate
- `com.lab126.transferService` — transfer progress notifications
- `com.lab126.refreshCache` — refresh-cache orchestrator: run/status per client
- `com.lab126.dsus` — device software update: reportVersion

## System (init, appmgr, daemons, config)

- `com.lab126.system` — system info/control: version, GUIDs, date, screenshots, debug commands, VoiceView, e-ink waveform
- `com.lab126.appmgrd` — app manager daemon: load/run/stop/pause booklets, active app + pid
- `com.lab126.lxinit` — init system; exposes no LIPC
- `com.lab126.pmond` — process monitor: kill/restart, memory watch, heartbeat start/stop
- `com.lab126.kaf` — Kindle app framework (Java): heap dumps, timezone, framework start state
- `com.lab126.todo` — todo daemon: schedule/enable/disable todo items, wifi-portal response hooks
- `com.lab126.todo.kaf` — Java todo item handler
- `com.lab126.stored` — stored-content daemon: run/kill/restart, cache refresh, ready state
- `com.lab126.dynconfig` — dynamic config: todo handling, transfer progress
- `com.lab126.kwis` — KWIS daemon control
- `com.lab126.kwis.weblabTreatments` — WebLab AB experiment treatments
- `com.lab126.legalComplianceService` — GDPR compliance value
- `com.lab126.tutorialService` — clear tutorial status

## Reader (reading, typography, search)

- `com.lab126.reader.languagelayer` — reader language layer reset
- `com.lab126.reader.languagelayer.pinyin` — pinyin language layer reset
- `com.lab126.reader.qa` — typography QA: font styles, size, boldness, line spacing
- `com.lab126.reader.readingtimer` — reading progress type: location/page/time-left
- `com.lab126.readingstreams` — reading streams: context show/hide/open, actions, settings
- `com.lab126.LocalizationServices` — dictionaries, content-pack language updates
- `com.lab126.grokservice` — Grok AI search requests, link state, cache flush
- `com.lab126.instantSearch` — instant search: requests, suggestions, search init

## Input/UI (keyboard, winmgr, dialogs)

- `com.lab126.keyboard` — on-screen keyboard: language, bounds, open/close, preedit
- `com.amazon.kindle.inputMethod` — input method ops: preedit set, commit, replace, delete, get surrounding text
- `com.lab126.winmgr` — window manager: window list, orientation, e-ink mode, fake taps/keys, chrome
- `com.lab126.winmgr.ligl` — LIGL; logging props only
- `com.lab126.blanket` — blanket overlay layers: load/unload (screensaver, langpicker, usb), uiQuery
- `com.lab126.pillow` — pillow UI toolkit: dialogs, chrome, activity indicator, alerts
- `com.lab126.KIWIBridge` — UI query bridge
- `com.lab126.chromebar` — chrome bar: activity indicator, search results, chrome config

## Media (audio, bluetooth)

- `com.lab126.btService` — audible/bluetooth capability flags
- `com.lab126.btfd` — bluetooth daemon: pair/bond/disconnect, scan, A2DP/BLE, playback metadata
- `com.lab126.imageViewer` — image viewer; exposes no LIPC

## Metrics/Diagnostics

- `com.lab126.devicemetrics` — metrics push: all, clickstream, high-priority
- `com.lab126.fastMetrics` — fast event hooks: wifi popup, captive portal, wireless on
- `com.lab126.demd` — device metrics daemon: log app/OS metrics, emission status
- `com.lab126.kindleStatusService` — status logging, config metrics to file
- `com.lab126.JournalingService` — journaling enabled flag
- `com.lab126.linux.arm.metrics` — exposes no LIPC

## Identity & Registration

- `com.lab126.amazonRegistrationService` — registration: register/deregister, primary/secondary users, isRegistered
- `com.lab126.IdentityService` — identity access token: invalidate, refresh
- `com.lab126.DeviceAuthenticationService` — Amazon auth cookies: fetch, install
- `com.lab126.household` — household profiles: active profile/role, link secondary adult
- `com.lab126.KindleIdentity` — read-only device identity: deviceType, GUID

## Push (s2dm/adm messaging)

- `AssetOwnership.DeviceSharingUpdated` — device-sharing update push receiver
- `AssetOwnership.SMD.Poll` — SMD poll: transfer progress, todo handling, cache refresh
- `CampaignSync.Invalidate` — exposes no LIPC
- `CampaignSync.Update` — campaign update push receiver
- `DPCService.SettingChanged` — device-policy setting-changed push receiver
- `DeviceMessaging.LanguageLayer.MessageResponse` — language-layer message response push receiver
- `HouseholdMessage.Updates` — household message update push receiver
- `com.amazon.java.messagingservice` — Java push messaging endpoint

## Policy & Profiles

- `com.lab126.dpmManager` — device policy: parental-controls password, disabled features, passcode rules
- `com.lab126.dpm.apps` — per-app policy: disable annotations backup, public notes, popular highlights
- `com.lab126.freetime` — FreeTime kids: subscription status, offer reject
- `com.lab126.ccat` — active profile selection

## Other

- `com.amazon.ebook.util.net.certmanutilities` — exposes no LIPC
- `com.lab126.bev` — exposes no LIPC
- `com.lab126.demoservice` — exposes no LIPC
- `com.lab126.sph` — exposes no LIPC
- `com.lab126.yjff` — exposes no LIPC
- `com.lab126.odot` — message queueing
- `com.lab126.phd` — PHD daemon: new SPH schedule
- `com.lab126.cvm` — CVM service; logging props only
