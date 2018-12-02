import logging
import shutil

from pathlib import Path


_logger = logging.getLogger('nxsd')


class NXSDPackage(object):

    def __init__(self, name, build_directory, output_filename):
        self.name = name
        self.build_directory = build_directory
        self.output_filename = output_filename

        self.components = []

    def build_components(self):
        self._cleanup_build_directory()

        for component_module in self.components:
            component = component_module.get_component()
            _logger.info('Building {name} {version}...'.format(
                name=component.name, version=component.version_string))
            component.install(self.build_directory)

        output_path = Path(self.output_filename)
        shutil.make_archive(output_path.stem, 'zip',
                            root_dir=self.build_directory)

    def _cleanup_build_directory(self):
        build_dir = Path(self.build_directory)
        if build_dir.exists():
            shutil.rmtree(build_dir)
