#!/usr/bin/env python3

import argparse
import logging
import nxsd

from nxsd.package import NXSDPackage
from nxsd.components import atmosphere
from nxsd.components import hekate
from nxsd.components import homebrew
from nxsd.components import sigpatches
from nxsd.components import checkpoint
from nxsd.components import edizon
from nxsd.components import lockpickrcm


def main():
    commands = {
        'build': build,
        'clean': clean,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', 
        help='enable verbose logging output to log/build.log')
    parser.add_argument('command', nargs='?', default='build', 
        choices=commands.keys(),
        help='build command to execute. options: build, clean (default: build)')

    args = parser.parse_args()

    if args.verbose:
        nxsd.logger.setLevel(logging.DEBUG)
        nxsd.logger.debug('Verbose logging enabled.')
    
    commands[args.command](args)

def build(args):
    packages = get_packages()
    for package in packages:
        if package.build_components():
            nxsd.logger.info('Created {name} package!'.format(name=package.name))
        else:
            nxsd.logger.info('Failed to create {name} package! Check build.log for details.'.format(name=package.name))
        

def clean(args):
    packages = get_packages()
    for package in packages:
        package.clean()
        nxsd.logger.info('Cleaned {name} package!'.format(name=package.name))
    pass

def get_packages():
    nxsd_core = NXSDPackage(
        name='nxsd-core',
        build_directory='build/core/',
        output_filename='nx-sd.zip',
    )
    nxsd_core.components = [
        atmosphere,
        hekate,
        homebrew,
        sigpatches,
    ]

    nxsd_addon = NXSDPackage(
        name='nxsd-addon',
        build_directory='build/addon/',
        output_filename='nx-sd-addon.zip',
    )
    nxsd_addon.components = [
        checkpoint,
        edizon,
        lockpickrcm,
    ]

    return [nxsd_core, nxsd_addon]


if __name__ == '__main__':
    main()
