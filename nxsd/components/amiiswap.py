import os
from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'AmiiSwap'
COMPONENT_VERSION = 'v0.1.3'
COMPONENT_COMMIT_OR_TAG = 'master'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class AmiiSwapComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        dest_nro = Path(install_directory, 'sdcard/switch/')
        
        component_dict = {
            'app': (
                Path(self._source_directory, 'AmiiSwap.nro'),
                Path(dest_nro, 'AmiiSwap/AmiiSwap.nro'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git clean -fdx',
                'git submodule foreach --recursive git clean -fdx',
                'docker image ls | grep {} -c > /dev/null && docker image rm {} || echo "No image to delete."'.format(
                    DOCKER_IMAGE_NAME, DOCKER_IMAGE_NAME),
            ]
            util.execute_shell_commands(build_commands)

    def _build(self):
        self._build_docker()
        self._build_component()

    def _build_docker(self):
        with util.change_dir(self._dockerfiles_directory):
            build_commands = [
                'docker image ls | grep {} -c > /dev/null && echo "Using existing image." || docker build . -t {}:latest'.format(
                    DOCKER_IMAGE_NAME, DOCKER_IMAGE_NAME),
            ]
            util.execute_shell_commands(build_commands)

    def _build_component(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git submodule update --init --recursive',
                'git checkout {} && git reset --hard && git pull'.format(COMPONENT_COMMIT_OR_TAG),
                'docker run -it --rm -a stdout -a stderr --name {} --mount src="$(cd ../../ && pwd)",target=/developer,type=bind {}:latest'.format(
                    DOCKER_IMAGE_NAME, DOCKER_IMAGE_NAME),
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return AmiiSwapComponent()
