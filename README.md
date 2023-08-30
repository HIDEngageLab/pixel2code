# Tools pixel2code

Helper tools for pixel-based fonts and icons of an OLED display.

The Python tools assist in creating and customizing pixel fonts and icons for OLED displays.

PixelFont is an interactive editor designed to modify font definitions and generate compilable C code.

PixelIcon takes source images in PNG format and produces compilable C code.

# Install

The prerequisite is that you are using a Linux machine.

Please perform following three steps:

1. Clone the repository.
2. Navigate into the cloned repository directory.
3. Run the script `venv-create.sh`.

Make sure to follow these steps in the given order to create a virtual environment as intended.

# Code from PNG

The prerequisite is that you are using a Linux machine.

At first, convert your SVG-Images into monochromatic PNG-Files.
Please use the script `svg2png.sh` for this purpose.

The SVG images should be located in the `resources/vector` directory. 
If the resources are located elsewhere, please adjust the script `svg2png.sh`.

The script creates PNG images with resolutions of 8x8, 16x16, 24x24 and 32x32 pixel for each SVG file.
To generate images with different resolutions, please modify the svg2png.sh script.

The PNG images are written in the `resources/png` directory. 
If you want to store images in a different location, please adjust the script `svg2png.sh`.

Next call the script `icon.sh` to create compilable C-Code.

The generated code will be placed in the `resources/code` directory.
The target directory will be be created if not exists.
If you want to use for code different location, please modify the script `icon.sh`.

The format of the output data file is self-explanatory.

# Code from font description

Initiate the interactive editor by using the `font.sh` script.

The `file` menu enables you to load and save font definitions. 
You can find example font definitions in the resources/font folder.

Look at the layout of the editor window:

- The left section is dedicated to sign editing.
- The upper right section provides information.
- The lower right section contains the font matrix for rapid navigation.

Clicking the left mouse button on the font matrix immediately switches to the respective sign.
The symbol in the edit area can be toggled using the `prev` and `next` buttons.

Use the toolbox with buttons like `clean`, `fill`, `copy`, and `paste` to speed up the design tasks.

Clicking the left mouse button on a pixel in the editor area inverts the pixel value.

While holding the 
- `shift` key, move the mouse cursor for quick area filling.
- `ctrl` key, move the mouse cursor to clean up areas.
- `alt` key, move the mouse cursor to invert pixels.

Under the `generate` menu, you can produce compilable C code from the currently loaded font definition.

The concept of font description can be exemplified using the part of 8x8 font sample.

```json
{
    "name": "small",
    "width": 8,
    "height": 8,
    "font": [
        {
            "data": [
                "0x00",
                "0x00",
                "0x00",
                "0x00",
                "0x00",
                "0x00",
                "0x00",
                "0x00"
            ],
            "symbol": " "
        },

        ...

    ]
}
```

The font's name, which is also utilized for the C code file names, can be specified in the `name` field.

The `width` and `height` fields define the dimensions of each symbol. 
Please provide values that are multiples of 8.

The `symbol` field offers a human-readable representation of the character.
Let this field empty, using space " ", for spezial characters that don't have a representation.

The `data` field holds the pixel values of the character matrix. 

Pixels can be defined in a row or column-wise manner.
The pixels of a row or column are sequenced from left to right or from top to bottom in the byte sequence.

Set the radio button above the font matrix area to the appropriate setting for fonts defined in rows or column-wise manner.

The format of the output data file is self-explanatory.
