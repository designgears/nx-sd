#!/bin/bash
cd /developer/components/Atmosphere
git checkout master
git pull

cd /developer/components/Atmosphere/exosphere
make -j5

cd /developer/components/Atmosphere/sept
make -j5

cd /developer/components/ReiNX/NX_Sysmodules
git checkout a06c3ba
git reset --hard a06c3ba

cd /developer/components/ReiNX

sed -i 's/@$(MAKE) ver_maj=$(ver_major) ver_min=$(ver_minor) -C $(dir_sysmod)/@$(MAKE) -C $(dir_sysmod)/g' Makefile

make -j5
