#!/usr/bin/env python3

import logging

from nxsd.builder import NXSDBuilder, NXSDBuildConfig
from nxsd.packages import atmosphere
from nxsd.packages import hekate
from nxsd.packages import homebrew
from nxsd.packages import sigpatches
from nxsd.packages import checkpoint
from nxsd.packages import tinfoil


BUILD_DIR_CORE = 'build/core/'
OUTPUT_FILE_CORE = 'nx-sd.zip'

BUILD_DIR_ADDON = 'build/addon/'
OUTPUT_FILE_ADDON = 'nx-sd-addon.zip'

COMPONENTS_DIR = 'components/'
DEFAULTS_DIR = 'defaults/'


def main():
    logger = logging.getLogger('nxsd')

    nxsd_core_config = NXSDBuildConfig(
        build_dir=BUILD_DIR_CORE,
        components_dir=COMPONENTS_DIR,
        defaults_dir=DEFAULTS_DIR,
        output_path=OUTPUT_FILE_CORE,
        logger=logger,
    )
    nxsd_core = (
        'nxsd-core',
        NXSDBuilder(nxsd_core_config),
        [atmosphere, hekate, homebrew, sigpatches],
    )

    nxsd_addon_config = NXSDBuildConfig(
        build_dir=BUILD_DIR_ADDON,
        components_dir=COMPONENTS_DIR,
        defaults_dir=DEFAULTS_DIR,
        output_path=OUTPUT_FILE_ADDON,
        logger=logger,
    )
    nxsd_addon = (
        'nxsd-addon',
        NXSDBuilder(nxsd_addon_config),
        [checkpoint, tinfoil],
    )

    builders = [nxsd_core, nxsd_addon]
    for name, builder, packages in builders:
        for package in packages:
            builder.add_package(package.get_package())

        builder.build_packages()
        logger.info('Created {name} package!'.format(name=name))


if __name__ == '__main__':
    main()
