from nxsd import util
from nxsd.components import _dependencies as dependencies
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

CHECKPOINT_VERSION = 'v3.6.0'


class CheckpointComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'Checkpoint'
        self._version_string = CHECKPOINT_VERSION

        self._source_directory = Path(settings.components_directory, 'checkpoint/')

    def has_all_dependencies(self):
        if not dependencies.check_core_dependencies():
            return False

        dependency_list = [
            dependencies.SWITCH_SDL2_GFX,
            dependencies.SWITCH_SDL2_IMAGE,
            dependencies.SWITCH_SDL2_TTF
        ]

        if not dependencies.check_dependencies(dependency_list):
            return False
        
        return True

    def install(self, install_directory):
        self._build()

        component_dict = {
            'checkpoint': (
                Path(self._source_directory, 'switch/out/Checkpoint.nro'),
                Path(install_directory, 'sdcard/switch/Checkpoint/Checkpoint.nro'),
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
                'git submodule update --recursive',
                'git checkout {version}'.format(version=CHECKPOINT_VERSION),
                'make switch',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return CheckpointComponent()
