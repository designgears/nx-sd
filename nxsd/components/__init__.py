import shutil

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
        pass

    @abstractmethod
    def clean(self):
        """
        Clean up built binaries for this component.
        """
        pass


    @staticmethod
    def _copy_components(component_dict):
        for component in component_dict:
            src, dest = component_dict[component]
            if src.is_dir():
                shutil.copytree(str(src), str(dest))
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(src), str(dest))
