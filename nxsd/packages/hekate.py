import subprocess

from nxsd import util
from nxsd.packages import NXSDPackage
from pathlib import Path

HEKATE_VERSION = 'v4.2'


class HekatePackage(NXSDPackage):

    def build(self):
        output_dev = open('build.log', 'a')
        error_dev = open('error.log', 'a')

        hekate_root = Path(self.config.components_dir, 'hekate/')
        with util.change_dir(hekate_root):
            subprocess.call(['git', 'fetch', 'origin'], stdout=output_dev, stderr=error_dev)
            subprocess.call(['git', 'checkout', HEKATE_VERSION], stdout=output_dev, stderr=error_dev)
            subprocess.call('make', stdout=output_dev, stderr=error_dev)

        output_dev.close()
        error_dev.close()

    def pack(self):
        hekate_root = Path(self.config.components_dir, 'hekate/')
        payload_dest_dir = Path(self.config.build_dir, 'payload/')
        sdcard_dest_dir = Path(self.config.build_dir, 'sdcard/bootloader/')

        component_dict = {
            'payload': (
                Path(hekate_root, 'output/hekate.bin'),
                Path(payload_dest_dir, 'hekate.bin')
            ),
            'sleep_module': (
                Path(hekate_root, 'output/libsys_lp0.bso'),
                Path(sdcard_dest_dir, 'sys/libsys_lp0.bso')
            ),
            'config': (
                Path(self.config.defaults_dir, 'bootloader/hekate_ipl.ini'),
                Path(sdcard_dest_dir, 'hekate_ipl.ini')
            ),
        }

        self._copy_package_components(component_dict)


def get_package():
    return HekatePackage()
