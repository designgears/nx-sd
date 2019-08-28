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

def component_clean(name):
    build_commands = [
        'git clean -fdx',
        'git submodule foreach --recursive git clean -fdx',
        'git submodule foreach --recursive git reset --hard',
        'git reset --hard',
        'git submodule update --init --recursive',
        'docker inspect "{d}" > /dev/null 2>&1 && docker image rm {d} || echo "No image to delete."'.format(
            d=name),
    ]
    execute_shell_commands(build_commands)

def dock_worker(name):
    build_commands = [
        'docker inspect "{d}" > /dev/null 2>&1 && echo "Using existing image." || docker build . -t {d}:latest'.format(
                d=name),
        'docker container inspect "{d}" > /dev/null 2>&1 && docker stop {d} || echo "Container not running."'.format(d=name),
        'docker container inspect "{d}" > /dev/null 2>&1 && docker rm {d} || echo "Container not found."'.format(d=name),
        'docker run --rm -a stdout -a stderr --name {d} --mount src="{bd}",target=/developer,type=bind {d}:latest'.format(
                d=name, bd=PROJECT_PATH),
    ]
    execute_shell_commands(build_commands)

