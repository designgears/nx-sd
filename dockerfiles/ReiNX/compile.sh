#!/bin/bash
cd /developer/components/Atmosphere
git checkout 0.8.10

cd /developer/components/Atmosphere/exosphere
make -j5

cd /developer/components/Atmosphere/sept
make -j5

cd /developer/components/ReiNX

make -j5
