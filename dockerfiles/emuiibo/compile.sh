#!/bin/bash

cd /developer/components/emuiibo

make -j8

cd /developer/components/emuiibo/libtesla

make -j8

cd /developer/components/emuiibo/overlay

make -j8
