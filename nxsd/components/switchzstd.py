import os
from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'switch-zstd'
COMPONENT_VERSION = 'v1.4.3'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class SwitchZstdComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

    def clean(self):
        build_commands = [
            'docker inspect "{d}" > /dev/null 2>&1 && docker image rm {d} || echo "No image to delete."'.format(
                d=DOCKER_IMAGE_NAME),
        ]
        util.execute_shell_commands(build_commands)

    def _build(self):
        self._build_docker()
        
    def _build_docker(self):
        with util.change_dir(self._dockerfiles_directory):
            util.dock_worker(DOCKER_IMAGE_NAME)

def get_component():
    return SwitchZstdComponent()
