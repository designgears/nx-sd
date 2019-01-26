from nxsd import util
from nxsd.components import _dependencies as dependencies
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

ATMOSPHERE_VERSION = '0.8.3'


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

        component_dict = {
            'set_mitm': (
                Path(self._source_directory, 'stratosphere/set_mitm/set_mitm.nsp'),
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
            'fs-mitm': (
                Path(self._source_directory, 'stratosphere/fs_mitm/fs_mitm.kip'),
                Path(dest_ams, 'modules/core/fs_mitm.kip'),
            ),
            'loader': (
                Path(self._source_directory, 'stratosphere/loader/loader.kip'),
                Path(dest_ams, 'modules/core/loader.kip'),
            ),
            'pm': (
                Path(self._source_directory, 'stratosphere/pm/pm.kip'),
                Path(dest_ams, 'modules/core/pm.kip'),
            ),
            'sm': (
                Path(self._source_directory, 'stratosphere/sm/sm.kip'),
                Path(dest_ams, 'modules/core/sm.kip'),
            ),
            'secmon': (
                Path(self._source_directory, 'exosphere/exosphere.bin'),
                Path(dest_ams, 'secmon/exosphere.bin'),
            ),
            'reboot-to-payload': (
                Path(self._source_directory, 'troposphere/reboot_to_payload/reboot_to_payload.nro'),
                Path(dest_ams, 'reboot_to_payload.bin'),
            ),
            'no-gc': (
                Path(self._source_directory, 'common/defaults/kip_patches/default_nogc/'),
                Path(dest_ams, 'kip_patches/default_nogc/'),
            ),
            'bct.ini': (
                Path(self._source_directory, 'common/defaults/BCT.ini'),
                Path(dest_ams, 'BCT.ini'),
            ),
            'system-settings': (
                Path(self._source_directory, 'common/defaults/system_settings.ini'),
                Path(dest_ams, 'system_settings.ini'),
            ),
        }
        self._copy_components(component_dict)

        _, set_mitm_dir = component_dict['set_mitm']
        set_mitm_flags_dir = Path(set_mitm_dir.parent, 'flags')
        set_mitm_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(set_mitm_flags_dir, 'boot2.flag'), 'a').close()

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
                'git submodule update --recursive',
                'git checkout {}'.format(ATMOSPHERE_VERSION),
                'make',
                # manually build troposphere due to makefile issues
                'make -C troposphere',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return AtmosphereComponent()
