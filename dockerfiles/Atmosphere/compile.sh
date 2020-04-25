#!/bin/bash

git apply /ams.patch

make -C /developer/components/Atmosphere -j8

git apply -R /ams.patch