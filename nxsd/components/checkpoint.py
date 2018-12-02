from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

CHECKPOINT_VERSION = 'v3.5.0'


class CheckpointComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'Checkpoint'
        self._version_string = CHECKPOINT_VERSION

        self._source_directory = Path(settings.components_directory, 'checkpoint/')

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
            self._execute_shell_commands(['make clean'])

    def _build(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git checkout {version}'.format(version=CHECKPOINT_VERSION),
                'make -C switch',
            ]
            self._execute_shell_commands(build_commands)


def get_component():
    return CheckpointComponent()
