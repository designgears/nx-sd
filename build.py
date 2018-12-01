#!/usr/bin/env python3

from nxsd.builder import NXSDBuilder, NXSDBuildConfig
from nxsd.packages import atmosphere
from nxsd.packages import hekate
from nxsd.packages import homebrew
from nxsd.packages import sigpatches
from nxsd.packages import checkpoint

OUTPUT_FILE = "nx-sd.zip"

BUILD_DIR = "build/"
COMPONENTS_DIR = "components/"
DEFAULTS_DIR = "defaults/"


def main():
    build_config = NXSDBuildConfig(
        build_dir=BUILD_DIR,
        components_dir=COMPONENTS_DIR,
        defaults_dir=DEFAULTS_DIR,
        output_path=OUTPUT_FILE
    )

    nxsd_builder = NXSDBuilder(build_config)
    package_list = [atmosphere, hekate, homebrew, sigpatches, checkpoint]
    for package in package_list:
        nxsd_builder.add_package(package.get_package())
    nxsd_builder.build_packages()


if __name__ == '__main__':
    main()
