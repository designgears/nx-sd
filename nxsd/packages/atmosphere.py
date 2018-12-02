import logging
import subprocess

from nxsd import util
from nxsd.packages import NXSDPackage
from pathlib import Path

ATMOSPHERE_VERSION = '0.8.1'


class AtmospherePackage(NXSDPackage):

    def build(self):
        self.config.logger.info('Building Atmosphere {version}...'.format(version=ATMOSPHERE_VERSION))

        ams_root = Path(self.config.components_dir, 'atmosphere/')

        # Need to apply a Makefile patch for fatal to use a custom build of libnx.
        # Latest libnx (1.6.0) does not properly build Atmosphere 0.8.x due
        # to missing GPU dependencies.
        fatal_patch = Path(self.config.patches_dir, 'fatal.patch').resolve()
        with util.change_dir(ams_root):
            build_commands = [
                'git fetch origin',
                'git submodule update --recursive',
                'git checkout {version}'.format(version=ATMOSPHERE_VERSION),
                'git apply {path}'.format(path=str(fatal_patch)),
                'make',
                'git reset --hard',
            ]

            for command in build_commands:
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                with process.stdout:
                    self._log_stream_output(logging.DEBUG, process.stdout)
                with process.stderr:
                    self._log_stream_output(logging.ERROR, process.stderr)

                process.wait()

    def pack(self):
        self.config.logger.info('Packing Atmosphere {version}...'.format(version=ATMOSPHERE_VERSION))

        ams_root = Path(self.config.components_dir, 'atmosphere/')

        dest_sd = Path(self.config.build_dir, 'sdcard/')
        dest_ams = Path(dest_sd, 'atmosphere/')

        component_dict = {
            'set_mitm': (
                Path(ams_root, 'stratosphere/set_mitm/set_mitm.nsp'),
                Path(dest_ams, 'titles/0100000000000032/exefs.nsp'),
            ),
            'fatal': (
                Path(ams_root, 'stratosphere/fatal/fatal.nsp'),
                Path(dest_ams, 'titles/0100000000000034/exefs.nsp'),
            ),
            'creport': (
                Path(ams_root, 'stratosphere/creport/creport.nsp'),
                Path(dest_ams, 'titles/0100000000000036/exefs.nsp'),
            ),
            'no-gc': (
                Path(ams_root, 'common/defaults/kip_patches/default_nogc/'),
                Path(dest_ams, 'kip_patches/default_nogc/'),
            ),
            'fusee-primary': (
                Path(ams_root, 'fusee/fusee-primary/fusee-primary.bin'),
                Path(dest_sd, 'bootloader/payloads/fusee-primary.bin'),
            ),
            'fusee-secondary': (
                Path(ams_root, 'fusee/fusee-secondary/fusee-secondary.bin'),
                Path(dest_sd, 'fusee-secondary.bin'),
            ),
            'bct.ini': (
                Path(ams_root, 'common/defaults/BCT.ini'),
                Path(dest_sd, 'BCT.ini'),
            ),
        }

        self._copy_package_components(component_dict)

        _, set_mitm_dir = component_dict['set_mitm']
        set_mitm_flags_dir = Path(set_mitm_dir.parent, 'flags')
        set_mitm_flags_dir.mkdir(parents=True, exist_ok=True)
        open(Path(set_mitm_flags_dir, 'boot2.flag'), 'a').close()


def get_package():
    return AtmospherePackage()
