from nxsd import util
from nxsd.components import _dependencies as dependencies
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

ATMOSPHERE_VERSION = '0.8.2'


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
            # Custom libnx for building `fatal`. This can be removed
            # once latest libnx release can build Atmosphere.
            dependencies.NXSDDependency(
                name='libnx.newgpu',
                paths=[Path(dependencies.dkp_root, 'libnx.newgpu/lib/libnx.a')]
            )
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
            'no-gc': (
                Path(self._source_directory, 'common/defaults/kip_patches/default_nogc/'),
                Path(dest_ams, 'kip_patches/default_nogc/'),
            ),
            'bct.ini': (
                Path(self._source_directory, 'common/defaults/BCT.ini'),
                Path(dest_ams, 'BCT.ini'),
            ),
        }
        self._copy_components(component_dict)

        _, set_mitm_dir = component_dict['set_mitm']
        set_mitm_flags_dir = Path(set_mitm_dir.parent, 'flags')
        set_mitm_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(set_mitm_flags_dir, 'boot2.flag'), 'a').close()

    def clean(self):
        with util.change_dir(self._source_directory):
            util.execute_shell_commands(['make clean'])

    def _build(self):
        # Need to apply a Makefile patch for fatal to use a custom build of
        # libnx. Latest libnx (1.6.0) does not properly build Atmosphere 0.8.x
        # due to missing GPU dependencies.
        fatal_patch = Path(settings.patches_directory, 'fatal.patch').resolve()
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git submodule update --recursive',
                'git checkout {}'.format(ATMOSPHERE_VERSION),
                'git apply {}'.format(str(fatal_patch)),
                'make',
                'git reset --hard',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return AtmosphereComponent()
