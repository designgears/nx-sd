import os
from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'hekate'
COMPONENT_VERSION = 'v4.10.2J'
COMPONENT_COMMIT_OR_TAG = '5142b77'
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

        dest_hekate = Path(install_directory, 'sdcard/bootloader2/')
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
                Path(dest_hekate, 'sys/libsys_lp0.bso'),
            ),
            'minerva': (
                Path(self._source_directory, 'output/libsys_minerva.bso'),
                Path(dest_hekate, 'sys/libsys_minerva.bso'),
            ),
            'config': (
                Path(settings.defaults_directory, 'hekate/hekate_ipl.ini'),
                Path(dest_hekate, 'hekate_ipl.ini'),
            ),
            'bootlogo': (
                Path(settings.defaults_directory, 'hekate/bootlogo.bmp'),
                Path(dest_hekate, 'bootlogo.bmp'),
            ),
        }
        self._copy_components(component_dict)

        ini_dir = Path(dest_hekate, 'ini')
        ini_dir.mkdir(parents=True, exist_ok=True)

        payloads_dir = Path(dest_hekate, 'payloads')
        payloads_dir.mkdir(parents=True, exist_ok=True)

    def clean(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git clean -fdx',
                'git submodule foreach --recursive git clean -fdx',
                'docker image ls | grep {d} -c > /dev/null && docker image rm {d} || echo "No image to delete."'.format(
                    d=DOCKER_IMAGE_NAME),
            ]
            util.execute_shell_commands(build_commands)

    def _build(self):
        self._build_docker()
        self._build_component()

    def _build_docker(self):
        with util.change_dir(self._dockerfiles_directory):
            build_commands = [
                'docker image ls | grep {d} -c > /dev/null && echo "Using existing image." || docker build . -t {d}:latest'.format(
                    d=DOCKER_IMAGE_NAME),
            ]
            util.execute_shell_commands(build_commands)

    def _build_component(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git submodule update --init --recursive',
                'git checkout {c} && git reset --hard {c}'.format(c=COMPONENT_COMMIT_OR_TAG),
                'docker run --rm -a stdout -a stderr --name {d} --mount src="$(cd ../.. && pwd)",target=/developer,type=bind {d}:latest'.format(
                    d=DOCKER_IMAGE_NAME),
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return HekateComponent()
