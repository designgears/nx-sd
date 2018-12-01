import logging
import subprocess

from nxsd import util
from nxsd.packages import NXSDPackage
from pathlib import Path

TINFOIL_VERSION = 'master'


class TinfoilPackage(NXSDPackage):

    def build(self):
        self.config.logger.info('Building Tinfoil {version}...'.format(version=TINFOIL_VERSION))

        tinfoil_root = Path(self.config.components_dir, 'tinfoil/')
        with util.change_dir(tinfoil_root):
            build_commands = [
                'git fetch origin',
                'git checkout {version}'.format(version=TINFOIL_VERSION),
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
        self.config.logger.info('Packing Tinfoil {version}...'.format(version=TINFOIL_VERSION))

        component_dict = {
            'tinfoil': (
                Path(self.config.components_dir, 'tinfoil/tinfoil.nro'),
                Path(self.config.build_dir, 'sdcard/switch/Tinfoil/tinfoil.nro'),
            ),
        }

        self._copy_package_components(component_dict)


def get_package():
    return TinfoilPackage()
