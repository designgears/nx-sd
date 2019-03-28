from nxsd import util
from nxsd.components import _dependencies as dependencies
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

HEKATE_VERSION = 'master'


class HekateComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'Hekate'
        self._version_string = HEKATE_VERSION

        self._source_directory = Path(settings.components_directory, 'hekate/')

    def has_all_dependencies(self):
        if not dependencies.check_core_dependencies():
            return False
        
        if not util.check_environment_variable('DEVKITARM'):
            return False

        if not dependencies.check_dependency(dependencies.DEVKITARM):
            return False
        
        return True

    def install(self, install_directory):
        self._build()

        dest_bootloader = Path(install_directory, 'sdcard/bootloader/')
        dest_ams = Path(install_directory, 'sdcard/atmosphere/')
        
        component_dict = {
            'payload': (
                Path(self._source_directory, 'output/hekate.bin'),
                Path(install_directory, 'payload/hekate-{version}.bin'.format(version=HEKATE_VERSION)),
            ),
            'reboot-payload-bin': (
                Path(self._source_directory, 'output/hekate.bin'),
                Path(dest_ams, 'reboot_payload.bin'),
            ),
            'sleep_module': (
                Path(self._source_directory, 'output/libsys_lp0.bso'),
                Path(dest_bootloader, 'sys/libsys_lp0.bso'),
            ),
            'config': (
                Path(settings.defaults_directory, 'bootloader/hekate_ipl.ini'),
                Path(dest_bootloader, 'hekate_ipl.ini'),
            ),
        }
        self._copy_components(component_dict)

        ini_dir = Path(dest_bootloader, 'ini')
        ini_dir.mkdir(parents=True, exist_ok=True)

        payloads_dir = Path(dest_bootloader, 'payloads')
        payloads_dir.mkdir(parents=True, exist_ok=True)

    def clean(self):
        with util.change_dir(self._source_directory):
            util.execute_shell_commands(['make clean'])

    def _build(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git checkout {version}'.format(version=HEKATE_VERSION),
                'git pull --recurse-submodules',
                'make',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return HekateComponent()
