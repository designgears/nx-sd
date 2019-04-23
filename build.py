#!/usr/bin/env python3

import argparse
import logging
import nxsd

from nxsd.package import NXSDPackage
from nxsd.components import hekate
from nxsd.components import atmosphere
from nxsd.components import nxhbloader
from nxsd.components import nxhbmenu
from nxsd.components import sigpatches
from nxsd.components import edizon
from nxsd.components import lockpickrcm
from nxsd.components import ldnmitm
from nxsd.components import sysclk
from nxsd.components import sysftpd
from nxsd.components import goldleaf
from nxsd.components import nxshell
from nxsd.components import incognito
from nxsd.components import amiiswap
from nxsd.components import emuiibo


def main():
    commands = {
        'build': build,
        'clean': clean,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='enable verbose logging output to log/build.log')
    parser.add_argument('-c', '--component', help='build/clean a specific component')
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
        name='nxsd-{}'.format(component),
        build_directory='build/{}/'.format(component),
        output_filename='nxsd-{}.zip'.format(component),
    )
    nxsd_component.components = [eval(component)]

    return [nxsd_component]

def get_packages():
    nxsd_core = NXSDPackage(
        name='nxsd-core',
        build_directory='build/core/',
        output_filename='nxsd-core.zip',
    )
    nxsd_core.components = [
        hekate,
        atmosphere,
        nxhbloader,
        nxhbmenu,
        sigpatches,
    ]

    nxsd_addon = NXSDPackage(
        name='nxsd-addon',
        build_directory='build/addon/',
        output_filename='nxsd-addon.zip',
    )
    nxsd_addon.components = [
        edizon,
        lockpickrcm,
        ldnmitm,
        sysclk,
        sysftpd,
        goldleaf,
        nxshell,
        incognito,
        # emuiibo,
        # amiiswap,
    ]

    return [nxsd_core, nxsd_addon]


if __name__ == '__main__':
    main()
