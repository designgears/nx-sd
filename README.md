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

       sudo pacman -S switch-curl switch-freetype switch-libconfig switch-libjpeg-turbo switch-sdl2 switch-sdl2_image switch-sdl2_gfx switch-sdl2_ttf switch-zlib
   
3. Install [Python 3.7](https://www.python.org/downloads/) or newer.
4. Clone this repo and all submodules recursively.

       git clone https://github.com/designgears/nx-sd.git --recurse-submodules

5. Run `build.py`.


## Components

### Core components

| Component                                                 | Version | Description |
| --------------------------------------------------------- | ------- | ----------- |
| [Atmosphère](https://github.com/Atmosphere-NX/Atmosphere) | master  | Custom firmware for the Nintendo Switch |
| [hekate](https://github.com/CTCaer/hekate)                | master  | Custom Nintendo Switch bootloader |
| [nx-hbloader](https://github.com/switchbrew/nx-hbloader)  | 2.1.0   | Host process for loading homebrew NROs |
| [nx-hbmenu](https://github.com/switchbrew/nx-hbmenu)      | master  | The Nintendo Switch homebrew menu |
| [sigpatches](https://goo.gl/rsYAaB)                       | 7.0.1   | Sweet patches! |

### Addons

| Component                                                 | Version | Description |
| --------------------------------------------------------- | ------- | ----------- |
| [Checkpoint](https://github.com/FlagBrew/Checkpoint)      | 3.6.0   | Save manager for the Nintendo Switch |
| [EdiZon](https://github.com/WerWolv/EdiZon)               | 3.0.1   | Save manager, editing tool, and memory trainer for the Nintendo Switch |
