#!/bin/bash

# remove hardcoded directory
sed -i 's/f:/out/g' /developer/components/emuiibo/Makefile

# update libstratosphere
cd /developer/components/emuiibo/libstratosphere
git reset --hard 163d925 # Update Runtime Firmware Version stuff for 8.0

# create build directories
mkdir -p /developer/components/emuiibo/out/atmosphere/titles/0100000000000352/

cd /
make -j8
