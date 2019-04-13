from nxsd import util
from nxsd.components import _dependencies as dependencies
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

EDIZON_VERSION = 'v3.0.1'
EDIZON_COMMIT_OR_TAG = 'ffee462'
SCRIPTS_VERSION = 'master'
LIBNX_COMMIT_OR_TAG = 'v2.1.0'


class EdizonComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'EdiZon + Scripts + Cheats'
        self._version_string = EDIZON_VERSION

        self._edizon_source_directory = Path(settings.components_directory, 'edizon/')
        self._scripts_source_directory = Path(settings.components_directory, 'edizon-scripts/')
        self._libnx_source_directory = Path(settings.components_directory, 'libnx/')

    def has_all_dependencies(self):
        if not dependencies.check_core_dependencies():
            return False

        dependency_list = [
            dependencies.SWITCH_CURL,
            dependencies.SWITCH_FREETYPE
        ]

        if not dependencies.check_dependencies(dependency_list):
            return False
        
        return True

    def install(self, install_directory):
        self._build()

        dest_ams = Path(install_directory, 'sdcard/atmosphere/')
        dest_nro = Path(install_directory, 'sdcard/switch/')
        edizon_conf = Path(install_directory, 'sdcard/EdiZon/')

        component_dict = {
            'edizon': (
                Path(self._edizon_source_directory, 'out/EdiZon.nro'),
                Path(dest_nro, 'EdiZon/EdiZon.nro'),
            ),
            'configs': (
                Path(self._scripts_source_directory, 'Configs'),
                Path(edizon_conf, 'editor'),
            ),
            'scripts': (
                Path(self._scripts_source_directory, 'Scripts'),
                Path(edizon_conf, 'editor/scripts'),
            ),
            'cheats': (
                Path(self._scripts_source_directory, 'Cheats'),
                Path(dest_ams, 'titles'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        with util.change_dir(self._edizon_source_directory):
            util.execute_shell_commands(['make clean'])

    def _build(self):
        self._build_libnx()
        self._build_edizon()
        self._build_scripts()

    def _build_edizon(self):
        with util.change_dir(self._edizon_source_directory):
            build_commands = [
                'git fetch origin',
                'git checkout {}'.format(EDIZON_COMMIT_OR_TAG),
                'make',
            ]
            util.execute_shell_commands(build_commands)

    def _build_scripts(self):
        with util.change_dir(self._scripts_source_directory):
            build_commands = [
                'git fetch origin',
                'git checkout {}'.format(SCRIPTS_VERSION),
            ]
            util.execute_shell_commands(build_commands)

    def _build_libnx(self):
        with util.change_dir(self._libnx_source_directory):
            build_commands = [
                'git fetch origin',
                'git submodule update --recursive',
                'git checkout {}'.format(LIBNX_COMMIT_OR_TAG),
                'make install',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return EdizonComponent()
