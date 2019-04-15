from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

EDIZON_VERSION = 'v3.0.1'
EDIZON_COMMIT_OR_TAG = 'ffee462'
SCRIPTS_VERSION = 'master'


class EdizonComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'EdiZon + Scripts + Cheats'
        self._version_string = EDIZON_VERSION

        self._source_directory = Path(settings.components_directory, 'edizon/')
        self._scripts_source_directory = Path(settings.components_directory, 'edizon-scripts/')

    def install(self, install_directory):
        self._build()

        dest_ams = Path(install_directory, 'sdcard/atmosphere/')
        dest_nro = Path(install_directory, 'sdcard/switch/')

        component_dict = {
            'edizon': (
                Path(self._source_directory, 'out/EdiZon.nro'),
                Path(dest_nro, 'EdiZon/EdiZon.nro'),
            ),
            'configs': (
                Path(self._scripts_source_directory, 'Configs'),
                Path(dest_nro, 'EdiZon/editor'),
            ),
            'scripts': (
                Path(self._scripts_source_directory, 'Scripts'),
                Path(dest_nro, 'EdiZon/editor/scripts'),
            ),
            'cheats': (
                Path(self._scripts_source_directory, 'Cheats'),
                Path(dest_ams, 'titles'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        with util.change_dir(self._source_directory):
            util.execute_shell_commands(['make clean'])

    def _build(self):
        self._build_edizon()
        self._build_scripts()

    def _build_edizon(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git checkout {}'.format(EDIZON_COMMIT_OR_TAG),
                'make -j12',
            ]
            util.execute_shell_commands(build_commands)

    def _build_scripts(self):
        with util.change_dir(self._scripts_source_directory):
            build_commands = [
                'git fetch origin',
                'git checkout {}'.format(SCRIPTS_VERSION),
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return EdizonComponent()
