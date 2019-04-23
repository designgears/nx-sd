import os

from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'Atmosphere'
COMPONENT_VERSION = 'v0.8.8'
COMPONENT_COMMIT_OR_TAG = 'master'
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
        dest_boot = Path(install_directory, 'sdcard/bootloader/')
        dest_sept = Path(install_directory, 'sdcard/sept/')
        dest_switch = Path(install_directory, 'sdcard/switch')

        component_dict = {
            'dmnt': (
                Path(self._source_directory, 'stratosphere/dmnt/dmnt.nsp'),
                Path(dest_ams, 'titles/010000000000000D/exefs.nsp'),
            ),
            'eclct.stub': (
                Path(self._source_directory,
                     'stratosphere/eclct.stub/eclct.stub.nsp'),
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
            'fusee-primary': (
                Path(self._source_directory, 'fusee/fusee-primary/fusee-primary.bin'),
                [
                    Path(dest_boot, 'payloads/fusee-primary.bin'),
                    Path(install_directory, 'payloads/fusee-primary.bin'),
                ],
            ),
            'fusee-secondary': (
                Path(self._source_directory, 'fusee/fusee-secondary/fusee-secondary.bin'),
                [
                    Path(dest_ams, 'fusee-secondary.bin'),
                    Path(dest_sept, 'payload.bin'),
                ],
            ),
            'sept-primary': (
                Path(self._source_directory, 'sept/sept-primary/sept-primary.bin'),
                Path(dest_sept, 'sept-primary.bin'),
            ),
            'sept-secondary-enc': (
                Path(self._source_directory, 'sept/sept-secondary/sept-secondary.enc'),
                Path(dest_sept, 'sept-secondary.enc'),
            ),
            'reboot-to-payload': (
                Path(self._source_directory, 'troposphere/reboot_to_payload/reboot_to_payload.nro'),
                Path(dest_switch, 'reboot_to_payload/reboot_to_payload.nro'),
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
                Path(self._source_directory, 'common/defaults/BCT.ini'),
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
        }
        self._copy_components(component_dict)

        _, eclct_stub_dir = component_dict['eclct.stub']
        eclct_stub_flags_dir = Path(eclct_stub_dir.parent, 'flags')
        eclct_stub_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(eclct_stub_flags_dir, 'boot2.flag'), 'a').close()

        fatal_errors_dir = Path(dest_ams, 'fatal_errors')
        fatal_errors_dir.mkdir(parents=True, exist_ok=True)

        atmos_flags_dir = Path(dest_ams, 'flags')
        atmos_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(atmos_flags_dir, 'hbl_bis_write.flag'), 'a').close()
        open(Path(atmos_flags_dir, 'hbl_cal_read.flag'), 'a').close()

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
    return AtmosphereComponent()
