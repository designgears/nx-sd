#!/bin/bash

# update libstratosphere to latest master
cd /developer/components/emuiibo/libstratosphere
git clean -fdx

# Update Runtime Firmware Version stuff for 8.0
git reset --hard 163d925

cd /
make -j5
