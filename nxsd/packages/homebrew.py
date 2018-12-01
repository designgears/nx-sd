import logging
import subprocess

from nxsd import util
from nxsd.packages import NXSDPackage
from pathlib import Path

HBLOADER_VERSION = 'v2.0.1'
HBMENU_VERSION = 'v3.0.1'


class HomebrewPackage(NXSDPackage):

    def build(self):
        self._build_hbloader()
        self._build_hbmenu()

    def _build_hbloader(self):
        self.config.logger.info('Building nx-hbloader {version}...'.format(version=HBLOADER_VERSION))

        hbloader_root = Path(self.config.components_dir, 'nx-hbloader/')
        with util.change_dir(hbloader_root):
            build_commands = [
                'git fetch origin',
                'git checkout {version}'.format(version=HBLOADER_VERSION),
                'make',
            ]

            for command in build_commands:
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                with process.stdout:
                    self._log_stream_output(logging.DEBUG, process.stdout)
                with process.stderr:
                    self._log_stream_output(logging.ERROR, process.stderr)

                process.wait()

    def _build_hbmenu(self):
        self.config.logger.info('Building nx-hbmenu {version}...'.format(version=HBMENU_VERSION))

        hbmenu_root = Path(self.config.components_dir, 'nx-hbmenu/')
        with util.change_dir(hbmenu_root):
            build_commands = [
                'git fetch origin',
                'git checkout {version}'.format(version=HBMENU_VERSION),
                'make nx',
            ]

            for command in build_commands:
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                with process.stdout:
                    self._log_stream_output(logging.DEBUG, process.stdout)
                with process.stderr:
                    self._log_stream_output(logging.ERROR, process.stderr)

                process.wait()

    def pack(self):
        self.config.logger.info('Packing nx-hbloader {loaderversion} and nx-hbmenu {menuversion}...'.format(
            loaderversion=HBLOADER_VERSION,
            menuversion=HBMENU_VERSION))

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
