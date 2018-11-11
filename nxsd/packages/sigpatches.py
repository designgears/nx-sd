from nxsd.packages import NXSDPackage
from pathlib import Path

# Corresponds to Nintendo Switch system software version
SIGPATCHES_VERSION = '6.1.0'


class SigpatchesPackage(NXSDPackage):

    def build(self):
        # no-op. Nothing to build.
        pass

    def pack(self):
        component_dict = {
            'es-patches': (
                Path(self.config.components_dir, 'sigpatches/'),
                Path(self.config.build_dir, 'sdcard/atmosphere/exefs_patches/sigpatches/'),
            ),
        }

        self._copy_package_components(component_dict)


def get_package():
    return SigpatchesPackage()
