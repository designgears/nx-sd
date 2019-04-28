#!/bin/bash
cd /developer/components/Tinfoil88
sed -i 's/Tinfoil/Tinfoil-88/g' Makefile
make -j5
