import shutil

from abc import ABC, abstractmethod


class NXSDPackage(ABC):

    def __init__(self):
        self.config = None

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def pack(self):
        pass

    @staticmethod
    def _copy_package_components(component_dict):
        for component in component_dict:
            src, dest = component_dict[component]
            if src.is_dir():
                shutil.copytree(str(src), str(dest))
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(src), str(dest))
