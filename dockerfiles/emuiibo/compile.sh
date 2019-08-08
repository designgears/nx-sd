#!/bin/bash

# remove hardcoded directory
sed -i 's,/mnt/f,out,g' /developer/components/emuiibo/Makefile

# create build directories
mkdir -p /developer/components/emuiibo/out/atmosphere/titles/0100000000000352/

make -C /developer/components/emuiibo/libstratosphere -j8
make -C /developer/components/emuiibo -j8
