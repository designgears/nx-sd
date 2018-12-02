from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

# Corresponds to Nintendo Switch system software version
SIGPATCHES_VERSION = '6.1.0'


class SigpatchesComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = 'Sigpatches'
        self._version_string = SIGPATCHES_VERSION

    def install(self, install_directory):
        component_dict = {
            'es-patches': (
                Path(settings.components_directory, 'sigpatches/'),
                Path(install_directory, 'sdcard/atmosphere/exefs_patches/sigpatches/'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        # no-op. Nothing to clean.
        pass


def get_component():
    return SigpatchesComponent()
