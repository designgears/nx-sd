#!/usr/bin/env python3

import argparse
import logging
import nxsd

from nxsd.package import NXSDPackage
from nxsd.components import hekate
from nxsd.components import atmosphere
from nxsd.components import nxhbloader
from nxsd.components import nxhbmenu
from nxsd.components import edizon
from nxsd.components import lockpickrcm
from nxsd.components import ldnmitm
from nxsd.components import incognito
from nxsd.components import sysclk
from nxsd.components import sysftpd
from nxsd.components import goldleaf
from nxsd.components import nxshell
from nxsd.components import incognito
from nxsd.components import amiiswap
from nxsd.components import emuiibo
from nxsd.components import gearbox
from nxsd.components import sigpatches

CORE_COMPONENTS = {
    'hekate': hekate,
    'atmosphere': atmosphere,
    'nxhbloader': nxhbloader,
    'nxhbmenu': nxhbmenu,
    'lockpickrcm': lockpickrcm,
    'gearbox': gearbox,
    'sigpatches': sigpatches,
}

ADDON_COMPONENTS = {
    'emuiibo': emuiibo,
    'ldnmitm': ldnmitm,
    'sysclk': sysclk,
    'sysftpd': sysftpd,
    'amiiswap': amiiswap,
    'edizon': edizon,
    'goldleaf': goldleaf,
    'nxshell': nxshell,
    'incognito': incognito,
}

OPTIONAL_COMPONENTS = {
    'incognito': incognito
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
    if args.component != None:
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
        'docker system prune -f',
    ]
    nxsd.util.execute_shell_commands(purge_commands)

def clean(args):
    with open('log/build.log', "w"):
        nxsd.logger.info('Cleared log!')
        pass
    if args.component != None:
        packages = get_package(args.component)
    else:
        packages = get_packages()
    for package in packages:
        package.clean()
        nxsd.logger.info('Cleaned {name} package!'.format(name=package.name))
    pass

def get_package(component):
    nxsd_component = NXSDPackage(
        name=component,
        build_directory='build/{}/'.format(component),
        output_filename='build/{}.zip'.format(component),
    )
    nxsd_component.components = [ALL_COMPONENTS[component]]

    return [nxsd_component]

def get_packages():
    nxsd_core = NXSDPackage(
        name='nxsd-core',
        build_directory='build/core/',
        output_filename='build/nxsd-core.zip',
    )
    nxsd_core.components = list(CORE_COMPONENTS.values())

    nxsd_addon = NXSDPackage(
        name='nxsd-addon',
        build_directory='build/addon/',
        output_filename='build/nxsd-addon.zip',
    )
    nxsd_addon.components = list(ADDON_COMPONENTS.values())

    return [nxsd_core, nxsd_addon]


if __name__ == '__main__':
    main()
