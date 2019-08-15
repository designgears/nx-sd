import contextlib
import logging
import nxsd
import os
from subprocess import Popen, PIPE, STDOUT

from contextlib import contextmanager
from pathlib import Path

PROJECT_PATH = Path().absolute()

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


def dock_worker(name):
    build_commands = [
        'docker build . -t {d}:latest'.format(d=name),
        'docker stop {d}'.format(d=name),
        'docker rm {d}'.format(d=name),
        'docker run --rm -a stdout -a stderr --name {d} --mount src="{bd}",target=/developer,type=bind {d}:latest'.format(
            d=name, bd=PROJECT_PATH),
    ]
    execute_shell_commands(build_commands)

