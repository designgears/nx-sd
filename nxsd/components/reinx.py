import os
from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'ReiNX'
COMPONENT_VERSION = 'v2.2.1'
COMPONENT_COMMIT_OR_TAG = '948e2db'
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
                Path(self._source_directory, 'out/sept/payload.bin'),
                Path(dest_reinx, 'septchainloader.bin'),
            ),
            'splash': (
                Path(self._source_directory, 'out/ReiNX/splash.bin'),
                Path(dest_reinx, 'splash.bin'),
            ),
            'patches': (
                Path(self._source_directory, 'out/ReiNX/patches/es_patch.rxp'),
                Path(dest_reinx, 'patches/es_patch.rxp'),
            ),
            'loader': (
                Path(self._source_directory, 'out/ReiNX/sysmodules/loader.kip'),
                Path(dest_reinx, 'sysmodules/loader.kip'),
            ),
            'pm': (
                Path(self._source_directory, 'out/ReiNX/sysmodules/pm.kip'),
                Path(dest_reinx, 'sysmodules/pm.kip'),
            ),
            'rnx_mitm': (
                Path(self._source_directory, 'out/ReiNX/sysmodules/rnx_mitm.kip'),
                Path(dest_reinx, 'sysmodules/rnx_mitm.kip'),
            ),
            'sm': (
                Path(self._source_directory, 'out/ReiNX/sysmodules/sm.kip'),
                Path(dest_reinx, 'sysmodules/sm.kip'),
            ),
            'dmnt': (
                Path(self._source_directory, 'out/ReiNX/titles/010000000000000D/exefs.nsp'),
                Path(dest_reinx, 'titles/010000000000000D/exefs.nsp'),
            ),
            'fatal': (
                Path(self._source_directory, 'out/ReiNX/titles/0100000000000034/exefs.nsp'),
                Path(dest_reinx, 'titles/0100000000000034/exefs.nsp'),
            ),
            'creport': (
                Path(self._source_directory, 'out/ReiNX/titles/0100000000000036/exefs.nsp'),
                Path(dest_reinx, 'titles/0100000000000036/exefs.nsp'),
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
        }
        self._copy_components(component_dict)

        disabled_sysmodules_dir = Path(dest_reinx, 'sysmodules.dis')
        disabled_sysmodules_dir.mkdir(parents=True, exist_ok=True)

        _, dmnt_dir = component_dict['dmnt']
        dmnt_flags_dir = Path(dmnt_dir.parent, 'flags')
        dmnt_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(dmnt_flags_dir, 'boot2.flag'), 'a').close()

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
