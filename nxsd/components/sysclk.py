import os
from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'sys-clk'
COMPONENT_VERSION = 'v0.12.2'
COMPONENT_COMMIT_OR_TAG = '0.12.2'
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
            'titles': (
                Path(self._source_directory, 'out/sys-clk.nsp'),
                Path(dest_ams, 'titles/00FF0000636C6BFF/exefs.nsp'),
            ),
            'config': (
                Path(settings.defaults_directory, 'sys-clk/config.ini'),
                Path(dest_conf, 'sys-clk/config.ini'),
            ),
        }
        self._copy_components(component_dict)

        _, titles_dir = component_dict['titles']
        titles_flags_dir = Path(titles_dir.parent, 'flags')
        titles_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(titles_flags_dir, 'boot2.flag'), 'a').close()

        _, config_dir = component_dict['config']
        config_flags_dir = Path(config_dir.parent)
        open(Path(config_flags_dir, 'log.flag'), 'a').close()

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
                'docker run --rm -a stdout -a stderr --name {} --mount src="$(cd ../../ && pwd)",target=/developer,type=bind {}:latest'.format(
                    DOCKER_IMAGE_NAME, DOCKER_IMAGE_NAME),
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return SysCLKComponent()
