##  @file   file_utils.py
#   @brief  Utilities for file handling.
#
#   @note   Potential point for contributors to add
#           different output saving options.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on April 5, 2023.


# ---- IMPORTS ----
import json


##  Saves color palette to json file.
#
#   @note    If a file with the same name already exists, it is overwritten.
#
#   @param  color_palette   Dictionary of light, normal, and dark color palettes.
#   @param  output_filepath Output file path with filename of where to store color palette.
def save_palette_to_file(color_palette, output_filepath):
    with open(output_filepath, 'w') as outfile:
        json.dump(color_palette, outfile, indent=4)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Saves color palette to json file as default color schemes.
#   @details    Constructs 2 default color schemes, light and
#               dark, using the color palettes and saves them
#               to a json file.
#
#   @note    If a file with the same name already exists, it is overwritten.
#
#   @param  color_palette   Dictionary of light, normal, and dark color palettes.
#   @param  output_filepath Output file path with filename of where to store color palette.
def save_default_scheme_to_file(color_palette, output_filepath):
    light_scheme = {
        'background': color_palette['light background'],
        'foreground': color_palette['dark foreground'],
        'black': color_palette['normal black'],
        'red': color_palette['normal red'],
        'green': color_palette['normal green'],
        'yellow': color_palette['normal yellow'],
        'blue': color_palette['normal blue'],
        'magenta': color_palette['normal magenta'],
        'cyan': color_palette['normal cyan'],
        'white': color_palette['normal white'],
        'bright black': color_palette['dark black'],
        'bright red': color_palette['dark red'],
        'bright green': color_palette['dark green'],
        'bright yellow': color_palette['dark yellow'],
        'bright blue': color_palette['dark blue'],
        'bright magenta': color_palette['dark magenta'],
        'bright cyan': color_palette['dark cyan'],
        'bright white': color_palette['dark white']
    }

    dark_scheme = {
        'background': color_palette['dark background'],
        'foreground': color_palette['light foreground'],
        'black': color_palette['normal black'],
        'red': color_palette['normal red'],
        'green': color_palette['normal green'],
        'yellow': color_palette['normal yellow'],
        'blue': color_palette['normal blue'],
        'magenta': color_palette['normal magenta'],
        'cyan': color_palette['normal cyan'],
        'white': color_palette['normal white'],
        'bright black': color_palette['light black'],
        'bright red': color_palette['light red'],
        'bright green': color_palette['light green'],
        'bright yellow': color_palette['light yellow'],
        'bright blue': color_palette['light blue'],
        'bright magenta': color_palette['light magenta'],
        'bright cyan': color_palette['light cyan'],
        'bright white': color_palette['light white']
    }

    color_schemes_dict = {
        'light': light_scheme,
        'dark': dark_scheme
    }

    with open(output_filepath, 'w') as outfile:
        json.dump(color_schemes_dict, outfile, indent=4)