#!/bin/bash
cd /developer/components/Goldleaf/libnx-Goldleaf
git reset --hard
git checkout master
git reset --hard a6989b2

cp /default_icon.jpg ./nx/default_icon.jpg

cd /

make -j5
