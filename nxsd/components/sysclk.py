import os
from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'sys-clk'
COMPONENT_VERSION = 'v0.12.3'
COMPONENT_COMMIT_OR_TAG = '5e78c80'
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

        component_dict = {
            'titles': (
                Path(self._source_directory, 'out/sys-clk.nsp'),
                Path(dest_ams, 'titles/00FF0000636C6BFF/exefs.nsp'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git clean -fdx',
                'git submodule foreach --recursive git clean -fdx',
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
                'git checkout {c} && git reset --hard {c}'.format(c=COMPONENT_COMMIT_OR_TAG),
                'git submodule update --init --recursive',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return SysCLKComponent()
