#!/bin/bash

cd /developer/components/ldn_mitm/libstratosphere

sed -i 's/\/atmosphere\/titles\//\/atmosphere\/contents\//' /developer/components/ldn_mitm/libstratosphere/source/cfg/cfg_flags.cpp
sed -i 's/\/atmosphere\/titles\//\/atmosphere\/contents\//' /developer/components/ldn_mitm/libstratosphere/source/cfg/cfg_override.cpp
sed -i 's/\/atmosphere\/loader.ini/\/atmosphere\/config\/override_config.ini/' /developer/components/ldn_mitm/libstratosphere/source/cfg/cfg_override.cpp

make -C /developer/components/ldn_mitm -j8
