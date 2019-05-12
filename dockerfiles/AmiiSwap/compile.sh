#!/bin/bash
cd /developer/components/AmiiSwap/Plutonium
git checkout f66d07d
git reset --hard f66d07d

cd /developer/components/AmiiSwap

make -j5
