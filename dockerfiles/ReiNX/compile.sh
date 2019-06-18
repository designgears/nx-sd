#!/bin/bash
cd /developer/components/Atmosphere

cd /developer/components/Atmosphere/exosphere
make -j8

cd /developer/components/Atmosphere/sept
make -j8

cd /developer/components/ReiNX

make -j8
