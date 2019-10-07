#!/bin/bash

# apply cal0 write patch
# git apply /cal0.patch

make -C /developer/components/Atmosphere -j8

# remove cal0 write patch
# git apply -R /cal0.patch
