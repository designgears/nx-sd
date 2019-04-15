from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

LDNMITM_VERSION = 'v1.1.2'
LDNMITM_COMMIT_OR_TAG = '1d78707'


class LdnmitmComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'ldn_mitm + ldnmitm_config'
        self._version_string = LDNMITM_VERSION

        self._source_directory = Path(settings.components_directory, 'ldn-mitm/')

    def install(self, install_directory):
        self._build()
        
        dest_ams = Path(install_directory, 'sdcard/atmosphere/')
        dest_nro = Path(install_directory, 'sdcard/switch/')

        component_dict = {
            'ldn_mitm': (
                Path(self._source_directory, 'ldn_mitm/out/ldn_mitm.nsp'),
                Path(dest_ams, 'titles/4200000000000010/exefs.nsp'),
            ),
            'config-app': (
                Path(self._source_directory, 'ldnmitm_config/ldnmitm_config.nro'),
                Path(dest_nro, 'ldnmitm_config/ldnmitm_config.nro'),
            ),
        }
        self._copy_components(component_dict)

        _, ldn_mitm_stub_dir = component_dict['ldn_mitm']
        ldn_mitm_stub_flags_dir = Path(ldn_mitm_stub_dir.parent, 'flags')
        ldn_mitm_stub_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(ldn_mitm_stub_flags_dir, 'boot2.flag'), 'a').close()

    def clean(self):
        with util.change_dir(self._source_directory):
            util.execute_shell_commands(['make clean'])

    def _build(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git submodule update --recursive',
                'git checkout {}'.format(LDNMITM_COMMIT_OR_TAG),
                'make -j12',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return LdnmitmComponent()
