import subprocess

from nxsd import util
from nxsd.packages import NXSDPackage
from pathlib import Path

CHECKPOINT_VERSION = 'v3.5.0'


class CheckpointPackage(NXSDPackage):

    def build(self):
        output_dev = open('build.log', 'a')
        error_dev = open('error.log', 'a')

        checkpoint_root = Path(self.config.components_dir, 'checkpoint/')
        with util.change_dir(checkpoint_root):
            subprocess.call(['git', 'fetch', 'origin'], stdout=output_dev, stderr=error_dev)
            subprocess.call(['git', 'checkout', CHECKPOINT_VERSION], stdout=output_dev, stderr=error_dev)
            subprocess.call(['make', '-C', 'switch'], stdout=output_dev, stderr=error_dev)

        output_dev.close()
        error_dev.close()

    def pack(self):
        component_dict = {
            'checkpoint': (
                Path(self.config.components_dir, 'checkpoint/switch/out/Checkpoint.nro'),
                Path(self.config.build_dir, 'sdcard/switch/Checkpoint/Checkpoint.nro'),
            ),
        }

        self._copy_package_components(component_dict)


def get_package():
    return CheckpointPackage()
