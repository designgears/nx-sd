import contextlib
import logging
import os
import subprocess

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
        process = subprocess.Popen(command.split(),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with process.stdout:
            log_stream_output(logging.DEBUG, process.stdout)
        with process.stderr:
            log_stream_output(logging.ERROR, process.stderr)

        process.wait()

def log_stream_output(level, stream):
    logger = logging.getLogger('nxsd')
    for line in stream:
        logger.log(level, '%s', line.decode('utf-8').rstrip())
