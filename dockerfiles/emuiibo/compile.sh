#!/bin/bash

cd /developer/components/emuiibo/libstratosphere

# apply patch
git apply /contents.patch

make -C /developer/components/emuiibo -j8

# remove patch
git apply -R /contents.patch
