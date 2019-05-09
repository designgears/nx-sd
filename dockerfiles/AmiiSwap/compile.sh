#!/bin/bash
cd /developer/components/AmiiSwap/Plutonium
git checkout b17ac54
git reset --hard b17ac54

cd /developer/components/AmiiSwap

make -j5
