from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'Sigpatches'
SIGPATCHES_VERSION = '8.0.1'


class SigpatchesComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = SIGPATCHES_VERSION

    def has_all_dependencies(self):
        # No dependencies
        return True

    def install(self, install_directory):
        component_dict = {
            'fs-patches': (
                Path(settings.components_directory, 'sigpatches/es_patches/'),
                Path(install_directory, 'sdcard/atmosphere/exefs_patches/es_patches/'),
            ),
            'es-patches': (
                Path(settings.components_directory, 'sigpatches/fs_patches/'),
                Path(install_directory, 'sdcard/atmosphere/kip_patches/fs_patches/'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        # no-op. Nothing to clean.
        pass


def get_component():
    return SigpatchesComponent()
