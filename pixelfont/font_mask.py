#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

# Copyright (c) 2023, Roman Koch, koch.roman@gmail.com
# All rights reserved
#
# SPDX-License-Identifier: MIT

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path


_script = sys.argv[0]
_location = os.path.dirname(_script)

source_path = os.path.join(_location, 'resources/font')
target_path = os.path.join(_location, 'resources/code')


class FontMask:
    def __init__(self, top=None):
        global target_path, source_path

        top.geometry("1000x700+300+300")
        top.minsize(100, 100)
        top.maxsize(1905, 2130)
        top.resizable(1,  1)
        top.title("pixelfont")
        top.configure(highlightcolor="black")

        self.top = top

        self.draw_mode = None

        self.pixel_point_matrix = None
        self.pixel_button_matrix = None

        self.menubar = tk.Menu(top, font="TkMenuFont",
                               bg='#d9d9d9', fg='#000000')
        top.configure(menu=self.menubar)

        self.sub_menu = tk.Menu(self.menubar,
                                activebackground='beige',
                                activeforeground='black',
                                tearoff=0)
        self.menubar.add_cascade(compound='left',
                                 label='file',
                                 menu=self.sub_menu,)

        self.sub_menu.add_command(compound='left', label='load font',
                                  command=load_font_file)

        self.sub_menu.add_command(compound='left', label='store font',
                                  command=store_font_file)
        self.sub_menu.add_separator()

        self.sub_menu.add_command(compound='left', label='quit',
                                  command=lambda: self.top.quit())

        from font_instance import generate_code
        self.menubar.add_command(compound='left',
                                 label='generate',
                                 command=lambda _target_path=target_path: generate_code(_target_path))

        self.menubar.add_command(compound='left',
                                 label='about',
                                 command=about)

        self.FrameEditor = tk.Frame(self.top)
        self.FrameEditor.place(relx=0, rely=0,
                               relheight=0.95,
                               relwidth=0.65)
        self.FrameEditor.configure(relief='groove')
        self.FrameEditor.configure(borderwidth="2")
        self.FrameEditor.configure(relief="groove")

        self.ButtonPrev = tk.Button(self.FrameEditor,
                                    command=select_prev_symbol)
        self.ButtonPrev.place(relx=0, rely=0.9,
                              relheight=0.1, relwidth=0.1)
        self.ButtonPrev.configure(activebackground="beige")
        self.ButtonPrev.configure(borderwidth="2")
        self.ButtonPrev.configure(compound='left')
        self.ButtonPrev.configure(text='prev')

        self.ButtonNext = tk.Button(self.FrameEditor,
                                    command=select_next_symbol)
        self.ButtonNext.place(relx=0.9, rely=0.9,
                              relheight=0.1, relwidth=0.1)
        self.ButtonNext.configure(activebackground="beige")
        self.ButtonNext.configure(borderwidth="2")
        self.ButtonNext.configure(compound='left')
        self.ButtonNext.configure(text='next')

        self.ButtonClean = tk.Button(self.FrameEditor, command=clean_symbol)
        self.ButtonClean.place(relx=0.9, rely=0.1,
                               relheight=0.05, relwidth=0.1)
        self.ButtonClean.configure(activebackground="beige")
        self.ButtonClean.configure(borderwidth="2")
        self.ButtonClean.configure(compound='left')
        self.ButtonClean.configure(text='clean')

        self.ButtonFill = tk.Button(self.FrameEditor, command=fill_symbol)
        self.ButtonFill.place(relx=0.9, rely=0.15,
                              relheight=0.05, relwidth=0.1)
        self.ButtonFill.configure(activebackground="beige")
        self.ButtonFill.configure(borderwidth="2")
        self.ButtonFill.configure(compound='left')
        self.ButtonFill.configure(text='fill')

        self.ButtonCopy = tk.Button(self.FrameEditor, command=copy_symbol)
        self.ButtonCopy.place(relx=0.9, rely=0.2, relheight=0.05, relwidth=0.1)
        self.ButtonCopy.configure(activebackground="beige")
        self.ButtonCopy.configure(borderwidth="2")
        self.ButtonCopy.configure(compound='left')
        self.ButtonCopy.configure(text='copy')

        self.ButtonPaste = tk.Button(self.FrameEditor, command=paste_symbol)
        self.ButtonPaste.place(relx=0.9, rely=0.25,
                               relheight=0.05, relwidth=0.1)
        self.ButtonPaste.configure(activebackground="beige")
        self.ButtonPaste.configure(borderwidth="2")
        self.ButtonPaste.configure(compound='left')
        self.ButtonPaste.configure(text='paste')

        self.FrameSymbol = tk.Frame(self.FrameEditor)
        self.FrameSymbol.place(relx=0.1,
                               rely=0.1,
                               relheight=0.9,
                               relwidth=0.8)
        self.FrameSymbol.configure(relief='sunken')
        self.FrameSymbol.configure(borderwidth="2")

        self.SymbolFrame = tk.Frame(self.FrameSymbol)
        # create_pixel(8, 8)

        self.LabelSymbol = tk.Label(self.FrameEditor)
        self.LabelSymbol.place(relx=0.1, rely=0.05,
                               height=21, relwidth=0.8)
        self.LabelSymbol.configure(activebackground="#f9f9f9")
        self.LabelSymbol.configure(anchor='w')
        self.LabelSymbol.configure(compound='left')

        self.SymbolLabelFrame = self.LabelSymbol

        self.LabelSymbol.configure(text='Symbol')

        self.FrameAttributes = tk.Frame(self.top)
        self.FrameAttributes.place(relx=0.65, rely=0,
                                   relheight=0.95, relwidth=0.35)
        self.FrameAttributes.configure(relief='groove')
        self.FrameAttributes.configure(borderwidth="2")
        self.FrameAttributes.configure(relief="groove")

        self.LabelName = tk.Label(self.FrameAttributes)
        self.LabelName.place(relx=0.03, rely=0.02,
                             height=31, width=87)
        self.LabelName.configure(activebackground="#f9f9f9")
        self.LabelName.configure(anchor='w')
        self.LabelName.configure(compound='left')
        self.LabelName.configure(text='Name')

        self.EntryNameText = tk.StringVar()
        self.EntryName = tk.Entry(self.FrameAttributes,
                                  textvariable=self.EntryNameText)
        self.EntryName.place(relx=0.35, rely=0.02,
                             height=23, relwidth=0.6)
        self.EntryName.configure(background="white")
        self.EntryName.configure(font="TkFixedFont")
        self.EntryName.configure(selectbackground="#c4c4c4")
        self.EntryName.configure(state='disabled')

        self.LabelWidth = tk.Label(self.FrameAttributes)
        self.LabelWidth.place(relx=0.03, rely=0.08,
                              height=31, width=87)
        self.LabelWidth.configure(activebackground="#f9f9f9")
        self.LabelWidth.configure(anchor='w')
        self.LabelWidth.configure(compound='left')
        self.LabelWidth.configure(text='Width pix')

        self.EntryWidthText = tk.StringVar()
        self.EntryWidth = tk.Entry(self.FrameAttributes,
                                   textvariable=self.EntryWidthText)
        self.EntryWidth.place(relx=0.35, rely=0.08,
                              height=23, relwidth=0.6)
        self.EntryWidth.configure(background="white")
        self.EntryWidth.configure(font="TkFixedFont")
        self.EntryWidth.configure(justify='right')
        self.EntryWidth.configure(selectbackground="#c4c4c4")
        self.EntryWidth.configure(state='disabled')

        self.LabelHeight = tk.Label(self.FrameAttributes)
        self.LabelHeight.place(relx=0.03, rely=0.14,
                               height=31, width=87)
        self.LabelHeight.configure(activebackground="#f9f9f9")
        self.LabelHeight.configure(anchor='w')
        self.LabelHeight.configure(compound='left')
        self.LabelHeight.configure(text='Height pix')

        self.EntryHeightText = tk.StringVar()
        self.EntryHeight = tk.Entry(self.FrameAttributes,
                                    textvariable=self.EntryHeightText)
        self.EntryHeight.place(relx=0.35, rely=0.14,
                               height=23, relwidth=0.6)
        self.EntryHeight.configure(background="white")
        self.EntryHeight.configure(font="TkFixedFont")
        self.EntryHeight.configure(justify='right')
        self.EntryHeight.configure(selectbackground="#c4c4c4")
        self.EntryHeight.configure(state='disabled')

        self.LabelDescription = tk.Label(self.FrameAttributes)
        self.LabelDescription.place(relx=0.03, rely=0.20,
                                    height=31, width=87)
        self.LabelDescription.configure(activebackground="#f9f9f9")
        self.LabelDescription.configure(anchor='w')
        self.LabelDescription.configure(compound='left')
        self.LabelDescription.configure(text='Description')
        self.TextDescription = tk.Text(self.FrameAttributes)
        self.TextDescription.place(relx=0.35, rely=0.20,
                                   height=46, relwidth=0.6)
        self.TextDescription.configure(background="white")
        self.TextDescription.configure(font="TkTextFont")
        self.TextDescription.configure(selectbackground="#c4c4c4")
        self.TextDescription.configure(wrap="word")

        self.ButtonSourcePath = tk.Button(self.FrameAttributes,
                                          command=set_source_path)
        self.ButtonSourcePath.place(relx=0.03, rely=0.36,
                                    height=31, width=87)
        self.ButtonSourcePath.configure(activebackground="#f9f9f9")
        self.ButtonSourcePath.configure(borderwidth="2")
        self.ButtonSourcePath.configure(compound='left')
        self.ButtonSourcePath.configure(text='source dir')

        self.TextSourcePath = tk.Text(self.FrameAttributes)
        self.TextSourcePath.place(relx=0.35, rely=0.36,
                                  height=69, relwidth=0.6)
        self.TextSourcePath.insert(END, source_path)
        self.TextSourcePath.configure(background="white")
        self.TextSourcePath.configure(font="TkTextFont")
        self.TextSourcePath.configure(selectbackground="#c4c4c4")
        self.TextSourcePath.configure(wrap="word")
        self.TextSourcePath.config(state='disabled')

        self.ButtonTargetPath = tk.Button(self.FrameAttributes,
                                          command=set_target_path)
        self.ButtonTargetPath.place(relx=0.03, rely=0.5,
                                    height=31, width=87)
        self.ButtonTargetPath.configure(activebackground="#f9f9f9")
        self.ButtonTargetPath.configure(borderwidth="2")
        self.ButtonTargetPath.configure(compound='left')
        self.ButtonTargetPath.configure(text='target dir')

        self.TextTargetPath = tk.Text(self.FrameAttributes)
        self.TextTargetPath.place(relx=0.35, rely=0.5,
                                  height=69, relwidth=0.6)
        self.TextTargetPath.insert(END, target_path)
        self.TextTargetPath.configure(background="white")
        self.TextTargetPath.configure(font="TkTextFont")
        self.TextTargetPath.configure(selectbackground="#c4c4c4")
        self.TextTargetPath.configure(wrap="word")
        self.TextTargetPath.configure(state='disabled')

        self.PixelDirection = tk.IntVar()
        self.PixelDirection.set(1)
        self.DirectionRadioRows = tk.Radiobutton(self.FrameAttributes, text='rows',
                                                 variable=self.PixelDirection,
                                                 command=select_direction_rows,
                                                 value=1)
        self.DirectionRadioCols = tk.Radiobutton(self.FrameAttributes, text='cols',
                                                 variable=self.PixelDirection,
                                                 command=select_direction_cols,
                                                 value=2)
        self.DirectionRadioRows.place(relx=0.1, rely=0.65,
                                      height=25, relwidth=0.35)
        self.DirectionRadioCols.place(relx=0.55, rely=0.65,
                                      height=25, relwidth=0.35)

        self.FrameStatus = tk.Frame(self.top)
        self.FrameStatus.place(relx=0, rely=0.95,
                               relheight=0.05, relwidth=1.0)
        self.FrameStatus.configure(relief='sunken')
        self.FrameStatus.configure(borderwidth="2")
        self.FrameStatus.configure(relief="sunken")

        self.FontFrame = tk.Frame(self.FrameAttributes)
        self.ui_disable()
        self.__create_font()

    def ui_disable(self):
        self.ButtonNext.configure(state='disabled')
        self.ButtonPrev.configure(state='disabled')
        self.ButtonClean.configure(state='disabled')
        self.ButtonFill.configure(state='disabled')
        self.ButtonCopy.configure(state='disabled')
        self.ButtonPaste.configure(state='disabled')

        self.menubar.entryconfig("generate", state='disable')

    def ui_enable(self):
        self.ButtonNext.configure(state='normal')
        self.ButtonPrev.configure(state='normal')
        self.ButtonClean.configure(state='normal')
        self.ButtonFill.configure(state='normal')
        self.ButtonCopy.configure(state='normal')
        self.ButtonPaste.configure(state='normal')

        self.menubar.entryconfig("generate", state='normal')

        self.top.bind('<Any-KeyPress-Control_L>',
                      lambda e: set_draw_mode('erase'))
        self.top.bind('<Any-KeyRelease-Control_L>',
                      lambda e: set_draw_mode(None))
        self.top.bind('<Any-KeyPress-Shift_L>',
                      lambda e: set_draw_mode('draw'))
        self.top.bind('<Any-KeyRelease-Shift_L>',
                      lambda e: set_draw_mode(None))
        self.top.bind('<Any-KeyPress-Alt_L>',
                      lambda e: set_draw_mode('invert'))
        self.top.bind('<Any-KeyRelease-Alt_L>',
                      lambda e: set_draw_mode(None))

    def __create_font(self):
        rel_symbol_width = 1/16
        rel_symbol_height = 1/8

        self.FontFrame.place(relx=0,
                             rely=0.7,
                             relheight=0.3,
                             relwidth=1)
        self.FontFrame.configure(relief='sunken')
        self.FontFrame.configure(borderwidth="2")

        for dy in range(0, 8):
            for dx in range(0, 16):
                ButtonPixel = tk.Button(self.FontFrame,
                                        command=lambda idx=dy * 16 + dx: which_font_button(idx))
                ButtonPixel.place(relx=dx * rel_symbol_width,
                                  rely=dy * rel_symbol_height,
                                  relheight=rel_symbol_height,
                                  relwidth=rel_symbol_width)
                ButtonPixel.configure(activebackground="lightgray")
                ButtonPixel.configure(background="white")
                ButtonPixel.configure(borderwidth="0")
                ButtonPixel.configure(compound='left')
                ButtonPixel.configure(text=chr(dy * 16 + dx))


def set_draw_mode(mode):
    global _font_mask
    _font_mask.draw_mode = mode


def set_source_path():
    global source_path
    from tkinter import filedialog as fd
    tmp = fd.askdirectory(initialdir=source_path)
    if tmp is not None:
        if len(tmp) > 0:
            source_path = tmp


def set_target_path():
    global target_path
    from tkinter import filedialog as fd
    tmp = fd.askdirectory(initialdir=target_path)
    if tmp is not None:
        if len(tmp) > 0:
            target_path = tmp


def select_prev_symbol():
    from font_instance import set_prev_symbol
    set_prev_symbol()
    update_symbol()


def select_next_symbol():
    from font_instance import set_next_symbol
    set_next_symbol()
    update_symbol()


def select_direction_rows():
    from font_instance import set_direction_rows
    set_direction_rows()
    update_symbol()


def select_direction_cols():
    from font_instance import set_direction_cols
    set_direction_cols()
    update_symbol()


def update_symbol():
    global _font_mask

    from font_instance import get_symbol
    current_symbol = get_symbol()
    if current_symbol is None:
        return

    if current_symbol.isprintable():
        character_value = f'[{current_symbol:^1s}]'
    else:
        character_value = '???'
    text_line = f'Symbol {character_value} {ord(current_symbol):2d} {ord(current_symbol):#02x}'
    _font_mask.SymbolLabelFrame.configure(text=text_line)

    from font_instance import get_data
    _font_mask.pixel_point_matrix = get_data()
    if _font_mask.pixel_point_matrix is None:
        from font_instance import get_dimension
        w, h = get_dimension()
        if w is not None and h is not None:
            for row in range(0, h):
                for col in range(0, w):
                    _font_mask.pixel_button_matrix[row][col].configure(
                        background="white")
                    _font_mask.pixel_button_matrix[row][col].configure(
                        activebackground="lightgray")
    else:
        for row in range(0, _font_mask.pixel_point_matrix.shape[0]):
            for col in range(0, _font_mask.pixel_point_matrix.shape[1]):
                if _font_mask.pixel_point_matrix[row][col]:
                    _font_mask.pixel_button_matrix[row][col].configure(
                        background="black")
                    _font_mask.pixel_button_matrix[row][col].configure(
                        activebackground="darkgray")
                else:
                    _font_mask.pixel_button_matrix[row][col].configure(
                        background="white")
                    _font_mask.pixel_button_matrix[row][col].configure(
                        activebackground="lightgray")


def clean_symbol():
    from font_instance import clean_data
    clean_data()
    update_symbol()


def fill_symbol():
    from font_instance import fill_data
    fill_data()
    update_symbol()


def copy_symbol():
    from font_instance import copy_data
    copy_data()


def paste_symbol():
    from font_instance import paste_data
    paste_data()
    update_symbol()


def which_pixel_enter(row, col):
    global _font_mask

    if _font_mask.draw_mode is not None:
        if _font_mask.draw_mode == 'draw':
            _font_mask.pixel_point_matrix[row][col] = 1.0
            _font_mask.pixel_button_matrix[row][col].configure(
                background="black")
            _font_mask.pixel_button_matrix[row][col].configure(
                activebackground="darkgray")
        elif _font_mask.draw_mode == 'erase':
            _font_mask.pixel_point_matrix[row][col] = 0.0
            _font_mask.pixel_button_matrix[row][col].configure(
                background="white")
            _font_mask.pixel_button_matrix[row][col].configure(
                activebackground="lightgray")
        elif _font_mask.draw_mode == 'invert':
            which_pixel_button(row, col)

        from font_instance import set_data
        set_data(_font_mask.pixel_point_matrix)


def which_pixel_leave(row, col):
    global _font_mask
    pass


def which_pixel_button(row, col):
    global _font_mask

    if _font_mask.pixel_point_matrix[row][col]:
        _font_mask.pixel_point_matrix[row][col] = 0.0
        _font_mask.pixel_button_matrix[row][col].configure(background="white")
        _font_mask.pixel_button_matrix[row][col].configure(
            activebackground="lightgray")
    else:
        _font_mask.pixel_point_matrix[row][col] = 1.0
        _font_mask.pixel_button_matrix[row][col].configure(background="black")
        _font_mask.pixel_button_matrix[row][col].configure(
            activebackground="darkgray")

    from font_instance import set_data
    set_data(_font_mask.pixel_point_matrix)


def which_font_button(index):
    from font_instance import set_index
    set_index(index)
    update_symbol()


def create_pixel(symbol_width, symbol_height):
    global _font_mask

    for widgets in _font_mask.SymbolFrame.winfo_children():
        widgets.destroy()

    _font_mask.pixel_point_matrix = None
    _font_mask.pixel_button_matrix = None

    rel_symbol_width = 1 / symbol_width
    rel_symbol_height = 1 / symbol_height

    if rel_symbol_width < rel_symbol_height:
        rel_symbol_size = rel_symbol_width
    else:
        rel_symbol_size = rel_symbol_height

    offset_x = (rel_symbol_width - rel_symbol_size) * symbol_width / 2
    offset_y = (rel_symbol_height - rel_symbol_size) * symbol_height / 2

    _font_mask.SymbolFrame.place(relx=offset_x,
                                 rely=offset_y,
                                 relheight=symbol_height * rel_symbol_size,
                                 relwidth=symbol_width * rel_symbol_size)
    _font_mask.SymbolFrame.configure(relief='sunken')
    _font_mask.SymbolFrame.configure(borderwidth="2")

    _font_mask.pixel_button_matrix = list()
    for dy in range(0, symbol_height):
        _font_mask.pixel_button_matrix.append(list())

        for dx in range(0, symbol_width):
            ButtonPixel = tk.Button(_font_mask.SymbolFrame,
                                    command=lambda r=dy, c=dx: which_pixel_button(r, c))

            _font_mask.pixel_button_matrix[dy].append(ButtonPixel)

            ButtonPixel.place(relx=dx * rel_symbol_width,
                              rely=dy * rel_symbol_height,
                              relheight=rel_symbol_height,
                              relwidth=rel_symbol_width)
            ButtonPixel.configure(activebackground="lightgray")
            ButtonPixel.configure(background="white")
            ButtonPixel.configure(borderwidth="0")
            ButtonPixel.configure(compound='left')

            ButtonPixel.bind('<Enter>',
                             lambda e, r=dy, c=dx: which_pixel_enter(r, c))
            ButtonPixel.bind('<Leave>',
                             lambda e, r=dy, c=dx: which_pixel_leave(r, c))


def load_font_file():
    global _font_mask

    from font_instance import load_font_file, get_symbol_width, get_symbol_height

    load_font_file()

    width = get_symbol_width()
    height = get_symbol_height()
    create_pixel(width, height)

    update_symbol()
    _font_mask.ui_enable()


def store_font_file():
    from font_instance import store_font_file
    store_font_file()


def set_font_name(font_name):
    global _font_mask
    _font_mask.EntryNameText.set(font_name)


def set_font_dimension(width, height):
    global _font_mask
    _font_mask.EntryWidthText.set(width)
    _font_mask.EntryHeightText.set(height)


def about():
    global root
    message_text = """pixelfont
simple font editor for pixel matrix display fonts

Copyright (C) 2023
Roman Koch
koch.roman@gmail.com

All rights reserved
"""
    from tkinter import messagebox
    messagebox.showinfo(title="about", message=message_text)


def main(*args):
    global target_path, source_path

    import sys
    try:
        source_path = sys.argv[1]
        target_path = sys.argv[2]
    except Exception as message:
        print('wrong path parameter', message)
        source_path = 'resources/font'
        target_path = 'resources/code'

    global root
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', root.destroy)
    global _font_mask
    _font_mask = FontMask(root)
    root.mainloop()
