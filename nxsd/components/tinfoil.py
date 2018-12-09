from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

TINFOIL_VERSION = 'master'


class TinfoilComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'Tinfoil'
        self._version_string = TINFOIL_VERSION

        self._source_directory = Path(settings.components_directory, 'tinfoil/')

    def install(self, install_directory):
        self._build()
        component_dict = {
            'tinfoil': (
                Path(self._source_directory, 'tinfoil.nro'),
                Path(install_directory, 'sdcard/switch/Tinfoil/tinfoil.nro'),
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
                'git checkout {version}'.format(version=TINFOIL_VERSION),
                'make',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return TinfoilComponent()
