## Building

1. Install [Docker](https://hub.docker.com/search/?type=edition&offering=community) and [Python 3.7](https://www.python.org/downloads/).

2. Clone this repo and all submodules recursively.

       git clone https://github.com/designgears/nx-sd.git --recurse-submodules

3. Run `python3 build.py`.

### Building optional components

The name of each componenet corresponds with its filename in `/nxsd/components`. A successful build will output to the `/build` directory under the same name.

       python3 build.py -c tinfoil

## Components

### Core components

| Component                                                 | Description |
| --------------------------------------------------------- | ----------- |
| [Atmosphère](https://github.com/Atmosphere-NX/Atmosphere) | Custom firmware for the Nintendo Switch |
| [hekate](https://github.com/designgears/hekate)           | Nintendo Switch Bootloader |
| [incognito](https://github.com/blawar/incognito)          | Wipes personal information from your Nintendo Switch |
| [Lockpick_RCM](https://github.com/shchmue/Lockpick_RCM)   | Encryption key derivation bare metal RCM payload |
| [nx-hbloader](https://github.com/switchbrew/nx-hbloader)  | Host process for loading homebrew NROs |
| [nx-hbmenu](https://github.com/switchbrew/nx-hbmenu)      | The Nintendo Switch homebrew menu |
| [RèiNX](https://github.com/designgears/ReiNX/)            | A modular Switch custom firmware |
| [Toolbox](https://github.com/designgears/Kosmos-Toolbox)  | A toolbox for the Kosmos CFW package |

### Addons

| Component                                                 | Description |
| --------------------------------------------------------- | ----------- |
| [AmiiSwap](https://github.com/FuryBaguette/AmiiSwap)      | Nintendo Switch GUI Amiibo Manager homebrew for emulation with Emuiibo |
| [EdiZon](https://github.com/WerWolv/EdiZon)               | Save manager, editing tool, and memory trainer |
| [emuiibo](https://github.com/XorTroll/emuiibo)            | MitM'ing NFP services for Amiibo emulation! |
| [Goldleaf](https://github.com/XorTroll/Goldleaf)          | Nintendo Switch multipurpose homebrew tool |
| [ldn_mitm](https://github.com/spacemeowx2/ldn_mitm)       | Play local wireless supported games online |
| [NX-Shell](https://github.com/joel16/NX-Shell)            | 3DShell port for the Nintendo Switch |
| [sys-CLK](https://github.com/retronx-team/sys-clk)        | Overclocking/underclocking system module |
| [sys-ftpd](https://github.com/designgears/sys-ftpd)       | Ftpd as a Nintendo Switch sysmodule |

### Optional

| Component                                                 | Description |
| --------------------------------------------------------- | ----------- |
| [tinfoil](https://github.com/Adubbz/Tinfoil)              | `OG tnfoil`, also known as `tinfoil 88` |
