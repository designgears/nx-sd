import contextlib
import logging
import nxsd
import os
from subprocess import Popen, PIPE, STDOUT

from contextlib import contextmanager
from pathlib import Path


@contextmanager
def change_dir(new_dir):
    prev_dir = Path.cwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(prev_dir)

def delete_if_exists(path):
    with contextlib.suppress(FileNotFoundError):
        os.remove(path)

def execute_shell_commands(command_list):
    for command in command_list:
        with Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                nxsd.logger.log(logging.DEBUG, '%s', line.rstrip())
