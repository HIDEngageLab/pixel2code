#!/bin/bash

# Copyright (c) 2023, Roman Koch, koch.roman@gmail.com
# All rights reserved
#
# SPDX-License-Identifier: MIT

venv_path=.venv

# --------------------------------------------------------
# parameter area ;)
# --------------------------------------------------------
src=resources/font
trg=resources/code
# --------------------------------------------------------

if [ ! -d "${venv_path}" ]; then
    echo "error: venv ${venv_path} can't be found"
    exit
fi

if [ ! -d "${src}" ]; then
    echo "error: source ${src} can't be found"
    exit
fi

[ ! -d "$trg" ] && mkdir -p "$trg"

. $venv_path/bin/activate && python3 pixelfont $src $trg

deactivate
