from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'Atmosphere'
COMPONENT_VERSION = 'v0.8.10'
COMPONENT_COMMIT_OR_TAG = '0.8.10'
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
        dest_switch = Path(install_directory, 'sdcard/switch')

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
            'fusee-primary': (
                Path(self._source_directory, 'fusee/fusee-primary/fusee-primary.bin'),
                Path(install_directory, 'payloads/fusee-primary.bin'),
            ),
            'fusee-secondary': (
                Path(self._source_directory, 'fusee/fusee-secondary/fusee-secondary.bin'),
                Path(dest_ams, 'fusee-secondary.bin'),
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
            'bootlogo': (
                Path(settings.defaults_directory, 'atmosphere/bootlogo.bmp'),
                Path(dest_ams, 'bootlogo.bmp'),
            ),
        }
        self._copy_components(component_dict)

        fatal_errors_dir = Path(dest_ams, 'fatal_errors')
        fatal_errors_dir.mkdir(parents=True, exist_ok=True)

        _, eclct_stub_dir = component_dict['eclct.stub']
        eclct_stub_flags_dir = Path(eclct_stub_dir.parent, 'flags')
        eclct_stub_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(eclct_stub_flags_dir, 'boot2.flag'), 'a').close()

        atmos_flags_dir = Path(dest_ams, 'flags')
        atmos_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(atmos_flags_dir, 'hbl_bis_write.flag'), 'a').close()
        open(Path(atmos_flags_dir, 'hbl_cal_read.flag'), 'a').close()

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
                'git submodule update --init --recursive',
                'git checkout {c} && git reset --hard {c}'.format(c=COMPONENT_COMMIT_OR_TAG),
                'docker run --rm -a stdout -a stderr --name {d} --mount src="{bd}",target=/developer,type=bind {d}:latest'.format(
                    d=DOCKER_IMAGE_NAME, bd=Path().absolute().parent.parent),
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return AtmosphereComponent()
