import os
from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'sys-ftpd'
COMPONENT_VERSION = 'v1.0' # fake version, doesn't seem to have a version
COMPONENT_COMMIT_OR_TAG = '4fed6f5'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class SysftpdComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        dest_ams = Path(install_directory, 'sdcard/atmosphere/')
        dest_sd = Path(install_directory, 'sdcard/')
        
        component_dict = {
            'titles': (
                Path(self._source_directory, 'sys-ftpd.nsp'),
                Path(dest_ams, 'titles/420000000000000E/exefs.nsp'),
            ),
            'config': (
                Path(self._source_directory, 'sd_card/ftpd/'),
                Path(dest_sd, 'config/sys-ftpd/'),
            ),
        }
        self._copy_components(component_dict)

        _, titles_dir = component_dict['titles']
        titles_flags_dir = Path(titles_dir.parent, 'flags')
        titles_flags_dir.mkdir(parents=True, exist_ok=True)
        # open(Path(titles_flags_dir, 'boot2.flag'), 'a').close()

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
    return SysftpdComponent()
