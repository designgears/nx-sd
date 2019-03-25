from nxsd import util
from nxsd.components import _dependencies as dependencies
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

EDIZON_VERSION = 'v3.0.1'


class EdizonComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'EdiZon'
        self._version_string = EDIZON_VERSION

        self._source_directory = Path(settings.components_directory, 'edizon/')

    def has_all_dependencies(self):
        if not dependencies.check_core_dependencies():
            return False

        dependency_list = [
            dependencies.SWITCH_FREETYPE
        ]

        if not dependencies.check_dependencies(dependency_list):
            return False
        
        return True

    def install(self, install_directory):
        self._build()

        component_dict = {
            'edizon': (
                Path(self._source_directory, 'out/EdiZon.nro'),
                Path(install_directory, 'sdcard/switch/EdiZon/EdiZon.nro'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        with util.change_dir(self._source_directory):
            util.execute_shell_commands(['make clean'])

    def _build(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git checkout {version}'.format(version=EDIZON_VERSION),
                'make',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return EdizonComponent()
