from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

HBLOADER_VERSION = 'v2.0.1'
HBMENU_VERSION = 'v3.0.1'


class HomebrewComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'nx-hbloader + nx-hbmenu'
        self._version_string = '{}/{}'.format(HBLOADER_VERSION, HBMENU_VERSION)

        self._hbloader_source_directory = Path(settings.components_directory, 'nx-hbloader/')
        self._hbmenu_source_directory = Path(settings.components_directory, 'nx-hbmenu/')

    def install(self, install_directory):
        self._build()

        dest_sd = Path(install_directory, 'sdcard/')

        component_dict = {
            'hbloader': (
                Path(self._hbloader_source_directory, 'hbl.nsp'),
                Path(dest_sd, 'atmosphere/hbl.nsp'),
            ),
            'hbmenu': (
                Path(self._hbmenu_source_directory, 'nx-hbmenu.nro'),
                Path(dest_sd, 'hbmenu.nro'),
            ),
            'config': (
                Path(settings.defaults_directory, 'atmosphere/loader.ini'),
                Path(dest_sd, 'atmosphere/loader.ini'),
            ),
        }
        self._copy_components(component_dict)

    def _build(self):
        self._build_hbloader()
        self._build_hbmenu()

    def _build_hbloader(self):
        component_root = Path(settings.components_directory, 'nx-hbloader/')
        with util.change_dir(component_root):
            build_commands = [
                'git fetch origin',
                'git checkout {version}'.format(version=HBLOADER_VERSION),
                'make',
            ]
            self._execute_shell_commands(build_commands)

    def _build_hbmenu(self):
        component_root = Path(settings.components_directory, 'nx-hbmenu/')
        with util.change_dir(component_root):
            build_commands = [
                'git fetch origin',
                'git checkout {version}'.format(version=HBMENU_VERSION),
                'make nx',
            ]
            self._execute_shell_commands(build_commands)


def get_component():
    return HomebrewComponent()
