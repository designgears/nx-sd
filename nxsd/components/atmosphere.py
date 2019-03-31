import os

from nxsd import util
from nxsd.components import _dependencies as dependencies
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

ATMOSPHERE_VERSION = 'v0.8.6'
ATMOSPHERE_COMMIT_OR_TAG = '994d7d5'


class AtmosphereComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'Atmosphere'
        self._version_string = ATMOSPHERE_VERSION

        self._source_directory = Path(settings.components_directory, 'atmosphere/')

    def has_all_dependencies(self):
        if not dependencies.check_core_dependencies():
            return False

        if not util.check_environment_variable('DEVKITARM'):
            return False

        dependency_list = [
            dependencies.DEVKITARM,
            dependencies.SWITCH_FREETYPE,
        ]

        if not dependencies.check_dependencies(dependency_list):
            return False

        return True

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
            'sept-secondary': (
                Path(self._source_directory, 'sept/sept-secondary/sept-secondary.enc'),
                Path(dest_sept, 'sept-secondary.enc'),
            ),
            'reboot-to-payload': (
                Path(self._source_directory, 'troposphere/reboot_to_payload/reboot_to_payload.nro'),
                Path(dest_switch, 'reboot_to_payload.nro'),
            ),
            'hbl_html': (
                Path(self._source_directory, 'common/defaults/hbl_html/'),
                Path(dest_ams, 'hbl_html/'),
            ),
            'no-gc': (
                Path(self._source_directory,
                     'common/defaults/kip_patches/default_nogc/'),
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

    def clean(self):
        with util.change_dir(self._source_directory):
            util.execute_shell_commands([
                'make clean',
            ])

    def _build(self):
        # Use a pre-built copy of sept-secondary since the keys to sign sept are not publicly available.
        os.environ['SEPT_ENC_PATH'] = str( Path(settings.defaults_directory, 'sept/sept-secondary.enc').resolve())

        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git submodule update --recursive',
                'git checkout {}'.format(ATMOSPHERE_COMMIT_OR_TAG),
                'make',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return AtmosphereComponent()
