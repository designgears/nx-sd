import logging
import subprocess

from nxsd import util
from nxsd.packages import NXSDPackage
from pathlib import Path

ATMOSPHERE_VERSION = '0.7.5'


class AtmospherePackage(NXSDPackage):

    def build(self):
        self.config.logger.info('Building Atmosphere {version}...'.format(version=ATMOSPHERE_VERSION))

        ams_root = Path(self.config.components_dir, 'atmosphere/')
        with util.change_dir(ams_root):
            build_commands = [
                'git fetch origin',
                'git submodule update --recursive',
                'git checkout {version}'.format(version=ATMOSPHERE_VERSION),
                'make',
            ]

            for command in build_commands:
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                with process.stdout:
                    self._log_stream_output(logging.DEBUG, process.stdout)
                with process.stderr:
                    self._log_stream_output(logging.ERROR, process.stderr)

                process.wait()

    def pack(self):
        self.config.logger.info('Packing Atmosphere {version}...'.format(version=ATMOSPHERE_VERSION))

        ams_root = Path(self.config.components_dir, 'atmosphere/')
        dest_dir = Path(self.config.build_dir, 'sdcard/atmosphere/')

        component_dict = {
            'set_mitm': (
                Path(ams_root, 'stratosphere/set_mitm/set_mitm.nsp'),
                Path(dest_dir, 'titles/0100000000000032/exefs.nsp'),
            ),
            'creport': (
                Path(ams_root, 'stratosphere/creport/creport.nsp'),
                Path(dest_dir, 'titles/0100000000000036/exefs.nsp'),
            ),
            'fs_mitm': (
                Path(ams_root, 'stratosphere/fs_mitm/fs_mitm.kip'),
                Path(dest_dir, 'modules/core/fs_mitm.kip'),
            ),
            'loader': (
                Path(ams_root, 'stratosphere/loader/loader.kip'),
                Path(dest_dir, 'modules/core/loader.kip'),
            ),
            'pm': (
                Path(ams_root, 'stratosphere/pm/pm.kip'),
                Path(dest_dir, 'modules/core/pm.kip'),
            ),
            'sm': (
                Path(ams_root, 'stratosphere/sm/sm.kip'),
                Path(dest_dir, 'modules/core/sm.kip'),
            ),
            'secmon': (
                Path(ams_root, 'exosphere/exosphere.bin'),
                Path(dest_dir, 'secmon/secmon.bin'),
            ),
        }

        self._copy_package_components(component_dict)

        _, set_mitm_dir = component_dict['set_mitm']
        open(Path(set_mitm_dir.parent, 'boot2.flag'), 'a').close()


def get_package():
    return AtmospherePackage()
