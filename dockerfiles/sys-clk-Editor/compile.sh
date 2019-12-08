#!/bin/bash

# apply patch
git apply /contents.patch

make -C /developer/components/sys-clk-Editor -j8

# remove patch
git apply -R /contents.patch
