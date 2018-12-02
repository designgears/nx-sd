#!/usr/bin/env python3

import logging

from nxsd.package import NXSDPackage
from nxsd.components import atmosphere
from nxsd.components import hekate
from nxsd.components import homebrew
from nxsd.components import sigpatches
from nxsd.components import checkpoint
from nxsd.components import tinfoil


logger = logging.getLogger('nxsd')


def main():
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
        tinfoil
    ]

    packages = [nxsd_core, nxsd_addon]
    for package in packages:
        package.build_components()
        logger.info('Created {name} package!'.format(name=package.name))


if __name__ == '__main__':
    main()
