#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

# Copyright (c) 2023, Roman Koch, koch.roman@gmail.com
# All rights reserved
#
# SPDX-License-Identifier: MIT

def rows2matrix(data, w, h):
    import math
    import numpy as np

    cols = math.ceil(w/8)*8
    rows = math.ceil(h/8)*8

    bytes = len(data) / rows

    symbol_matrix = np.zeros((rows, cols))

    row = 0
    byte = 0
    for value in data:

        value = int(value, 16)

        symbol_matrix[row][byte * 8 + 0] = value & 0x80 > 0
        symbol_matrix[row][byte * 8 + 1] = value & 0x40 > 0
        symbol_matrix[row][byte * 8 + 2] = value & 0x20 > 0
        symbol_matrix[row][byte * 8 + 3] = value & 0x10 > 0
        symbol_matrix[row][byte * 8 + 4] = value & 0x08 > 0
        symbol_matrix[row][byte * 8 + 5] = value & 0x04 > 0
        symbol_matrix[row][byte * 8 + 6] = value & 0x02 > 0
        symbol_matrix[row][byte * 8 + 7] = value & 0x01 > 0

        byte += 1
        if byte == bytes:
            byte = 0
            row += 1

    return symbol_matrix


def cols2matrix(data, w, h):
    import math
    import numpy as np

    cols = math.ceil(w/8)*8
    rows = math.ceil(h/8)*8

    bytes = int(len(data) / cols)

    symbol_matrix = np.zeros((rows, cols))

    col = 0
    byte = 0
    for value in data:
        value = int(value, 16)

        for row in range(0, 8):
            # row_index = (bytes - 1 - byte) * 8 + row
            # row_index = rows - 1 - (byte * 8 + row)
            row_index = byte * 8 + row
            symbol_matrix[row_index][col] = (value & (0x01 << row)) > 0

        byte += 1
        if byte == bytes:
            byte = 0
            col += 1

    return symbol_matrix


def matrix2rows(symbol_matrix):
    import math
    import numpy as np

    rows, cols = symbol_matrix.shape

    data = []
    bytes = math.ceil(cols/8)
    for row in range(0, rows):
        for byte in range(0, bytes):
            value = 0
            for index in range(0, 8):
                bit = byte * 8 + index
                if bit < cols:
                    value += (0x80 >> index) if symbol_matrix[row][bit] else 0
            data.append('0x%02X' % value)
    return data


def matrix2cols(symbol_matrix):
    import math
    import numpy as np

    rows, cols = symbol_matrix.shape

    data = []
    bytes = math.ceil(rows/8)
    for col in range(0, cols):
        for byte in range(0, bytes):
            value = 0
            for index in range(0, 8):
                bit = byte * 8 + index
                if bit < rows:
                    value += (0x01 << index) if symbol_matrix[bit][col] else 0
            data.append('0x%02X' % value)
    return data


def print_matrix(symbol_matrix, symbol_title, map_file):
    map_file.write(symbol_title)
    for row in range(0, symbol_matrix.shape[0]):
        for col in range(0, symbol_matrix.shape[1]):
            map_file.write('#' if symbol_matrix[row][col] else '.')
        map_file.write('\n')
    map_file.write('\n')
