from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'Sigpatches'
COMPONENT_VERSION = '7.0.1'


class SigpatchesComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)

    def install(self, install_directory):

        dest_ams = Path(install_directory, 'sdcard/atmosphere/')

        component_dict = {
            'es-patches': (
                Path(self._source_directory, 'exefs_patches/es_patches/'),
                Path(dest_ams, 'exefs_patches/es_patches/'),
            ),
            'fs-patches': (
                Path(self._source_directory, 'kip_patches/fs_patches/'),
                Path(dest_ams, 'kip_patches/fs_patches/'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        # no-op. Nothing to clean.
        pass


def get_component():
    return SigpatchesComponent()
