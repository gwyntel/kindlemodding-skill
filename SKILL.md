---
name: kindlemodding
author: gwyntel
description: "Condensed Kindle-modding knowledge base: every jailbreak method by model/firmware, post-jailbreak setup, firmware flashing/downgrading, Mesquite/WAF APIs, ~100 LIPC services, homebrew dev docs. Source: KindleModding wiki (kindlemodding.github.io)."
---

Kindle modding, compressed caveman-style. Every word earned. Facts from KindleModding community wiki: https://github.com/KindleModding/kindlemodding.github.io / https://kindlemodding.github.io. Unofficial condensation; not affiliated. License: CC BY-NC 4.0 (see LICENSE).

## Agent and path portability
This is a reference skill, not a device-control integration. It requires only access to this installed skill's files; optional serial screening requires Python 3. All reference and script paths below are relative to the directory containing this `SKILL.md`, not the agent's working directory. Invoke the checker from that directory or provide its resolved path. Do not assume Hermes-only tools, paths, or device access. Modifying a Kindle is consequential: provide accurate cited steps, clearly distinguish model/firmware compatibility, and require explicit user intent before suggesting risky actions.

## When use

- Jailbreaking a Kindle: pick method by model + firmware → read references/jailbreaks.md first.
- Screening a serial number: identify model offline → run `serial_checker.py SERIAL [FIRMWARE]` (mirrors site wizard, no network).
- Post-jailbreak: KUAL/MRPI, blocking OTA updates, backups → references/jailbreaks.md + references/faq.md.
- Flashing/downgrading firmware → references/firmware.md.
- Internals: debug searchbar commands, hotfix, appreg, boot process → references/hacking.md.
- Building WAF apps (Mesquite JS, `window.kindle` API) → references/wafs.md.
- System services (LIPC `com.lab126.*`) → references/lipc.md.
- Homebrew development: SDK, KPM packages, GTK, scriptlets, window manager → references/dev.md.
- Quick questions after jailbreak (KOReader, recovery, OOBE) → references/faq.md.

## Tools

- serial_checker.py — offline Python mirror of jailbreak wizard: serial → model/variant, optional firmware → jailbreak matches. Stdlib only, no network. `screen()` importable. Data snapshot 2026-09-25.

## Reference files

- references/jailbreaks.md — every jailbreak: WinterBreak, WinterBreak2, SpringBreak, Sanctuary, SpiderCat, Nosebleed, Vera, AdBreak, LanguageBreak, KindleBreak, Popcorn, WatchThis, legacy K2/DX/DXG/K3/K4/K5. Models, firmware ranges, how it works, exact steps/commands/URLs. Post-jailbreak: hotfix, KUAL/MRPI, OTA blocking, backups/restoring. Wizard + models-table logic.
- references/firmware.md — downgrading (rules + AllowDowngrade.sh), downloading updates, last-jailbreakable firmware table, KV cross-flash, OTA files.
- references/hacking.md — jailbreak mechanism, debug `;` commands (kpp_sys_cmds/kpp_app_cmds), hotfix internals, appreg.db tables, cc.db, usermode boot process, prototype Kindles, models table.
- references/wafs.md — Mesquite/WAF structure, config.xml, `window.kindle` sub-objects (chrome, dconfig, dev, device, gestures, messaging, net, todo) with exact methods, enums.
- references/lipc.md — ~100 LIPC services grouped by purpose, one line each, exact names. lipc-probe dump format, lipc-set-prop usage.
- references/dev.md — Kindle SDK install/targets, KPM package + repo creation, GTK tutorial, kindle considerations, scriptlets, Awesome Window Manager key reference.
- references/faq.md — jailbreak FAQ, OOBE bypass, OTA blocking scripts (ota.sh/nosb), recovering-from-reset, what's next (KOReader, homebrew), Vera privesc.sh.
