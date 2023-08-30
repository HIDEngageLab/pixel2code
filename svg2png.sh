#!/bin/bash

# Copyright (c) 2023, Roman Koch, koch.roman@gmail.com
# All rights reserved
#
# SPDX-License-Identifier: MIT

current_dir=$(pwd)

# --------------------------------------------------------
# parameter area ;)
# --------------------------------------------------------
src="resources/vector"
trg="resources/png"
icon_sizes=(8 16 24 32)
# --------------------------------------------------------

if ! command -v convert &>/dev/null; then
    echo "convert could not be found; try to install image magic packages"
    exit
fi

[ ! -d "$trg" ] && mkdir -p "$trg"

pushd $src

for i in $(ls *.svg); do
    for icon_size in ${icon_sizes[@]}; do
        pix_file=$(basename $i .svg)_${icon_size}.png
        echo $i to $pix_file

        convert -monochrome -threshold 90% -negate -transparent black -resize x$icon_size -transparent white -depth 1 -colors 2 -format PNG1 $i $current_dir/$trg/$pix_file
    done
done

popd
