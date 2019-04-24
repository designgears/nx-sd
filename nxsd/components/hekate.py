import os
from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'hekate'
COMPONENT_VERSION = 'v4.10.1'
COMPONENT_COMMIT_OR_TAG = 'v4.10.1'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class HekateComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        dest_bootloader = Path(install_directory, 'sdcard/bootloader/')
        dest_ams = Path(install_directory, 'sdcard/atmosphere/')

        component_dict = {
            'payload': (
                Path(self._source_directory, 'output/hekate.bin'),
                [
                    Path(install_directory, 'payloads/hekate-{}.bin'.format(COMPONENT_VERSION)),
                    Path(dest_ams, 'reboot_payload.bin'),
                ],
            ),
            'sleep-module': (
                Path(self._source_directory, 'output/libsys_lp0.bso'),
                Path(dest_bootloader, 'sys/libsys_lp0.bso'),
            ),
            'config': (
                Path(settings.defaults_directory, 'hekate/hekate_ipl.ini'),
                Path(dest_bootloader, 'hekate_ipl.ini'),
            ),
        }
        self._copy_components(component_dict)

        ini_dir = Path(dest_bootloader, 'ini')
        ini_dir.mkdir(parents=True, exist_ok=True)

        payloads_dir = Path(dest_bootloader, 'payloads')
        payloads_dir.mkdir(parents=True, exist_ok=True)

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
                'git checkout {} && git reset --hard'.format(COMPONENT_COMMIT_OR_TAG),
                'docker run --rm -a stdout -a stderr --name {} --mount src="$(cd ../../ && pwd)",target=/developer,type=bind {}:latest'.format(
                    DOCKER_IMAGE_NAME, DOCKER_IMAGE_NAME),
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return HekateComponent()
