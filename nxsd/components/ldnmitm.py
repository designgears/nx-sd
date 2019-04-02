from nxsd import util
from nxsd.components import _dependencies as dependencies
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

LDNMITM_VERSION = 'v1.1.2'
LOCKPICKRCM_COMMIT_OR_TAG = 'master'


class LdnmitmComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'ldn_mitm + ldnmitm_config'
        self._version_string = LDNMITM_VERSION

        self._source_directory = Path(settings.components_directory, 'ldn_mitm/')

    def has_all_dependencies(self):
        if not dependencies.check_core_dependencies():
            return False

        return True

    def install(self, install_directory):
        self._build()
        
        dest_ams = Path(install_directory, 'sdcard/atmosphere/')
        dest_nro = Path(install_directory, 'sdcard/switch/')

        component_dict = {
            'kip': (
                Path(self._source_directory, 'ldn_mitm/ldn_mitm.kip'),
                Path(dest_ams, 'kips/ldn_mitm.kip'),
            ),
            'config-app': (
                Path(self._source_directory, 'ldnmitm_config/ldnmitm_config.nro'),
                Path(dest_nro, 'ldnmitm_config.nro'),
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
                'git checkout {}'.format(LOCKPICKRCM_COMMIT_OR_TAG),
                'make',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return LdnmitmComponent()
