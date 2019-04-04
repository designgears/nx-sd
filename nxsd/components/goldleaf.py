from nxsd import util
from nxsd.components import _dependencies as dependencies
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

GOLDLEAF_VERSION = 'v0.5'
GOLDLEAF_COMMIT_OR_TAG = '0.5'


class GoldleafComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'Goldleaf'
        self._version_string = GOLDLEAF_VERSION

        self._source_directory = Path(settings.components_directory, 'ldn_mitm/')

    def has_all_dependencies(self):
        if not dependencies.check_core_dependencies():
            return False

        return True

    def install(self, install_directory):
        self._build()

        dest_switch = Path(install_directory, 'sdcard/switch/')

        component_dict = {
            'app': (
                Path(self._source_directory, 'Goldleaf/Goldleaf.nro'),
                Path(dest_switch, 'Goldleaf.nro'),
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
                'git checkout {}'.format(GOLDLEAF_COMMIT_OR_TAG),
                'make',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return GoldleafComponent()
