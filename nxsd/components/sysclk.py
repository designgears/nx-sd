import os
from nxsd import util
from nxsd.components import _dependencies as dependencies
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

SYSCLK_VERSION = '0.11.1'
SYSCLK_COMMIT_OR_TAG = '9e98488'

class SysCLKComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'sys-CLK'
        self._version_string = SYSCLK_VERSION

        self._source_directory = Path(settings.components_directory, 'sys-clk/')

    def has_all_dependencies(self):
        if not dependencies.check_core_dependencies():
            return False
        
        return True

    def install(self, install_directory):
        self._build()

        dest_ams = Path(install_directory, 'sdcard/atmosphere/')
        dest_conf = Path(install_directory, 'sdcard/config/')
        
        component_dict = {
            'titles': (
                Path(self._source_directory, 'out/sys-clk.nsp'),
                Path(dest_ams, 'titles/00FF0000636C6BFF/exefs.nsp'),
            ),
            'config': (
                Path(settings.defaults_directory, 'sys-clk/config.ini'),
                Path(dest_conf, 'sys-clk/config.ini'),
            ),
        }
        self._copy_components(component_dict)

        _, titles_dir = component_dict['titles']
        titles_flags_dir = Path(titles_dir.parent, 'flags')
        titles_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(titles_flags_dir, 'boot2.flag'), 'a').close()

        _, config_dir = component_dict['config']
        config_flags_dir = Path(config_dir.parent)
        open(Path(config_flags_dir, 'log.flag'), 'a').close()

    def clean(self):
        with util.change_dir(self._source_directory):
            util.execute_shell_commands(['make clean'])

    def _build(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git checkout {}'.format(SYSCLK_COMMIT_OR_TAG),
                'make',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return SysCLKComponent()
