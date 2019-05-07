#!/bin/bash
cd /developer/components/Atmosphere/exosphere
make -j5

cd /developer/components/Atmosphere/sept
make -j5

cd /developer/components/NX_Sysmodules
make -j5

cd /developer/components/ReiNX

sed -i 's/all: sysmod reinx/all: reinx/g' Makefile

make -j5

sed -i 's/all: reinx/all: sysmod reinx/g' Makefile
