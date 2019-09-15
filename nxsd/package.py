import nxsd
import shutil
import logging
import git
import os
import glob

from nxsd import util
from pathlib import Path


class NXSDPackage():

    def __init__(self, name, build_type, build_directory, output_filename):
        self.name = name
        self.build_type = build_type
        self.build_directory = build_directory
        self.output_filename = output_filename

        self.components = []

    def build_components(self):
        self._cleanup_build_directory()
        
        all_builds_successful = True

        for component_module in self.components:
            component = component_module.get_component()
            nxsd.logger.info('Building {name} {version}...'.format(
                name=component.name, version=component.version_string))
            component.install(self.build_directory)

        if all_builds_successful:
            output_path = Path(self.output_filename)
            shutil.make_archive(str(output_path.with_suffix(''))+self._get_repo_sha(component.name), 'zip',
                root_dir=self.build_directory)

        return all_builds_successful

    def clean(self):
        self._cleanup_build_directory()

        for component_module in self.components:
            component = component_module.get_component()
            nxsd.logger.info('Cleaning {name} {version}...'.format(
                name=component.name, version=component.version_string))
            component.clean()

        util.delete_if_exists(Path(self.output_filename))

    def _cleanup_build_directory(self):
        [os.remove(x) for x in glob.glob("out/"+self.name+"*.zip")]
        build_dir = Path(self.build_directory)
        if build_dir.exists():
            shutil.rmtree(build_dir, ignore_errors=True)

    def _get_repo_sha(self, name):
        sha = ''
        try:
            if self.build_type == 'package':
                repo = git.Repo(search_parent_directories=True)
            else:
                repo = git.Repo(search_parent_directories=False, path='components/'+name)
            sha = '-'+repo.head.object.hexsha[:7]
        except:
            nxsd.logger.log(logging.DEBUG, '%s', 'Git repo not found, skipping SHA.')
        
        return sha