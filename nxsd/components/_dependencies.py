import nxsd
import os

from nxsd import util
from pathlib import Path

class NXSDDependency(object):
    
    def __init__(self, name, paths):
        self.name = name
        self.paths = paths

dkp_root = os.environ.get('DEVKITPRO', default='/opt/devkitpro/')

DEVKITPRO = NXSDDependency(
    name='devkitPro',
    paths=[Path(dkp_root)]
)
DEVKITA64 = NXSDDependency(
    name='devkitA64',
    paths=[Path(dkp_root, 'devkitA64/lib/libaarch64-none-elf-sim.a')]
)
DEVKITARM = NXSDDependency(
    name='devkitARM',
    paths=[
        Path(dkp_root, 'devkitARM/lib/libarm-none-eabi-sim.a'),
        Path(dkp_root, 'devkitARM/base_rules'),
    ]
)
GENERAL_TOOLS = NXSDDependency(
    name='general-tools',
    paths=[
        Path(dkp_root, 'tools/bin/bin2s'),
        Path(dkp_root, 'tools/bin/bmp2bin'),
        Path(dkp_root, 'tools/bin/padbin'),
        Path(dkp_root, 'tools/bin/raw2c'),
    ]
)
LIBNX = NXSDDependency(
    name='libnx',
    paths=[Path(dkp_root, 'libnx/lib/libnx.a')]
)
SWITCH_CURL = NXSDDependency(
    name='switch-curl',
    paths=[Path(dkp_root, 'portlibs/switch/lib/libcurl.a')]
)
SWITCH_FREETYPE = NXSDDependency(
    name='switch-freetype',
    paths=[Path(dkp_root, 'portlibs/switch/lib/libfreetype.a')]
)
SWITCH_LIBCONFIG = NXSDDependency(
    name='switch-libconfig',
    paths=[
        Path(dkp_root, 'portlibs/switch/lib/libconfig.a'),
        Path(dkp_root, 'portlibs/switch/lib/libconfig++.a'),
    ]
)
SWITCH_LIBJPEG_TURBO = NXSDDependency(
    name='switch-libjpeg-turbo',
    paths=[
        Path(dkp_root, 'portlibs/switch/lib/libjpeg.a'),
        Path(dkp_root, 'portlibs/switch/lib/libturbojpeg.a'),
    ]
)
SWITCH_SDL2_GFX = NXSDDependency(
    name='switch-sdl2_gfx',
    paths=[Path(dkp_root, 'portlibs/switch/lib/libSDL2_gfx.a')]
)
SWITCH_SDL2_IMAGE = NXSDDependency(
    name='switch-sdl2_image',
    paths=[Path(dkp_root, 'portlibs/switch/lib/libSDL2_image.a')]
)
SWITCH_SDL2_TTF = NXSDDependency(
    name='switch-sdl2_ttf',
    paths=[Path(dkp_root, 'portlibs/switch/lib/libSDL2_ttf.a')]
)
SWITCH_TOOLS = NXSDDependency(
    name='switch-tools',
    paths=[
        Path(dkp_root, 'tools/bin/build_pfs0'),
        Path(dkp_root, 'tools/bin/build_romfs'),
        Path(dkp_root, 'tools/bin/elf2kip'),
        Path(dkp_root, 'tools/bin/elf2nro'),
        Path(dkp_root, 'tools/bin/elf2nso'),
        Path(dkp_root, 'tools/bin/nacptool'),
        Path(dkp_root, 'tools/bin/npdmtool'),
        Path(dkp_root, 'tools/bin/nxlink'),
    ]
)


def check_dependency(dependency):
    for path in dependency.paths:
        nxsd.logger.debug('Checking for dependency {} at {}'.format(dependency.name, path))
        if not os.path.exists(path):
            nxsd.logger.error('Dependency {} not found.'.format(dependency.name))
            return False

    return True

def check_dependencies(dependency_list):
    for dependency in dependency_list:
        if not check_dependency(dependency):
            return False

    return True

def check_core_dependencies():
    if not util.check_environment_variable('DEVKITPRO'):
        return False

    core_dependencies = [
        DEVKITPRO, 
        DEVKITA64, 
        GENERAL_TOOLS, 
        LIBNX, 
        SWITCH_TOOLS
    ]

    if not check_dependencies(core_dependencies):
        return False

    return True
