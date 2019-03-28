import os
from nxsd import util
from nxsd.components import _dependencies as dependencies
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

LIBNX_VERSION = 'a4c23a0'


class LibNXComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'libnx'
        self._version_string = LIBNX_VERSION

        self._source_directory = Path(
            settings.components_directory, 'libnx/')

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

    def clean(self):
        with util.change_dir(self._source_directory):
            util.execute_shell_commands(['make clean'])

    def _build(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch origin',
                'git submodule update --recursive',
                'git checkout {version}'.format(version=LIBNX_VERSION),
                'make',
                'make install',
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return LibNXComponent()
