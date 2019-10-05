import os
from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'sys-clk'
COMPONENT_VERSION = 'v0.13.0'
COMPONENT_COMMIT_OR_TAG = 'bb598fa'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class SysCLKComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        dest_ams = Path(install_directory, 'sdcard/atmosphere/')
        dest_conf = Path(install_directory, 'sdcard/config/')

        component_dict = {
            'title': (
                Path(self._source_directory, 'sysmodule/out/sys-clk.nsp'),
                Path(dest_ams, 'titles/00FF0000636C6BFF/exefs.nsp'),
            ),
            'config': (
                Path(settings.defaults_directory, 'sys-clk/config.ini'),
                Path(dest_conf, 'sys-clk/config.ini'),
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
    return SysCLKComponent()
