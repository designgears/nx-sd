from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'Lockpick_RCM'
COMPONENT_VERSION = 'v1.8.1'
COMPONENT_COMMIT_OR_TAG = 'e72e486'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'

class LockpickRCMComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        dest_hekate = Path(install_directory, 'sdcard/bootloader')

        component_dict = {
            'payload': (
                Path(self._source_directory, 'output/Lockpick_RCM.bin'),
                [
                    Path(install_directory, 'payloads/Lockpick_RCM.bin'),
                    Path(dest_hekate, 'payloads/Lockpick_RCM.bin'),
                ],
            ),
            'ini': (
                Path(settings.defaults_directory, COMPONENT_NAME, 'Lockpick_RCM.ini'),
                Path(dest_hekate, 'ini/Lockpick_RCM.ini'),
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
    return LockpickRCMComponent()
