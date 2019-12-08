#!/bin/bash

cd /developer/components/ldn_mitm/libstratosphere

# apply patch
git apply /contents.patch

make -C /developer/components/ldn_mitm -j8

# remove patch
git apply -R /contents.patch