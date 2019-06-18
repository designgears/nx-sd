#!/bin/bash
cd /developer/components/OG-Tinfoil
sed -i 's/Tinfoil/OG-Tinfoil/g' Makefile
make -j8
sed -i 's/OG-Tinfoil/Tinfoil/g' Makefile
