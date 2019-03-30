# nx-sd

nx-sd is a lightweight, ready-to-use custom firmware package for the Nintendo Switch. It includes everything necessary for launching homebrew and custom NSPs.


## Quick Start Guide

1. Download and extract the [latest release](https://github.com/designgears/nx-sd/releases/latest) of nx-sd.
2. Copy the contents of the `sdcard` folder to the root of your microSD card.
3. Power on your Nintendo Switch in RCM and inject the payload in `payload` folder.
4. Atmosphère will boot automatically.

## Building

1. Install [devkitARM and devkitA64](https://devkitpro.org/wiki/Getting_Started) toolchains.
2. Install dependencies

       pacman -S devkitARM devkitarm-rules switch-curl switch-freetype switch-libconfig switch-libjpeg-turbo switch-sdl2 switch-sdl2_gfx switch-sdl2_image switch-sdl2_ttf switch-zlib
   
3. Install [pycryptodome](https://pycryptodome.readthedocs.io/en/latest/)

       pip install pycryptodome

4. Clone this repo and all submodules recursively.

       git clone https://github.com/designgears/nx-sd.git --recurse-submodules

5. Run `python build.py`.


## Components

### Core components

| Component                                                 | Version        | Description |
| --------------------------------------------------------- | -------------- | ----------- |
| [Atmosphère](https://github.com/Atmosphere-NX/Atmosphere) | 0.8.6-994d7d5  | Custom firmware for the Nintendo Switch |
| [hekate](https://github.com/CTCaer/hekate)                | v4.9.1_        | Custom Nintendo Switch bootloader |
| [nx-hbloader](https://github.com/switchbrew/nx-hbloader)  | v2.1.0-3af8c89 | Host process for loading homebrew NROs |
| [nx-hbmenu](https://github.com/switchbrew/nx-hbmenu)      | v3.0.1-6ec7388 | The Nintendo Switch homebrew menu |
| [sigpatches](https://bit.ly/2EYbEHg)                      | 2.0.0-7.0.1    | Sweet patches! |

### Addons

| Component                                                 | Version | Description |
| --------------------------------------------------------- | ------------ | ----------- |
| [Checkpoint](https://github.com/FlagBrew/Checkpoint)      | v3.6.0       | Save manager |
| [EdiZon](https://github.com/WerWolv/EdiZon)               | v3.0.1       | Save manager, editing tool, and memory trainer |
| [EdiZon Scripts](https://bit.ly/2V0kXMt)   | master       | Cheats, configs, and scripts for EdiZon |
| [ldn_mitm](https://github.com/spacemeowx2/ldn_mitm)       | v1.1.2       | A mitm kip modified from fs_mitm |
| [sys-CLK](https://github.com/retronx-team/sys-clk)        | 0.11.1       | Overclocking/underclocking system module |
| [Lockpick_RCM](https://github.com/shchmue/Lockpick_RCM)   | v1.0-30b5faf | Encryption key derivation bare metal RCM payload |


