#!/bin/bash

cd /developer/components/sys-clk-Overlay/libs/libtesla

make -j8

cd /developer/components/sys-clk-Overlay/libs/SimpleIniParser

make -j8

cd /developer/components/sys-clk-Overlay

make -j8
