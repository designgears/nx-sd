from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

# Corresponds to Nintendo Switch system software version
SIGPATCHES_VERSION = '7.0.1'


class SigpatchesComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'Sigpatches'
        self._version_string = SIGPATCHES_VERSION

    def has_all_dependencies(self):
        # No dependencies
        return True

    def install(self, install_directory):

        dest_ams = Path(install_directory, 'sdcard/atmosphere/')

        component_dict = {
            'es-patches': (
                Path(settings.components_directory, 'sigpatches/exefs_patches/es_patches/'),
                Path(dest_ams, 'exefs_patches/es_patches/'),
            ),
            'fs-patches': (
                Path(settings.components_directory, 'sigpatches/kip_patches/fs_patches/'),
                Path(dest_ams, 'kip_patches/fs_patches/'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        # no-op. Nothing to clean.
        pass


def get_component():
    return SigpatchesComponent()
