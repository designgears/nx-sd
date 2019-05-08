#!/bin/bash
cd /developer/components/Goldleaf/libnx-Goldleaf
git checkout master
git reset --hard a6989b2

cd /

make -j5
