import logging
import shutil
import subprocess

from abc import ABC, abstractmethod


_logger = logging.getLogger('nxsd')

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

    def _log_stream_output(self, level, stream):
        for line in stream:
            _logger.log(level, '%s', line.decode('utf-8').rstrip())

    def _execute_shell_commands(self, command_list):
        for command in command_list:
            process = subprocess.Popen(command.split(),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            with process.stdout:
                self._log_stream_output(logging.DEBUG, process.stdout)
            with process.stderr:
                self._log_stream_output(logging.ERROR, process.stderr)

            process.wait()

    @staticmethod
    def _copy_components(component_dict):
        for component in component_dict:
            src, dest = component_dict[component]
            if src.is_dir():
                shutil.copytree(str(src), str(dest))
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(src), str(dest))
