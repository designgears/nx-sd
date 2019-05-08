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

sed -i 's/"%s ReiNX(%s.%s)"/"%s ReiNX(%d.%d)"/g' NX_Sysmodules/rnx_mitm/source/set_mitm/setsys_firmware_version.cpp

make -j5
