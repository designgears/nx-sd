#!/bin/bash
cd /developer/components/AmiiSwap/Plutonium
git checkout 82279ad
git reset --hard 82279ad

cd /developer/components/AmiiSwap

make -j5
