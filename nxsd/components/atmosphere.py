from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'Atmosphere'
COMPONENT_VERSION = 'v0.9.2'
COMPONENT_COMMIT_OR_TAG = 'd95e209'
COMPONENT_BRANCH = 'master'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class AtmosphereComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        dest_ams = Path(install_directory, 'sdcard/atmosphere/')
        dest_sept = Path(install_directory, 'sdcard/sept/')

        component_dict = {
            'dmnt': (
                Path(self._source_directory, 'stratosphere/dmnt/dmnt.nsp'),
                Path(dest_ams, 'titles/010000000000000D/exefs.nsp'),
            ),
            'eclct.stub': (
                Path(self._source_directory, 'stratosphere/eclct.stub/eclct.stub.nsp'),
                Path(dest_ams, 'titles/0100000000000032/exefs.nsp'),
            ),
            'fatal': (
                Path(self._source_directory, 'stratosphere/fatal/fatal.nsp'),
                Path(dest_ams, 'titles/0100000000000034/exefs.nsp'),
            ),
            'creport': (
                Path(self._source_directory, 'stratosphere/creport/creport.nsp'),
                Path(dest_ams, 'titles/0100000000000036/exefs.nsp'),
            ),
            'ro': (
                Path(self._source_directory, 'stratosphere/ro/ro.nsp'),
                Path(dest_ams, 'titles/0100000000000037/exefs.nsp'),
            ),
            'fusee-primary': (
                Path(self._source_directory, 'fusee/fusee-primary/fusee-primary.bin'),
                [
                    Path(install_directory, 'payloads/fusee-primary.bin'),
                    Path(dest_ams, 'reboot_payload.bin'),
                ],
            ),
            'fusee-secondary': (
                Path(self._source_directory, 'fusee/fusee-secondary/fusee-secondary.bin'),
                [
                    Path(dest_ams, 'fusee-secondary.bin'),
                    Path(dest_sept, 'payload.bin'),
                ],
            ),
            'hbl-html': (
                Path(self._source_directory, 'common/defaults/hbl_html/'),
                Path(dest_ams, 'hbl_html/'),
            ),
            'no-gc': (
                Path(self._source_directory, 'common/defaults/kip_patches/default_nogc/'),
                Path(dest_ams, 'kip_patches/default_nogc/'),
            ),
            'bct.ini': (
                Path(settings.defaults_directory, 'atmosphere/BCT.ini'),
                Path(dest_ams, 'BCT.ini'),
            ),
            'loader.ini': (
                Path(self._source_directory, 'common/defaults/loader.ini'),
                Path(dest_ams, 'loader.ini'),
            ),
            'system-settings': (
                Path(settings.defaults_directory, 'atmosphere/system_settings.ini'),
                Path(dest_ams, 'system_settings.ini'),
            ),
            'sept-primary': (
                Path(self._source_directory, 'sept/sept-primary/sept-primary.bin'),
                Path(dest_sept, 'sept-primary.bin'),
            ),
            'sept-secondary_00-enc': (
                Path(self._dockerfiles_directory, 'sept-secondary_00.enc'),
                Path(dest_sept, 'sept-secondary_00.enc'),
            ),
            'sept-secondary_01-enc': (
                Path(self._dockerfiles_directory, 'sept-secondary_01.enc'),
                Path(dest_sept, 'sept-secondary_01.enc'),
            ),
            'boot2.flag': (
                Path(settings.defaults_directory, 'boot2.flag'),
                [
                    Path(dest_ams, 'titles/0100000000000032/flags/boot2.flag'),
                    Path(dest_ams, 'titles/0100000000000037/flags/boot2.flag'),
                ],
            ),
            'bootlogo': (
                Path(settings.defaults_directory, 'atmosphere/bootlogo.bmp'),
                Path(dest_ams, 'bootlogo.bmp'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git clean -fdx',
                'git submodule foreach --recursive git clean -fdx',
                'git submodule foreach --recursive git reset --hard',
                'git submodule update --init --recursive',
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
                'git submodule foreach --recursive git reset --hard',
                'git checkout {b} && git pull && git reset --hard {c}'.format(c=COMPONENT_COMMIT_OR_TAG, b=COMPONENT_BRANCH),
                'git submodule update --init --recursive',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return AtmosphereComponent()
