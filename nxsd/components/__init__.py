import shutil

from distutils.dir_util import copy_tree
from abc import ABC, abstractmethod


class NXSDComponent(ABC):

    def __init__(self):
        self._name = None
        self._version_string = None

    @property
    def name(self):
        return self._name

    @property
    def version_string(self):
        return self._version_string

    @abstractmethod
    def install(self, install_directory):
        """
        Build this component from source (if necessary), then install it to the
        specified directory,
        """

    @abstractmethod
    def clean(self):
        """
        Clean up built binaries for this component.
        """


    @staticmethod
    def _copy_components(component_dict):
        for component in component_dict:
            src, dest_list = component_dict[component]

            if not isinstance(dest_list, list):
                dest_list = [dest_list]

            for dest in dest_list:
                if src.is_dir():
                    copy_tree(str(src), str(dest))
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(src), str(dest))
