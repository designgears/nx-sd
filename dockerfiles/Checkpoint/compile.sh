#!/bin/bash

# apply patch
git apply /contents.patch

make -C /developer/components/Checkpoint -j8 switch

# remove patch
git apply -R /contents.patch
