#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

# Copyright (c) 2023, Roman Koch, koch.roman@gmail.com
# All rights reserved
#
# SPDX-License-Identifier: MIT

from font import Font


__font_content = Font()

symbol_buffer = None


def get_font_name():
    return __font_content.name


def get_symbol_width():
    return __font_content.width


def get_symbol_height():
    return __font_content.height


def set_prev_symbol():
    __font_content.prev()


def set_next_symbol():
    __font_content.next()


def set_direction_rows():
    __font_content.direction_rows()


def set_direction_cols():
    __font_content.direction_cols()


def get_index():
    return __font_content.index


def set_index(value):
    __font_content.index = value


def get_symbol():
    return __font_content.symbol


def get_dimension():
    symbol_width = __font_content.width
    symbol_height = __font_content.height
    return (symbol_width, symbol_height)


def get_data():
    current_data = __font_content.data
    symbol_width = __font_content.width
    symbol_height = __font_content.height

    if current_data is not None:
        from matrix import rows2matrix, cols2matrix
        if __font_content.rows is True:
            symbol_matrix = rows2matrix(current_data,
                                        symbol_width,
                                        symbol_height)
        else:
            symbol_matrix = cols2matrix(current_data,
                                        symbol_width,
                                        symbol_height)

        return symbol_matrix

    if symbol_width is not None and symbol_height is not None:
        import numpy as np
        return np.zeros((symbol_height, symbol_width))

    return None


def set_data(symbol_data):
    if symbol_data is None:
        __font_content.data = None
    else:
        from matrix import matrix2rows, matrix2cols
        if __font_content.rows is True:
            __font_content.data = matrix2rows(symbol_data)
        else:
            __font_content.data = matrix2cols(symbol_data)


def clean_data():
    symbol_width = __font_content.width
    symbol_height = __font_content.height
    if symbol_width is not None and symbol_height is not None:
        import numpy as np
        data = np.zeros((symbol_height, symbol_width))
        set_data(data)


def fill_data():
    symbol_width = __font_content.width
    symbol_height = __font_content.height
    if symbol_width is not None and symbol_height is not None:
        import numpy as np
        data = np.ones((symbol_height, symbol_width))
        set_data(data)


def copy_data():
    symbol_width = __font_content.width
    symbol_height = __font_content.height
    if symbol_width is not None and symbol_height is not None:
        global symbol_buffer

        from matrix import rows2matrix, cols2matrix
        if __font_content.rows is True:
            symbol_buffer = rows2matrix(__font_content.data.copy(),
                                        symbol_width,
                                        symbol_height)
        else:
            symbol_buffer = cols2matrix(__font_content.data.copy(),
                                        symbol_width,
                                        symbol_height)


def paste_data():
    symbol_width = __font_content.width
    symbol_height = __font_content.height
    if symbol_width is not None and symbol_height is not None:
        global symbol_buffer
        set_data(symbol_buffer)


def load_font_file(source_path=None):
    from tkinter import filedialog as fd
    file_name = fd.askopenfilename(defaultextension='.json',
                                   initialdir=source_path)
    if file_name is not None:
        if len(file_name) > 0:
            __font_content.load_file(file_name)

            from font_mask import set_font_name, set_font_dimension
            set_font_name(__font_content.name)
            set_font_dimension(__font_content.width,
                               __font_content.height)


def store_font_file(source_path=None):
    from tkinter import filedialog as fd
    file_name = fd.asksaveasfilename(defaultextension='.json',
                                     initialdir=source_path)

    if file_name is not None:
        if len(file_name) > 0:
            __font_content.store_file(file_name)


def generate_code(target_path):
    __font_content.generate_code(target_path)

    global root
    message_text = f'generate font code for "{__font_content.name}" to\n'
    message_text += f'{target_path}\n\n'
    message_text += f'overview: font_{__font_content.name}.txt\n'
    message_text += f'code:     font_{__font_content.name}.h/c'

    from tkinter import messagebox
    messagebox.showinfo(title="generator done", message=message_text)
