#!/usr/bin/env python3

import argparse
import logging
import nxsd

from nxsd.package import NXSDPackage
from nxsd.components import atmosphere
from nxsd.components import awooinstaller
from nxsd.components import checkpoint
from nxsd.components import edizon
from nxsd.components import emuiibo
from nxsd.components import goldleaf
from nxsd.components import hbappstore
from nxsd.components import hekate
from nxsd.components import incognitorcm
from nxsd.components import jksv
from nxsd.components import ldnmitm
from nxsd.components import lockpickrcm
from nxsd.components import noexes
from nxsd.components import nxdumptool
from nxsd.components import nxhbloader
from nxsd.components import nxhbmenu
from nxsd.components import nxovlloader
from nxsd.components import nxshell
from nxsd.components import statusmonitoroverlay
from nxsd.components import switchzstd
from nxsd.components import sysclk
from nxsd.components import sysclkoverlay
from nxsd.components import sysclkeditor
from nxsd.components import syscon
from nxsd.components import sysftpdlight
from nxsd.components import teslamenu
from nxsd.components import toolbox

CORE_COMPONENTS = {
    'atmosphere':   atmosphere,
    'hekate':       hekate,
    'nxhbloader':   nxhbloader,
    'nxhbmenu':     nxhbmenu,
    'toolbox':      toolbox,
}

ADDON_COMPONENTS = {
    'jksv':                 jksv,
    'ldnmitm':              ldnmitm,
    'nxdumptool':           nxdumptool,
    'nxovlloader':          nxovlloader,
    'statusmonitoroverlay': statusmonitoroverlay,
    'sysclk':               sysclk,
    'sysclkoverlay':        sysclkoverlay,
    'sysftpdlight':         sysftpdlight,
    'teslamenu':            teslamenu,
}

OPTIONAL_COMPONENTS = {
    'awooinstaller':awooinstaller,
    'checkpoint':   checkpoint,
    'edizon':       edizon,
    'emuiibo':      emuiibo,
    'goldleaf':     goldleaf,
    'hbappstore':   hbappstore,
    'incognitorcm': incognitorcm,
    'lockpickrcm':  lockpickrcm,
    'noexes':       noexes,
    'nxshell':      nxshell,
    'switchzstd':   switchzstd,
    'sysclkeditor': sysclkeditor,
    'syscon':       syscon,
}

ALL_COMPONENTS = {
    **CORE_COMPONENTS,
    **ADDON_COMPONENTS,
    **OPTIONAL_COMPONENTS,
}

def main():
    commands = {
        'build': build,
        'clean': clean,
        'purge': purge,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='enable verbose logging output to log/build.log')
    parser.add_argument('-c', '--component', help='build/clean a specific component',
                        choices=sorted(ALL_COMPONENTS.keys()))
    parser.add_argument('command', nargs='?', default='build',
                        choices=commands.keys(),
                        help='build command to execute. options: build, clean (default: build)')

    args = parser.parse_args()

    if args.verbose:
        nxsd.logger.setLevel(logging.DEBUG)
        nxsd.logger.debug('Verbose logging enabled.')
    
    commands[args.command](args)

def build(args):
    if args.component is not None:
        packages = get_package(args.component)
    else:
        packages = get_packages()
    for package in packages:
        if package.build_components():
            nxsd.logger.info('Created {name} package!'.format(name=package.name))
        else:
            nxsd.logger.info('Failed to create {name} package! Check build.log for details.'.format(name=package.name))

def purge(args):
    purge_commands = [
        'git clean -fdx',
        'git submodule foreach --recursive git clean -fdx',
        'git submodule update --init --recursive',
        'docker system prune -a -f',
    ]
    nxsd.util.execute_shell_commands(purge_commands)

def clean(args):
    with open('log/build.log', "w"):
        nxsd.logger.info('Cleared log!')
    if args.component is not None:
        packages = get_package(args.component)
    else:
        packages = get_packages()
    for package in packages:
        package.clean()
        nxsd.logger.info('Cleaned {name} package!'.format(name=package.name))

def get_package(component):
    nxsd_component = NXSDPackage(
        name=component,
        build_type='component',
        build_directory='out/{}/'.format(component),
        output_filename='out/{}.zip'.format(component),
    )
    nxsd_component.components = [ALL_COMPONENTS[component]]

    return [nxsd_component]

def get_packages():
    nxsd_core = NXSDPackage(
        name='nxsd-core',
        build_type='package',
        build_directory='out/core/',
        output_filename='out/nxsd-core.zip',
    )
    nxsd_core.components = list(CORE_COMPONENTS.values())

    nxsd_addon = NXSDPackage(
        name='nxsd-addon',
        build_type='package',
        build_directory='out/addon/',
        output_filename='out/nxsd-addon.zip',
    )
    nxsd_addon.components = list(ADDON_COMPONENTS.values())

    return [nxsd_core, nxsd_addon]


if __name__ == '__main__':
    main()
