#!/bin/bash

cd /developer/components/Goldleaf/Plutonium

git reset --hard 343623a

cd /developer/components/Goldleaf/Goldleaf

make -j8
