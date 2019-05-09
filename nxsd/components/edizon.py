from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'EdiZon'
COMPONENT_VERSION = 'v3.0.1'
COMPONENT_COMMIT_OR_TAG = '22eddf6'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'
SCRIPTS_VERSION = 'master'


class EdizonComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)
        self._scripts_source_directory = Path(settings.components_directory, 'edizon-scripts/')

    def install(self, install_directory):
        self._build()

        dest_ams = Path(install_directory, 'sdcard/atmosphere/')
        dest_reinx = Path(install_directory, 'sdcard/ReiNX/')
        dest_nro = Path(install_directory, 'sdcard/switch/')

        component_dict = {
            'edizon': (
                Path(self._source_directory, 'out/EdiZon.nro'),
                Path(dest_nro, 'EdiZon/EdiZon.nro'),
            ),
            'configs': (
                Path(self._scripts_source_directory, 'Configs'),
                Path(dest_nro, 'EdiZon/editor'),
            ),
            'scripts': (
                Path(self._scripts_source_directory, 'Scripts'),
                Path(dest_nro, 'EdiZon/editor/scripts'),
            ),
            'cheats': (
                Path(self._scripts_source_directory, 'Cheats'),
                [
                    Path(dest_ams, 'titles'),
                    Path(dest_reinx, 'titles'),
                ]
            ),
        }
        self._copy_components(component_dict)

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
        self._build_scripts()

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

    def _build_scripts(self):
        with util.change_dir(self._scripts_source_directory):
            build_commands = [
                'git fetch origin',
                'git checkout {} && git reset --hard && git pull'.format(SCRIPTS_VERSION),
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return EdizonComponent()
