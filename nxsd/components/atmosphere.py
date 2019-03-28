import os
from nxsd import util
from nxsd.components import _dependencies as dependencies
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

ATMOSPHERE_VERSION = '994d7d5'


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

        os.environ['SEPT_ENC_PATH'] = '{}atmosphere/sept-secondary.enc'.format(settings.defaults_directory)

        dest_ams = Path(install_directory, 'sdcard/atmosphere/')
        dest_nro = Path(install_directory, 'sdcard/switch/')
        dest_spt = Path(install_directory, 'sdcard/sept/')

        component_dict = {
            'ams_mitm': (
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
            'dmnt': (
                Path(self._source_directory, 'stratosphere/dmnt/dmnt.nsp'),
                Path(dest_ams, 'titles/010000000000000D/exefs.nsp'),
            ),
            'sept-primary': (
                Path(self._source_directory, 'sept/sept-primary/sept-primary.bin'),
                Path(dest_spt, 'sept-primary.bin'),
            ),
            'sept-secondary': (
                Path(self._source_directory, 'sept/sept-secondary/sept-secondary.bin'),
                Path(dest_spt, 'sept-secondary.bin'),
            ),
            'sept-secondary-enc': (
                Path(settings.defaults_directory, 'atmosphere/sept-secondary.enc'),
                Path(dest_spt, 'sept-secondary.enc'),
            ),
            'sept-payload': (
                Path(self._source_directory, 'fusee/fusee-secondary/fusee-secondary.bin'),
                Path(dest_spt, 'payload.bin'),
            ),
            'fusee-secondary': (
                Path(self._source_directory, 'fusee/fusee-secondary/fusee-secondary.bin'),
                Path(dest_ams, 'fusee-secondary.bin'),
            ),
            'reboot-payload-nro': (
                Path(self._source_directory, 'troposphere/reboot_to_payload/reboot_to_payload.nro'),
                Path(dest_nro, 'reboot_to_payload.nro'),
            ),
            'no-gc': (
                Path(self._source_directory, 'common/defaults/kip_patches/default_nogc/'),
                Path(dest_ams, 'kip_patches/default_nogc/'),
            ),
            'hbl-html': (
                Path(self._source_directory, 'common/defaults/hbl_html/accessible-urls/'),
                Path(dest_ams, 'hbl_html/accessible-urls/'),
            ),
            'bct.ini': (
                Path(self._source_directory, 'common/defaults/BCT.ini'),
                Path(dest_ams, 'BCT.ini'),
            ),
            'system-settings': (
                Path(settings.defaults_directory, 'atmosphere/system_settings.ini'),
                Path(dest_ams, 'system_settings.ini'),
            ),
        }
        self._copy_components(component_dict)

        _, ams_mitm_dir = component_dict['ams_mitm']
        ams_mitm_flags_dir = Path(ams_mitm_dir.parent, 'flags')
        ams_mitm_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(ams_mitm_flags_dir, 'boot2.flag'), 'a').close()

    def clean(self):
        with util.change_dir(self._source_directory):
            util.execute_shell_commands([
                'make clean',
                # manually clean troposphere due to makefile issues
                'make clean -C troposphere',
            ])

    def _build(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git checkout {}'.format(ATMOSPHERE_VERSION),
                'git pull --recurse-submodules',
                'make',
                # manually build troposphere due to makefile issues
                'make -C troposphere',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return AtmosphereComponent()
