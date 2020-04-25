from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'nx-ovlloader'
COMPONENT_VERSION = 'v1.0.5'
COMPONENT_COMMIT_OR_TAG = '0f26f78'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class OvlLoaderComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        dest_contents = Path(install_directory, 'sdcard/atmosphere/contents')

        component_dict = {
            'contents': (
                Path(self._source_directory, 'ovll.nsp'),
                Path(dest_contents, '010000000007E51A/exefs.nsp'),
            ),
            'toolbox': (
                Path(self._source_directory, 'toolbox.json'),
                Path(dest_contents, '010000000007E51A/toolbox.json'),
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
    return OvlLoaderComponent()
