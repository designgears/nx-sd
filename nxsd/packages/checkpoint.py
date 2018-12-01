import logging
import subprocess

from nxsd import util
from nxsd.packages import NXSDPackage
from pathlib import Path

CHECKPOINT_VERSION = 'v3.5.0'


class CheckpointPackage(NXSDPackage):

    def build(self):
        self.config.logger.info('Building Checkpoint {version}...'.format(version=CHECKPOINT_VERSION))

        checkpoint_root = Path(self.config.components_dir, 'checkpoint/')
        with util.change_dir(checkpoint_root):
            build_commands = [
                'git fetch origin',
                'git checkout {version}'.format(version=CHECKPOINT_VERSION),
                'make -C switch',
            ]

            for command in build_commands:
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                with process.stdout:
                    self._log_stream_output(logging.DEBUG, process.stdout)
                with process.stderr:
                    self._log_stream_output(logging.ERROR, process.stderr)

                process.wait()

    def pack(self):
        self.config.logger.info('Packing Checkpoint {version}...'.format(version=CHECKPOINT_VERSION))

        component_dict = {
            'checkpoint': (
                Path(self.config.components_dir, 'checkpoint/switch/out/Checkpoint.nro'),
                Path(self.config.build_dir, 'sdcard/switch/Checkpoint/Checkpoint.nro'),
            ),
        }

        self._copy_package_components(component_dict)


def get_package():
    return CheckpointPackage()
