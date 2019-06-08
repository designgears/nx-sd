#!/bin/bash

# remove extra ||
sed -i 's/"gif", 3)) ||/"gif", 3))/g' /developer/components/NX-Shell/source/menus/menu_gallery.c

cd /developer/components/NX-Shell/

make -j5
