[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/gwyntel/kindlemodding-skill)

# kindlemodding skill

Condensed, unofficial Kindle-modding knowledge base derived from the [KindleModding community wiki](https://kindlemodding.github.io/). Covers jailbreak selection by model and firmware, post-jailbreak setup, firmware flashing, Mesquite/WAF APIs, LIPC services, homebrew development, and FAQs. Community contributors own the underlying facts; this project is not affiliated with Amazon.

## Install with Vercel Skills CLI

Install the skill for Hermes Agent globally:

```sh
npx skills add gwyntel/kindlemodding-skill --skill kindlemodding --agent hermes-agent -g -y
```

To inspect available skills before installing:

```sh
npx skills add gwyntel/kindlemodding-skill --list
```

The canonical source is [gwyntel/kindlemodding-skill](https://github.com/gwyntel/kindlemodding-skill). This is a single-skill repository; its entry point is the root `SKILL.md`, with supporting material in `references/` and `serial_checker.py`.

## Use

Ask your compatible agent about Kindle modding; the skill's `SKILL.md` routes the question to the relevant reference. For offline serial/model and optional firmware screening, run the Python 3, standard-library-only checker:

```sh
python3 serial_checker.py SERIAL [FIRMWARE]
```

Use the output as a guide and consult the linked community source before acting. Firmware and jailbreak guidance can be device-specific and consequential.

## Update

Update the installed skill with:

```sh
npx skills update kindlemodding -g -y
```

If your CLI version does not accept a named skill with `-g`, run `npx skills update -g -y` to update all globally installed skills. To get the current repository version without the CLI, rerun the install command above.

## Troubleshooting

- **Skill not discovered:** Verify the repository root contains `SKILL.md`, and install with the exact name `kindlemodding` using `--skill kindlemodding`.
- **Invalid frontmatter:** Keep `name` and `description` as valid YAML scalar fields at the top of `SKILL.md`; the name must match `kindlemodding`.
- **Wrong agent or install scope:** Specify `--agent hermes-agent` and `-g` for a global Hermes install. Omit `-g` to install in the current project instead.
- **Permission or network errors:** Check GitHub access and the target agent skills directory's write permissions; retry in a writable environment.
- **Checker won't run:** Use Python 3 and pass a serial argument; the checker does not require network access or third-party packages.

## Source and license

- Upstream knowledge: [KindleModding wiki](https://github.com/KindleModding/kindlemodding.github.io) and [website](https://kindlemodding.github.io/).
- The existing [LICENSE](LICENSE) is CC BY-NC 4.0; it is preserved. See it for the applicable terms.
