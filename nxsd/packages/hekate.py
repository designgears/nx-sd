import logging
import subprocess

from nxsd import util
from nxsd.packages import NXSDPackage
from pathlib import Path

HEKATE_VERSION = 'v4.2'


class HekatePackage(NXSDPackage):

    def build(self):
        self.config.logger.info('Building Hekate {version}...'.format(version=HEKATE_VERSION))

        hekate_root = Path(self.config.components_dir, 'hekate/')
        with util.change_dir(hekate_root):
            build_commands = [
                'git fetch origin',
                'git checkout {version}'.format(version=HEKATE_VERSION),
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
        self.config.logger.info('Packing Hekate {version}...'.format(version=HEKATE_VERSION))

        hekate_root = Path(self.config.components_dir, 'hekate/')
        payload_dest_dir = Path(self.config.build_dir, 'payload/')
        sdcard_dest_dir = Path(self.config.build_dir, 'sdcard/bootloader/')

        component_dict = {
            'payload': (
                Path(hekate_root, 'output/hekate.bin'),
                Path(payload_dest_dir, 'hekate.bin'),
            ),
            'sleep_module': (
                Path(hekate_root, 'output/libsys_lp0.bso'),
                Path(sdcard_dest_dir, 'sys/libsys_lp0.bso'),
            ),
            'config': (
                Path(self.config.defaults_dir, 'bootloader/hekate_ipl.ini'),
                Path(sdcard_dest_dir, 'hekate_ipl.ini'),
            ),
        }

        self._copy_package_components(component_dict)


def get_package():
    return HekatePackage()
