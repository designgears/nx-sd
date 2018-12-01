import shutil

from pathlib import Path


class NXSDBuilder(object):

    def __init__(self, config):
        self._packages = []
        self.config = config

    def add_package(self, package):
        self._packages.append(package)

    def build_packages(self):
        self._cleanup_build_folder()

        for package in self._packages:
            package.config = self.config
            package.build()
            package.pack()

        output_path = Path(self.config.output_path)
        shutil.make_archive(output_path.stem, 'zip', root_dir=self.config.build_dir)

    def _cleanup_build_folder(self):
        build_dir = Path(self.config.build_dir)
        if build_dir.exists():
            shutil.rmtree(build_dir)



class NXSDBuildConfig(object):

    def __init__(self, components_dir, build_dir, defaults_dir, output_path, logger=None):
        self.components_dir = components_dir
        self.build_dir = build_dir
        self.defaults_dir = defaults_dir
        self.output_path = output_path
        self.logger = logging.getLogger() if logger is None else logger
