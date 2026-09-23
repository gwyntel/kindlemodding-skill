---
name: kindlemodding
description: Condensed Kindle-modding knowledge base — every jailbreak method by model/firmware, post-jailbreak setup, firmware flashing/downgrading, Mesquite/WAF APIs, ~100 LIPC services, homebrew dev docs. Source: KindleModding wiki (kindlemodding.github.io).
---

Kindle modding, compressed caveman-style. Every word earned. Facts from KindleModding community wiki: https://github.com/KindleModding/kindlemodding.github.io / https://kindlemodding.github.io. Unofficial condensation; not affiliated. License: CC BY-NC 4.0 (see LICENSE).

## When use

- Jailbreaking a Kindle: pick method by model + firmware → read references/jailbreaks.md first.
- Post-jailbreak: KUAL/MRPI, blocking OTA updates, backups → references/jailbreaks.md + references/faq.md.
- Flashing/downgrading firmware → references/firmware.md.
- Internals: debug searchbar commands, hotfix, appreg, boot process → references/hacking.md.
- Building WAF apps (Mesquite JS, `window.kindle` API) → references/wafs.md.
- System services (LIPC `com.lab126.*`) → references/lipc.md.
- Homebrew development: SDK, KPM packages, GTK, scriptlets, window manager → references/dev.md.
- Quick questions after jailbreak (KOReader, recovery, OOBE) → references/faq.md.

## Reference files

- references/jailbreaks.md — every jailbreak: WinterBreak, WinterBreak2, SpringBreak, Sanctuary, SpiderCat, Nosebleed, Vera, AdBreak, LanguageBreak, KindleBreak, Popcorn, WatchThis, legacy K2/DX/DXG/K3/K4/K5. Models, firmware ranges, how it works, exact steps/commands/URLs. Post-jailbreak: hotfix, KUAL/MRPI, OTA blocking, backups/restoring. Wizard + models-table logic.
- references/firmware.md — downgrading (rules + AllowDowngrade.sh), downloading updates, last-jailbreakable firmware table, KV cross-flash, OTA files.
- references/hacking.md — jailbreak mechanism, debug `;` commands (kpp_sys_cmds/kpp_app_cmds), hotfix internals, appreg.db tables, cc.db, usermode boot process, prototype Kindles, models table.
- references/wafs.md — Mesquite/WAF structure, config.xml, `window.kindle` sub-objects (chrome, dconfig, dev, device, gestures, messaging, net, todo) with exact methods, enums.
- references/lipc.md — ~100 LIPC services grouped by purpose, one line each, exact names. lipc-probe dump format, lipc-set-prop usage.
- references/dev.md — Kindle SDK install/targets, KPM package + repo creation, GTK tutorial, kindle considerations, scriptlets, Awesome Window Manager key reference.
- references/faq.md — jailbreak FAQ, OOBE bypass, OTA blocking scripts (ota.sh/nosb), recovering-from-reset, what's next (KOReader, homebrew), Vera privesc.sh.
