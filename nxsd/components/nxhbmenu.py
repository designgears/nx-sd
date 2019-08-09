from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'nx-hbmenu'
COMPONENT_VERSION = 'v3.1.0'
COMPONENT_COMMIT_OR_TAG = 'd7c37c6'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class HBMenuComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        dest_sd = Path(install_directory, 'sdcard/')

        component_dict = {
            'hbmenu': (
                Path(self._source_directory, 'nx-hbmenu.nro'),
                Path(dest_sd, 'hbmenu.nro'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git clean -fdx',
                'git submodule foreach --recursive git clean -fdx',
                'git reset --hard',
                'git submodule update --init --recursive',
                'docker image rm {d}'.format(d=DOCKER_IMAGE_NAME),
            ]
            util.execute_shell_commands(build_commands)

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
                'git reset --hard',
                'git checkout {c} && git reset --hard {c}'.format(c=COMPONENT_COMMIT_OR_TAG),
                'git submodule update --init --recursive',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return HBMenuComponent()
