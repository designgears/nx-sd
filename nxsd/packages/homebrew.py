import subprocess

from nxsd import util
from nxsd.packages import NXSDPackage
from pathlib import Path

HBLOADER_VERSION = 'v2.0.1'
HBMENU_VERSION = 'v3.0.0'


class HomebrewPackage(NXSDPackage):

    def build(self):
        output_dev = open('build.log', 'a')
        error_dev = open('error.log', 'a')

        # Build nx-hbloader
        hbloader_root = Path(self.config.components_dir, 'nx-hbloader/')
        with util.change_dir(hbloader_root):
            subprocess.call(['git', 'checkout', HBLOADER_VERSION], stdout=output_dev, stderr=error_dev)
            subprocess.call('make', stdout=output_dev, stderr=error_dev)

        # Build nx-hbmenu
        hbmenu_root = Path(self.config.components_dir, 'nx-hbmenu/')
        with util.change_dir(hbmenu_root):
            subprocess.call(['git', 'checkout', HBMENU_VERSION], stdout=output_dev, stderr=error_dev)
            subprocess.call(['make', 'nx'], stdout=output_dev, stderr=error_dev)

        output_dev.close()
        error_dev.close()

    def pack(self):
        hbloader_root = Path(self.config.components_dir, 'nx-hbloader/')
        hbmenu_root = Path(self.config.components_dir, 'nx-hbmenu/')
        dest_dir = Path(self.config.build_dir, 'sdcard/')

        component_dict = {
            'hbloader': (
                Path(hbloader_root, 'hbl.nsp'),
                Path(dest_dir, 'atmosphere/hbl.nsp'),
            ),
            'hbmenu': (
                Path(hbmenu_root, 'nx-hbmenu.nro'),
                Path(dest_dir, 'hbmenu.nro'),
            ),
            'config': (
                Path(self.config.defaults_dir, 'atmosphere/loader.ini'),
                Path(dest_dir, 'atmosphere/loader.ini'),
            ),
        }

        self._copy_package_components(component_dict)


def get_package():
    return HomebrewPackage()
