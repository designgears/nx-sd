from nxsd import util
from nxsd.components import NXSDComponent
from nxsd.config import settings
from pathlib import Path

COMPONENT_NAME = 'Atmosphere'
COMPONENT_VERSION = 'v0.12.0'
COMPONENT_COMMIT_OR_TAG = '7bc0250'
COMPONENT_BRANCH = 'master'
DOCKER_IMAGE_NAME = COMPONENT_NAME.lower()+'-builder'


class AtmosphereComponent(NXSDComponent):

    def __init__(self):
        super().__init__()
        self._name = COMPONENT_NAME
        self._version_string = COMPONENT_VERSION+'-'+COMPONENT_COMMIT_OR_TAG

        self._source_directory = Path(settings.components_directory, COMPONENT_NAME)
        self._dockerfiles_directory = Path(settings.dockerfiles_directory, COMPONENT_NAME)
        self._defaults_directory = Path(settings.defaults_directory, COMPONENT_NAME)

    def install(self, install_directory):
        self._build()

        dest_sd = Path(install_directory, 'sdcard')
        dest_ams = Path(dest_sd, 'atmosphere')
        dest_sept = Path(dest_sd, 'sept')
        dest_hekate = Path(dest_sd, 'bootloader')

        component_dict = {
            'dmnt': (
                Path(self._source_directory, 'stratosphere/dmnt/dmnt.nsp'),
                Path(dest_ams, 'contents/010000000000000D/exefs.nsp'),
            ),
            'erpt': (
                Path(self._source_directory, 'stratosphere/erpt/erpt.nsp'),
                Path(dest_ams, 'contents/010000000000002B/exefs.nsp'),
            ),
            'boot2': (
                Path(self._source_directory, 'stratosphere/boot2/boot2.nsp'),
                Path(dest_ams, 'contents/0100000000000008/exefs.nsp'),
            ),
            'eclct.stub': (
                Path(self._source_directory, 'stratosphere/eclct.stub/eclct.stub.nsp'),
                Path(dest_ams, 'contents/0100000000000032/exefs.nsp'),
            ),
            'fatal': (
                Path(self._source_directory, 'stratosphere/fatal/fatal.nsp'),
                Path(dest_ams, 'contents/0100000000000034/exefs.nsp'),
            ),
            'creport': (
                Path(self._source_directory, 'stratosphere/creport/creport.nsp'),
                Path(dest_ams, 'contents/0100000000000036/exefs.nsp'),
            ),
            'ro': (
                Path(self._source_directory, 'stratosphere/ro/ro.nsp'),
                Path(dest_ams, 'contents/0100000000000037/exefs.nsp'),
            ),
            'jpegdec': (
                Path(self._source_directory, 'stratosphere/jpegdec/jpegdec.nsp'),
                Path(dest_ams, 'contents/010000000000003C/exefs.nsp'),
            ),
            'fusee-primary': (
                Path(self._source_directory, 'fusee/fusee-primary/fusee-primary.bin'),
                [
                    Path(install_directory, 'payloads/fusee-primary.bin'),
                    Path(dest_hekate, 'payloads/fusee-primary.bin'),
                ],
            ),
            'fusee-secondary': (
                Path(self._source_directory, 'fusee/fusee-secondary/fusee-secondary.bin'),
                [
                    Path(dest_ams, 'fusee-secondary.bin'),
                    Path(dest_sept, 'payload.bin'),
                ],
            ),
            'fusee-mtc': (
                Path(self._source_directory, 'fusee/fusee-mtc/fusee-mtc.bin'),
                Path(dest_ams, 'fusee-mtc.bin'),
            ),
            'hbl-html': (
                Path(self._source_directory, 'config_templates/hbl_html/'),
                Path(dest_ams, 'hbl_html/'),
            ),
            'bct.ini': (
                Path(self._defaults_directory, 'BCT.ini'),
                Path(dest_ams, 'config/BCT.ini'),
            ),
            'exosphere.ini': (
                Path(self._defaults_directory, 'exosphere.ini'),
                Path(dest_sd, 'exosphere.ini'),
            ),
            'override_config.ini': (
                Path(self._defaults_directory, 'override_config.ini'),
                Path(dest_ams, 'config/override_config.ini'),
            ),
            'system-settings': (
                Path(self._defaults_directory, 'system_settings.ini'),
                Path(dest_ams, 'config/system_settings.ini'),
            ),
            'sept-primary': (
                Path(self._source_directory, 'sept/sept-primary/sept-primary.bin'),
                Path(dest_sept, 'sept-primary.bin'),
            ),
            'sept-secondary_00-enc': (
                Path(self._dockerfiles_directory, 'sept-secondary_00.enc'),
                Path(dest_sept, 'sept-secondary_00.enc'),
            ),
            'sept-secondary_01-enc': (
                Path(self._dockerfiles_directory, 'sept-secondary_01.enc'),
                Path(dest_sept, 'sept-secondary_01.enc'),
            ),
            'sept-secondary_dev_00-enc': (
                Path(self._dockerfiles_directory, 'sept-secondary_dev_00.enc'),
                Path(dest_sept, 'sept-secondary_dev_00.enc'),
            ),
            'sept-secondary_dev_01-enc': (
                Path(self._dockerfiles_directory, 'sept-secondary_dev_01.enc'),
                Path(dest_sept, 'sept-secondary_dev_01.enc'),
            ),
            'boot_flags': (
                Path(settings.defaults_directory, 'boot2.flag'),
                [
                    Path(dest_ams, 'contents/0100000000000032/flags/boot2.flag'), # eclct.stub
                    Path(dest_ams, 'contents/0100000000000037/flags/boot2.flag'), # ro
                ],
            ),
            'nogc-patches': (
                Path(self._source_directory, 'config_templates/kip_patches/default_nogc/'),
                Path(dest_ams, 'kip_patches/default_nogc/'),
            ),
            'fs-patches': (
                Path(self._defaults_directory, 'sigpatches/fs_patches/'),
                Path(dest_ams, 'kip_patches/fs_patches/'),
            ),
            'logo-patches': (
                Path(self._defaults_directory, 'sigpatches/logo_patches/'),
                Path(dest_ams, 'exefs_patches/logo_patches/'),
            ),
            'es-patches': (
                Path(self._defaults_directory, 'sigpatches/es_patches/'),
                Path(dest_ams, 'exefs_patches/es_patches/'),
            ),
        }
        self._copy_components(component_dict)

    def clean(self):
        with util.change_dir(self._source_directory):
            util.clean_component(DOCKER_IMAGE_NAME, COMPONENT_COMMIT_OR_TAG)

    def _build(self):
        self._build_prepare()
        self._build_docker()
        
    def _build_docker(self):
        with util.change_dir(self._dockerfiles_directory):
            util.dock_worker(DOCKER_IMAGE_NAME)

    def _build_prepare(self):
        with util.change_dir(self._source_directory):
            build_commands = [
                'git fetch',
                'git checkout {b} && git pull && git reset --hard {c}'.format(c=COMPONENT_COMMIT_OR_TAG, b=COMPONENT_BRANCH),
            ]
            util.execute_shell_commands(build_commands)


def get_component():
    return AtmosphereComponent()
