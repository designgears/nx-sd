import os
from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'ReiNX'
COMPONENT_VERSION = 'v2.3'
COMPONENT_COMMIT_OR_TAG = '186da77'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class ReiNXComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._ams_source_directory = Path(settings.components_directory, 'Atmosphere')
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        dest_sdcard = Path(install_directory, 'sdcard/')
        dest_reinx = Path(install_directory, 'sdcard/ReiNX')

        component_dict = {
            'payload': (
                Path(self._source_directory, 'out/ReiNX.bin'),
                [
                    Path(install_directory, 'payloads/ReiNX-{}.bin'.format(COMPONENT_VERSION)),
                    Path(dest_sdcard, 'ReiNX.bin'),
                ]
            ),
            'septchainloader': (
                Path(self._source_directory, 'septchainloader/out/payload.bin'),
                Path(dest_reinx, 'septchainloader.bin'),
            ),
            'patches': (
                Path(self._source_directory, 'data/es_patch.rxp'),
                Path(dest_reinx, 'patches/es_patch.rxp'),
            ),
            'loader': (
                Path(self._source_directory, 'NX_Sysmodules/loader/loader.kip'),
                Path(dest_reinx, 'sysmodules/loader.kip'),
            ),
            'pm': (
                Path(self._source_directory, 'NX_Sysmodules/pm/pm.kip'),
                Path(dest_reinx, 'sysmodules/pm.kip'),
            ),
            'ams_mitm': (
                Path(self._source_directory, 'NX_Sysmodules/ams_mitm/ams_mitm.kip'),
                Path(dest_reinx, 'sysmodules/ams_mitm.kip'),
            ),
            'sm': (
                Path(self._source_directory, 'NX_Sysmodules/sm/sm.kip'),
                Path(dest_reinx, 'sysmodules/sm.kip'),
            ),
            'dmnt': (
                Path(self._source_directory, 'NX_Sysmodules/dmnt/dmnt.nsp'),
                Path(dest_reinx, 'titles/010000000000000D/exefs.nsp'),
            ),
            'eclct.stub': (
                Path(self._source_directory, 'NX_Sysmodules/eclct.stub/eclct.stub.nsp'),
                Path(dest_reinx, 'titles/0100000000000032/exefs.nsp'),
            ),
            'fatal': (
                Path(self._source_directory, 'NX_Sysmodules/fatal/fatal.nsp'),
                Path(dest_reinx, 'titles/0100000000000034/exefs.nsp'),
            ),
            'creport': (
                Path(self._source_directory, 'NX_Sysmodules/creport/creport.nsp'),
                Path(dest_reinx, 'titles/0100000000000036/exefs.nsp'),
            ),
            'ro': (
                Path(self._source_directory, 'NX_Sysmodules/ro/ro.nsp'),
                Path(dest_reinx, 'titles/0100000000000037/exefs.nsp'),
            ),
            'ams-secmon': (
                Path(self._ams_source_directory, 'exosphere/exosphere.bin'),
                Path(dest_reinx, 'secmon.bin'),
            ),
            'ams-warmboot': (
                Path(self._ams_source_directory, 'exosphere/lp0fw/lp0fw.bin'),
                Path(dest_reinx, 'warmboot.bin'),
            ),
            'ams-sept-primary': (
                Path(self._ams_source_directory, 'sept/sept-primary/sept-primary.bin'),
                Path(dest_sdcard, 'sept/sept-primary.bin'),
            ),
            'ams-sept-secondary': (
                Path(self._ams_source_directory, 'sept/sept-secondary/sept-secondary.enc'),
                Path(dest_sdcard, 'sept/sept-secondary.enc'),
            ),
            'hbl-html': (
                Path(self._source_directory, 'NX_Sysmodules/common/defaults/hbl_html/'),
                Path(dest_reinx, 'hbl_html/'),
            ),
            'bct.ini': (
                Path(self._source_directory, 'NX_Sysmodules/common/defaults/BCT.ini'),
                Path(dest_reinx, 'BCT.ini'),
            ),
            'loader.ini': (
                Path(self._source_directory, 'NX_Sysmodules/common/defaults/loader.ini'),
                Path(dest_reinx, 'loader.ini'),
            ),
            'system-settings': (
                Path(self._source_directory, 'NX_Sysmodules/common/defaults/system_settings.ini'),
                Path(dest_reinx, 'system_settings.ini'),
            ),
            'splash': (
                Path(self._source_directory, 'data/splash.bin'),
                Path(dest_reinx, 'splash.bin'),
            ),
            'bootlogo': (
                Path(settings.defaults_directory, 'reinx/bootlogo.bmp'),
                Path(dest_reinx, 'bootlogo.bmp'),
            ),
        }
        self._copy_components(component_dict)

        disabled_sysmodules_dir = Path(dest_reinx, 'sysmodules.dis')
        disabled_sysmodules_dir.mkdir(parents=True, exist_ok=True)

        _, dmnt_dir = component_dict['dmnt']
        dmnt_flags_dir = Path(dmnt_dir.parent, 'flags')
        dmnt_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(dmnt_flags_dir, 'boot2.flag'), 'a').close()

        _, eclct_dir = component_dict['eclct.stub']
        eclct_flags_dir = Path(eclct_dir.parent, 'flags')
        eclct_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(eclct_flags_dir, 'boot2.flag'), 'a').close()

        _, ro_dir = component_dict['ro']
        ro_flags_dir = Path(ro_dir.parent, 'flags')
        ro_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(ro_flags_dir, 'boot2.flag'), 'a').close()

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
    return ReiNXComponent()
