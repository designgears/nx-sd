#!/bin/bash

cd /developer/components/hekate

make -j8

cp /emuMMC/emummc.kipm output/emummc.kipm
