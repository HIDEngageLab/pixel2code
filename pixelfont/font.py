#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

# Copyright (c) 2023, Roman Koch, koch.roman@gmail.com
# All rights reserved
#
# SPDX-License-Identifier: MIT

from generator import convert_font, generate_c_header, generate_c_array


class Font:
    def __init__(self) -> None:
        self.__name = None
        self.__width = None
        self.__height = None

        self.__is_loaded = False
        self.__is_changed = False

        self.__hash = None
        self.clean()
        self.__index = 0

        self.__rows = True

    @property
    def name(self):
        return self.__name

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def symbol(self):
        return chr(self.__index)

    @property
    def data(self):
        return self.__hash[chr(self.__index)]

    @data.setter
    def data(self, value):
        self.__is_changed = True
        self.__hash[chr(self.__index)] = value

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, value):
        self.__index = value

    def clean(self):
        self.__is_loaded = False
        self.__is_changed = False

        self.__index = 0
        self.__hash = dict()
        for i in range(0, 128):
            self.__hash[chr(i)] = None

    def prev(self):
        if self.__index > 0:
            self.__index -= 1
        else:
            self.__index = 127

    def next(self):
        if self.__index < 127:
            self.__index += 1
        else:
            self.__index = 0

    @property
    def rows(self):
        if self.__rows is True:
            return True
        return False

    def direction_rows(self):
        self.__rows = True

    def direction_cols(self):
        self.__rows = False

    def load_file(self, file_name):
        import json
        import sys

        with open(file_name, 'r') as font_json:
            self.clean()

            data = json.load(font_json)
            if data is not None:
                if 'name' in data:
                    self.__name = data['name']
                if 'width' in data:
                    self.__width = data['width']
                if 'height' in data:
                    self.__height = data['height']

                if 'font' in data:
                    for item in data['font']:
                        self.__hash[item['symbol']] = item['data']

            self.__is_loaded = True

    def store_file(self, file_name):
        import json
        import sys

        data = dict()

        if self.__name is not None:
            data['name'] = self.__name
        if self.__width is not None:
            data['width'] = self.__width
        if self.__height is not None:
            data['height'] = self.__height

        data['font'] = list()
        for key, value in self.__hash.items():
            if value is not None:
                font_item = {
                    'data': value,
                    'symbol': key
                }
                data['font'].append(font_item)

        with open(file_name, 'w') as font_json:
            content = json.dumps(data, indent=4)
            font_json.write(content)

            self.__is_changed = False

    def generate_code(self, target_path):
        if self.__width is None or self.__height is None:
            return

        import os

        target_path = os.path.abspath(target_path)
        if not os.path.exists(target_path):
            os.mkdir(target_path)

        font_name = self.__name if self.__name is not None else 'bla'
        font_file_name = os.path.join(target_path,
                                      f"font_{font_name}.txt")

        with open(font_file_name, "w") as font_map_file:
            data = list()
            for key, value in self.__hash.items():
                if value is not None:
                    font_item = {
                        'data': value,
                        'symbol': key
                    }
                    data.append(font_item)

            font_description = convert_font(data,
                                            self.__width,
                                            self.__height,
                                            self.__rows,
                                            font_map_file=font_map_file)

            header_name = os.path.join(target_path,
                                       f"font_{font_name}.h")
            with open(header_name, "w") as font_file:
                generate_c_header(font_description,
                                  header_file=font_file,
                                  object_name=font_name,
                                  prefix='font')

            source_name = os.path.join(target_path,
                                       f"font_{font_name}.c")
            with open(source_name, "w") as font_file:
                generate_c_array(font_description,
                                 font_file=font_file,
                                 font_name=font_name,
                                 prefix='font')
