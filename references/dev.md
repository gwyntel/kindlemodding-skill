# Kindle Development

Kindle runs Linux. Write native apps in C/C++ with Meson build system.

## Kindle SDK

Unofficial SDK by KMC. Supplants existing koxtoolchain installation with libraries and pkg-config support. Designed for Meson. Works by downloading target firmware from Amazon, copying libraries into toolchain's `sysroot`, setting up `.pc` files for pkgconfig on supported libraries.

### Install

Install koxtoolchain first, then:

1. Clone SDK:
```sh
git clone --recursive --depth=1 https://github.com/KindleModding/kindle-sdk.git
```
2. Install for target:
```sh
cd kindle-sdk
chmod +x ./gen-sdk.sh
./gen-sdk.sh <target>
```

`<target>` same as toolchain you want SDK for:

| TC | Supported Devices | Target |
|:---:|:---:|:---:|
| kindle | Kindle 2, DX, DXg, 3 | [not supported by this tutorial] |
| kindle5 | Kindle 4, Touch, PW1 | [not supported by this tutorial] |
| kindlepw2 | Kindle PW2 & everything since on FW <5.16.3 | kindlepw2 |
| kindlehf | Any Kindle on FW >= 5.16.3 | kindlehf |

### Usage

```sh
meson setup --cross-file <meson_crosscompile_path> builddir_<target>
```

Crosscompile file path is output when SDK installer runs. Typically under `~/x-tools/<toolchain>/meson-crosscompile.txt`.

## GTK Tutorial

Step-by-step guide: create native Kindle GUI app with `GTK+-2.0`, C++, Meson. Assumes basic C++ knowledge before following.

### Prerequisites

- Linux OS, or WSL/msys2 under Windows. MacOS untested, may work.
- Jailbroken Kindle; know its firmware version.
- Compile toolchain targeting device (see below).
- System packages for toolchain: git, ncurses, gperf, help2man, bison, texinfo, flex, gawk, unzip, wget.
- For SDK: curl, sed.
- For tutorial: meson, gtk2 (with development headers), compilation tools.

### Installing required packages

Arch Linux:
```sh
# For the toolchain
sudo pacman -S base-devel curl git gperf help2man unzip wget

# For the SDK
sudo pacman -S curl sed libarchive nettle

# For this tutorial
sudo pacman -S meson gtk2
```

Debian/Ubuntu:
```sh
# For the toolchain
sudo apt-get install build-essential autoconf automake bison flex gawk libtool libtool-bin libncurses-dev curl file git gperf help2man texinfo unzip wget

# For the sdk
sudo apt-get install curl sed libarchive-dev nettle-dev

# For this tutorial
sudo apt-get install meson gtk2.0 libgtk2.0-dev
```

### Building the toolchain

Pre-built option: use [pre-built release](https://github.com/koreader/koxtoolchain/releases/latest) to skip building.

1. Clone:
```sh
git clone --recursive --depth=1 https://github.com/koreader/koxtoolchain.git
```
2. Build for device:
```sh
cd koxtoolchain
chmod +x ./gen-tc.sh
./gen-tc.sh <target>
```

Target table (same as SDK table):

| TC | Supported Devices | Target |
|:---:|:---:|:---:|
| kindle | Kindle 2, DX, DXg, 3 | [not supported by this tutorial] |
| kindle5 | Kindle 4, Touch, PW1 | [not supported by this tutorial] |
| kindlepw2 | Kindle PW2 & everything since on FW <5.16.3 | kindlepw2 |
| kindlehf | Any Kindle on FW >= 5.16.3 | kindlehf |

Support multiple Kindles: run `./gen-tc.sh <other_target>` again; new toolchain added to `~/x-tools` directory. Compilation usually takes ~30 minutes per target on most PCs.

### Setting up the SDK

1. Clone:
```sh
git clone --recursive --depth=1 https://github.com/KindleModding/kindle-sdk.git
```
2. Install for target:
```sh
cd kindle-sdk
chmod +x ./gen-sdk.sh
./gen-sdk.sh <target>
```

`<target>` same as toolchain you want SDK for. Note path SDK installer returns to `meson-crosscompile.txt` — needed later.

### Setting up the project

Create new git repository in safe location for app code.

### meson.options

Create `meson.options`:
```python
option('kindle_root_dir', type : 'string', value: '', description: 'The path to the Kindle\'s mounted rootfs (for linking libraries)')
```

Tells Meson what parameters project uses for configuration/compilation. Here only need `kindle_root_dir` so can set it to Kindle's root directory in later step.

### meson.build

```python
project('example_gtk_application', 'cpp', version: 'v1.0.0', default_options: ['cpp_std=c++17'], meson_version: '>=1.1')

# Define dependencies we want
gtk_dep = dependency('gtk+-2.0')

###
# Project definition
###
sources = files(
    './src/main.cpp'
)

include_dirs = include_directories(
  './src/include/'
)

executable('example_gtk_application', sources, include_directories: include_dirs, dependencies: [gtk_dep], cpp_args: '-static-libstdc++', link_args: '-static-libstdc++')
```

Statically link C++ standard library. Koxtoolchain ships GCC newer than Kindle technically supports; fine so long as standard library statically linked.

File structure:
```
.
├── meson.build
└── meson.options

1 directory, 2 files
```

### Source files

Create `main.cpp` and `include/` folder under `src/`:
```
.
├── meson.build
├── meson.options
└── src
    ├── include
    └── main.cpp

3 directories, 3 files
```

`src/main.cpp`:
```cpp
#include <gtk-2.0/gtk/gtk.h>

int main(int argc, char* argv[]) {
  GtkWidget *window;
    
  gtk_init (&argc, &argv);
  
  window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
  gtk_window_set_title(GTK_WINDOW(window), "L:A_N:application_ID:org.kindlemodding.example-gtk-application_PC:T");

  g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

  gtk_widget_show(window);
  
  gtk_main();

  return 0;
}
```

### Testing compilation

Configure for computer:
```sh
meson setup builddir
```
Compile:
```sh
meson compile -C builddir
```

Run on computer: see empty GTK window.

### Testing cross-compilation

```sh
meson setup --cross-file <meson_crosscompile_path> builddir_<target>
```

Target same as before; substitute `<meson_crosscompile_path>` with path SDK installer gave earlier. Compile:
```sh
meson compile -C builddir_<target>
```

All steps work: first app compiled for Kindle.

### Kindle considerations

Things to consider writing GUI apps on Kindle. Only guidance given:

**Window title.** See Awesome Window Manager section below.

## Awesome Window Manager

Kindle uses Awesome Window Manager with some tweaks. Every window must have title following specific format. Example: Kindle store window title:
```
L:A_N:application_PC:TS_ID:com.lab126.store
```

Window titles are key-value store, separated by `_` character. Above translates roughly to:
```json
{
    "L":"A",
    "N":"application",
    "PC":"TS",
    "ID":"com.lab126.store"
}
```

### [L]ayer

Window layer. 5 values:

| Value | Description |
|-------|-------------|
| `A` | The `APP` layer |
| `C` | The `CHROME` layer |
| `D` | The `DIALOG` layer |
| `KB` | The `KB` (keyboard) layer |
| `SS` | The `SCREENSAVER` layer |

Layers displayed top to bottom; apps on `SCREENSAVER` layer above apps on `APP` layer. Generally only use `A` and `D`.

### [N]ame

lab126 internally calls this "name/role". In reality only represents role. Listed values:

| Value | Description |
|-------|-------------|
| `application` | For use with the `A` layer, application windows |
| `dialog` | For use with the `D` layer, dialog windows |
| `titlebar` | For backwards compatability |
| `tiledBottom` | [SHOULD NOT BE USED IN PRODUCTION - lab_126.application_layer.lua:255] |
| `searchResult` | For use with the `C` layer, seemingly used for search result displays, acts as a modified dialog |
| `pillowAlert` | An alert created by Pillow, for use with the `D` layer, blocks the home button |
| `titleBar` | |
| `footerBar` | |
| `topBar` | Seemingly used for custom search bar apps (use with `BARTYPE` parameter) |
| `mediaBar` | |
| `bottomBar` | REDUNDANT - use `topBar` role with `BARTYPE` of `B` |
| `appToolBar` | REDUNDANT - use `topBar` role with `BARTYPE` of `A` |
| `keyboard` | Used by the Kindle's keyboard |
| `keyboardExt` | |
| `activeSS` | |
| `screenSaver` | |
| `searchBar` | Used by the Kindle's top bar |

Generally only use `application` and `dialog`, with `A` and `D` layers.

### [PC] (Persistent Chrome)

Window manager uses to determine how to handle displaying chrome elements such as top bar and "search bar". Value any combination of:

| Value | Description |
|-------|-------------|
| `T` | Show the Kindle top bar/status bar on modern firmware |
| `S` | Shows the "search bar" |
| `B` | Shows the legacy bottom bar |
| `N` | Show no bars (same as if `PC` was ommited entirely) |

Combining multiple PC values: `TS`, `TSB`. Note: window resizing appears broken in `TSB`; shown for illustration only, shouldn't use.

### [ID] (Identifier)

Simple string giving app identifier. Value anything not containing underscore (used as delimiter). Usually reverse-domain-name format like `com.lab126.reader`. Note: value `blankBackground` reserved; purpose unknown; makes app `invalid`.

### [BARTYPE]

Used with `topBar` role type. Describes bar positioning:

| Value | Description |
|-------|-------------|
| `T` | Top bar type |
| `S` | Search bar type |
| `B` | Bottom bar type - "added for kpp chrome footer" - It behaves like top bars in terms of persistence |
| `A` | Application bar type - Secondary bar for application specific tools |

### [O]rientation - Supported App Orientations

Sets application's orientation mask. Any combination of 4 values (e.g. `ULR` or `UDLR`):

| Value | Description |
|-------|-------------|
| `U` | Up |
| `D` | Down |
| `L` | Left |
| `R` | Right |

### [HIDE]

Flag to hide window; update title without it to show window. Example:
```
L:A_N:application_HIDE_ID:org.kindlemodding.hiddenwindow
```

Optional value `background`: window does not take focus (actual purpose unknown).

### [RC] - Rounded Corners

For dialogs. Sets rounded corners. Use as flag or give integer value = corner radius in pixels of all corners. Can also give value `custom`; then any combination of 4 keys sets corner radius per window: `RCTL`, `RCTR`, `RCBL`, `RCBR`. Example (rounded corners only top-left and top-right, default radius):
```
RC:custom_RCTL_RCTR
```

### [M]odality

For dialogs specifically. Flag present means dialog modal. Optional value `dismissible`, e.g.:
```
L:A_N:application_M:dismissable_ID:org.kindlemodding.hiddenwindow
```

### [RKB] - Require KeyBoard

For dialogs requiring keyboard. Positions dialog so it does not clip with spawned keyboard. Can seemingly take numeric value of unknown purpose.

### [PALMR] - Palm Rejection

Purpose unknown. Only used in conjunction with `M:dismissable`; seemingly related to palm rejection on dismissal.

## KPM (Kindle Package Manager)

Package manager by [Hackerdude](https://hackerdude.tech). As of `hdnext`: recommended distribution method for Kindle homebrew. Indexes Kindle homebrew; download and install on-device.

Each developer expected to submit to official [KindleModding KPM repository](https://github.com/KindleModding/repo/pulls) or host own repository. Repositories can be hosted statically on GitHub Pages.

### Creating a package

Example package: https://github.com/KindleModding/example_kpm_package — read its files for KPM package structure understanding.

Create with [`kpm-helper.py`](https://github.com/KindleModding/KPM/blob/main/kpm-helper.py):
```sh
# Step 1. Create a folder to store your package contents
mkdir example_package
# Step 2. Initialise the package folder
python kpm-helper.py package init ./example_package
```

Result:
```
example_package
└── manifest.json

1 directory, 1 file
```

Manifest initialised to target all platforms.

### Packing

Convert package folder to `kpkg` file (addable to repository, installable by KPM):
```sh
python kpm-helper.py package pack FOLDER_PATH OUTPUT_PATH
```

`FOLDER_PATH`: path to package. `OUTPUT_PATH`: folder to put `kpkg` file.

### Targeting specific platforms

Modify manifest at pack time with `--supported-platform` flag, or manually set optional `supported_platforms` array in `manifest.json`.

Valid platforms:
- `kindle` - Kindles older than the K5
- `kindle5` - K5 and newer
- `kindlepw2` - PW2 and newer
- `kindlehf` - armhf platforms

### Hooks

Put any other files in package folder; they do nothing by themselves. Hooks:

```
example_package
├── install.sh
├── launch.sh
├── manifest.json
└── uninstall.sh

1 directory, 5 files
```

| File Name | Purpose |
|-----------|---------|
| install.sh | Ran during package installation after it is unpacked |
| uninstall.sh | Ran during package uninstallation after it is unmounted |
| launch.sh | Ran when package is launched from a launcher |

Hooks MUST NOT write to rootfs or remount it as rw. Hooks always run from package's folder while package in unpacked state: reference local files with relative paths.

Encouraged: use `install.sh` hook to place scriptlet in `/mnt/us/documents` folder when appropriate. Recommended scriptlet runs `/var/local/kmc/bin/kpm launch PACKAGENAME` to run package's `launch.sh`.

### Upgrade guidelines

- During upgrades: `uninstall.sh` ran with `upgrade` parameter, i.e. `uninstall.sh upgrade`
- Package files deleted
- New package files extracted
- `install.sh` ran on new version
- `uninstall.sh` hook should NOT delete package files; KPM handles that

### Writing to rootfs

Unsupported: using `install.sh` hook to modify contents of `rootfs`. Recommended not to do for now. Solution planned in near future.

### Creating a repository

Usually unnecessary: sufficient to submit packages to [official repository](https://github.com/KindleModding/repo). Otherwise create with [`kpm-helper.py`](https://github.com/KindleModding/KPM/blob/main/kpm-helper.py):
```sh
# Step 1. Create a folder to store your package contents
mkdir example_repository
# Step 2. Initialise the package folder
python kpm-helper.py repo init ./example_repository
```

Recommended instead: fork [example repository](https://github.com/KindleModding/kpm-repository-template).

Add package to repository:
```sh
python kpm-helper.py repo add ./example_repository PACKAGE_PATH
```

`PACKAGE_PATH`: path to `.kpkg` file generated by `kpm-helper.py`.

## Scriptlets

Introduced with Universal Hotfix released with Winterbreak. Method of running programs. Handled by [SH_Integration](https://github.com/KindleModding/sh_integration).

Any `.sh` file in Kindle's `documents` folder (`/mnt/us/documents`) indexed as though book; added to library. Click to run.

### Metadata

Customise appearance with specific lines at start of file:
```sh
#!/bin/sh
# Name: Test Script
# Author: Hackerdude

echo "Hello, World!"
```

Appears in library named `Test Script`, author `Hackerdude`.

### Icons

Set via `# Icon:` flag. Value either absolute path to image file, or base64 encoded image:
```sh
#!/bin/sh
# Name: KoReader
# Author: Hackerdude
# Icon: data:image/png;base64,[long base64 PNG omitted in condensation]

echo "Hello, World!"
```

Warning: some converters use wrong filetype when generating base64 string; ensure filetype matches actual data.

### Hooks

`# UseHooks` flag gives functions called when certain events happen to scriptlet, instead of whole script called once when ran:
```sh
#!/bin/sh
# Name: Test For Evnets
# Author: Hackerdude
# UseHooks

on_install() {
    echo "on_install called!" >> /mnt/us/test.log
}

on_remove() {
    echo "on_remove called!" >> /mnt/us/test.log
}

on_run() {
    echo "on_run called!" >> /mnt/us/test.log
}
```

Hooks: `on_install()`, `on_remove()`, `on_run()`.

### DontUseFbink

By default script's stdout and stderr both piped to FBink to display on Kindle. Add `# DontUseFBInk` flag to disable:
```sh
#!/bin/sh
# Name: Silent Script
# Author: Hackerdude
# DontUseFBInk

echo "A user won't see this"
```

### Examples

More scriptlet examples, or share own: `scriptlets` channel in [Kindle Modding Community Discord server](https://dsc.gg/kindle-modding).
