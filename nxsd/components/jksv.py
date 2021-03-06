from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'JKSV'
COMPONENT_VERSION = '04.30.2020'
COMPONENT_COMMIT_OR_TAG = '1e03cba'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class JKSVComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)
        self._defaults_directory = Path(settings.defaults_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        dest_switch = Path(install_directory, 'sdcard/switch')

        component_dict = {
            'nro': (
                Path(self._source_directory, 'JKSV.nro'),
                Path(dest_switch, 'JKSV', 'JKSV.nro'),
            ),
            'config': (
                Path(self._defaults_directory, 'jksv_dir.txt'),
                Path(dest_switch, 'jksv_dir.txt'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        with util.change_dir(self._source_directory):
            util.clean_component(DOCKER_IMAGE_NAME, COMPONENT_COMMIT_OR_TAG)

    def _build(self):
        self._build_prepare()
        self._build_docker()
        
    def _build_docker(self):
        with util.change_dir(self._dockerfiles_directory):
            util.dock_worker(DOCKER_IMAGE_NAME)

    def _build_prepare(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git checkout {c} && git reset --hard {c}'.format(c=COMPONENT_COMMIT_OR_TAG),
                'git submodule update --init --recursive',
            ]
            util.execute_shell_commands(build_commands)

def get_component():
    return JKSVComponent()
