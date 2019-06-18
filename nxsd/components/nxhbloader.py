from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'nx-hbloader'
COMPONENT_VERSION = 'v2.1'
COMPONENT_COMMIT_OR_TAG = '3af8c89'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class HBLoaderComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        dest_ams = Path(install_directory, 'sdcard/atmosphere/')
        dest_reinx = Path(install_directory, 'sdcard/ReiNX')

        component_dict = {
            'hbloader': (
                Path(self._source_directory, 'hbl.nsp'),
                [
                    Path(dest_ams, 'hbl.nsp'),
                    Path(dest_reinx, 'hbl.nsp'),
                ]
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
        self._build_docker()
        self._build_component()

    def _build_docker(self):
        with util.change_dir(self._dockerfiles_directory):
            build_commands = [
                'docker build . -t {d}:latest'.format(d=DOCKER_IMAGE_NAME),
            ]
            util.execute_shell_commands(build_commands)

    def _build_component(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git checkout {c} && git reset --hard {c}'.format(c=COMPONENT_COMMIT_OR_TAG),
                'git submodule update --init --recursive',
                'docker run --rm -a stdout -a stderr --name {d} --mount src="{bd}",target=/developer,type=bind {d}:latest'.format(
                    d=DOCKER_IMAGE_NAME, bd=Path().absolute().parent.parent),
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return HBLoaderComponent()
