import os
from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'switch-zstd'
COMPONENT_VERSION = 'v1.4.3'
COMPONENT_COMMIT_OR_TAG = '4f8345f'
COMPONENT_DIR = 'pacman-packages/switch/zstd'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class SwitchZstdComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_DIR)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        awoo_install_dir = Path(settings.dockerfiles_directory, 'Awoo-Installer')

        component_dict = {
            'package': (
                Path(self._source_directory, 'switch-zstd-1.4.3-1-any.pkg.tar.xz'),
                [
                    Path(install_directory, 'switch-zstd-1.4.3-1-any.pkg.tar.xz'),
                    Path(awoo_install_dir, 'switch-zstd-1.4.3-1-any.pkg.tar.xz'),
                ]
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        with util.change_dir(self._source_directory):
            util.clean_component(DOCKER_IMAGE_NAME, COMPONENT_COMMIT_OR_TAG)

    def _build(self):
        self._build_docker()
        
    def _build_docker(self):
        with util.change_dir(self._dockerfiles_directory):
            util.dock_worker(DOCKER_IMAGE_NAME)

def get_component():
    return SwitchZstdComponent()
