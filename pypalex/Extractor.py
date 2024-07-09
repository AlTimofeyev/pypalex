##  @file   Extractor.py
#   @brief  Extraction utility class for extracting colors from the image.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on February 10, 2022.
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 6, 2023.
#   - Modified by Al Timofeyev on March 22, 2023.
#   - Modified by Al Timofeyev on April 5, 2023.
#   - Modified by Al Timofeyev on June 10, 2024.
#   - Modified by Al Timofeyev on July 8, 2024.


# ---- IMPORTS ----
from . import extraction_utils as exutil
from . import conversion_utils as convert
from . import constants as const


##  Extracts colors given a matrix of HSV values extracted from an image.
class Extractor:

    ##  Extractor Constructor.
    #
    #   @param  self                The object pointer.
    #   @param  hsv_img_matrix_2d   A 2D numpy array of pixels from an image in [h,s,v] format.
    #   @param  image_name          The name of the image file, without any extension (e.g. .jpg, .png, etc.).
    def __init__(self, hsv_img_matrix_2d, image_name=None):
        self.hsv_img_matrix_2d = hsv_img_matrix_2d
        self.image_name = image_name
        self.ratio_dict = {}
        self.base_color_dict = {}
        self.extracted_colors_dict = {}

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Main method for Extractor class.
    #   @details    Performs extraction of colors.
    #
    #   @param  self    The object pointer.
    def run(self):
        # Organize colors.
        self.ratio_dict = exutil.extract_ratios(self.hsv_img_matrix_2d)
        self.base_color_dict = exutil.construct_base_color_dictionary(self.hsv_img_matrix_2d)

        # Extract colors.
        self.extracted_colors_dict = exutil.extract_colors(self.base_color_dict)
        exutil.check_missing_colors(self.base_color_dict, self.extracted_colors_dict)
        exutil.generate_remaining_colors(self.extracted_colors_dict, self.ratio_dict)

        # Organize the extracted colors that is suitable for raw file-saving.
        self.organize_extracted_dictionary()

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Converts the selected color types from the extracted colors to pastel.
    #   @details    There are only 3 color types to choose
    #               from: light, normal, dark.
    #
    #   @param  self            The object pointer.
    #   @param  pastel_light    Flag to convert light color types to pastel.
    #   @param  pastel_normal   Flag to convert normal color types to pastel.
    #   @param  pastel_dark     Flag to convert dark color types to pastel.
    def convert_to_pastel(self, pastel_light=False, pastel_normal=False, pastel_dark=False):
        if pastel_light:
            self.convert_pastel_light()
        if pastel_normal:
            self.convert_pastel_normal()
        if pastel_dark:
            self.convert_pastel_dark()

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Sets the color format of the colors in the extracted dictionary.
    #   @details    There are 3 color formats to choose from:
    #               hsv, rgb and hex.
    #
    #   @note   This can only be done once, as the colors are
    #           converted from hsv to a chosen color format.
    #
    #   @param  self            The object pointer.
    #   @param  color_format    A string that specifies the format each color should have (e.g. 'hsv', 'rgb', 'hex', 'ansi').
    def set_color_format(self, color_format=None):
        if color_format is None:
            return

        if color_format == 'hsv':
            self.extracted_colors_dict['light background'] = [int(self.extracted_colors_dict['light background'][0]),
                                                              round(self.extracted_colors_dict['light background'][1]),
                                                              round(self.extracted_colors_dict['light background'][2])]
            self.extracted_colors_dict['light foreground'] = [int(self.extracted_colors_dict['light foreground'][0]),
                                                              round(self.extracted_colors_dict['light foreground'][1]),
                                                              round(self.extracted_colors_dict['light foreground'][2])]
            self.extracted_colors_dict['dark background'] = [int(self.extracted_colors_dict['dark background'][0]),
                                                             round(self.extracted_colors_dict['dark background'][1]),
                                                             round(self.extracted_colors_dict['dark background'][2])]
            self.extracted_colors_dict['dark foreground'] = [int(self.extracted_colors_dict['dark foreground'][0]),
                                                             round(self.extracted_colors_dict['dark foreground'][1]),
                                                             round(self.extracted_colors_dict['dark foreground'][2])]
            self.extracted_colors_dict['black'] = [int(self.extracted_colors_dict['black'][0]),
                                                   round(self.extracted_colors_dict['black'][1]),
                                                   round(self.extracted_colors_dict['black'][2])]
            self.extracted_colors_dict['red'] = [int(self.extracted_colors_dict['red'][0]),
                                                 round(self.extracted_colors_dict['red'][1]),
                                                 round(self.extracted_colors_dict['red'][2])]
            self.extracted_colors_dict['green'] = [int(self.extracted_colors_dict['green'][0]),
                                                   round(self.extracted_colors_dict['green'][1]),
                                                   round(self.extracted_colors_dict['green'][2])]
            self.extracted_colors_dict['yellow'] = [int(self.extracted_colors_dict['yellow'][0]),
                                                    round(self.extracted_colors_dict['yellow'][1]),
                                                    round(self.extracted_colors_dict['yellow'][2])]
            self.extracted_colors_dict['blue'] = [int(self.extracted_colors_dict['blue'][0]),
                                                  round(self.extracted_colors_dict['blue'][1]),
                                                  round(self.extracted_colors_dict['blue'][2])]
            self.extracted_colors_dict['magenta'] = [int(self.extracted_colors_dict['magenta'][0]),
                                                     round(self.extracted_colors_dict['magenta'][1]),
                                                     round(self.extracted_colors_dict['magenta'][2])]
            self.extracted_colors_dict['cyan'] = [int(self.extracted_colors_dict['cyan'][0]),
                                                  round(self.extracted_colors_dict['cyan'][1]),
                                                  round(self.extracted_colors_dict['cyan'][2])]
            self.extracted_colors_dict['white'] = [int(self.extracted_colors_dict['white'][0]),
                                                   round(self.extracted_colors_dict['white'][1]),
                                                   round(self.extracted_colors_dict['white'][2])]
            self.extracted_colors_dict['light black'] = [int(self.extracted_colors_dict['light black'][0]),
                                                         round(self.extracted_colors_dict['light black'][1]),
                                                         round(self.extracted_colors_dict['light black'][2])]
            self.extracted_colors_dict['light red'] = [int(self.extracted_colors_dict['light red'][0]),
                                                       round(self.extracted_colors_dict['light red'][1]),
                                                       round(self.extracted_colors_dict['light red'][2])]
            self.extracted_colors_dict['light green'] = [int(self.extracted_colors_dict['light green'][0]),
                                                         round(self.extracted_colors_dict['light green'][1]),
                                                         round(self.extracted_colors_dict['light green'][2])]
            self.extracted_colors_dict['light yellow'] = [int(self.extracted_colors_dict['light yellow'][0]),
                                                          round(self.extracted_colors_dict['light yellow'][1]),
                                                          round(self.extracted_colors_dict['light yellow'][2])]
            self.extracted_colors_dict['light blue'] = [int(self.extracted_colors_dict['light blue'][0]),
                                                        round(self.extracted_colors_dict['light blue'][1]),
                                                        round(self.extracted_colors_dict['light blue'][2])]
            self.extracted_colors_dict['light magenta'] = [int(self.extracted_colors_dict['light magenta'][0]),
                                                           round(self.extracted_colors_dict['light magenta'][1]),
                                                           round(self.extracted_colors_dict['light magenta'][2])]
            self.extracted_colors_dict['light cyan'] = [int(self.extracted_colors_dict['light cyan'][0]),
                                                        round(self.extracted_colors_dict['light cyan'][1]),
                                                        round(self.extracted_colors_dict['light cyan'][2])]
            self.extracted_colors_dict['light white'] = [int(self.extracted_colors_dict['light white'][0]),
                                                         round(self.extracted_colors_dict['light white'][1]),
                                                         round(self.extracted_colors_dict['light white'][2])]
            self.extracted_colors_dict['dark black'] = [int(self.extracted_colors_dict['dark black'][0]),
                                                        round(self.extracted_colors_dict['dark black'][1]),
                                                        round(self.extracted_colors_dict['dark black'][2])]
            self.extracted_colors_dict['dark red'] = [int(self.extracted_colors_dict['dark red'][0]),
                                                      round(self.extracted_colors_dict['dark red'][1]),
                                                      round(self.extracted_colors_dict['dark red'][2])]
            self.extracted_colors_dict['dark green'] = [int(self.extracted_colors_dict['dark green'][0]),
                                                        round(self.extracted_colors_dict['dark green'][1]),
                                                        round(self.extracted_colors_dict['dark green'][2])]
            self.extracted_colors_dict['dark yellow'] = [int(self.extracted_colors_dict['dark yellow'][0]),
                                                         round(self.extracted_colors_dict['dark yellow'][1]),
                                                         round(self.extracted_colors_dict['dark yellow'][2])]
            self.extracted_colors_dict['dark blue'] = [int(self.extracted_colors_dict['dark blue'][0]),
                                                       round(self.extracted_colors_dict['dark blue'][1]),
                                                       round(self.extracted_colors_dict['dark blue'][2])]
            self.extracted_colors_dict['dark magenta'] = [int(self.extracted_colors_dict['dark magenta'][0]),
                                                          round(self.extracted_colors_dict['dark magenta'][1]),
                                                          round(self.extracted_colors_dict['dark magenta'][2])]
            self.extracted_colors_dict['dark cyan'] = [int(self.extracted_colors_dict['dark cyan'][0]),
                                                       round(self.extracted_colors_dict['dark cyan'][1]),
                                                       round(self.extracted_colors_dict['dark cyan'][2])]
            self.extracted_colors_dict['dark white'] = [int(self.extracted_colors_dict['dark white'][0]),
                                                        round(self.extracted_colors_dict['dark white'][1]),
                                                        round(self.extracted_colors_dict['dark white'][2])]
        elif color_format == 'hex':
            self.extracted_colors_dict['light background'] = convert.hsv_to_hex(self.extracted_colors_dict['light background'])
            self.extracted_colors_dict['light foreground'] = convert.hsv_to_hex(self.extracted_colors_dict['light foreground'])
            self.extracted_colors_dict['dark background'] = convert.hsv_to_hex(self.extracted_colors_dict['dark background'])
            self.extracted_colors_dict['dark foreground'] = convert.hsv_to_hex(self.extracted_colors_dict['dark foreground'])
            self.extracted_colors_dict['black'] = convert.hsv_to_hex(self.extracted_colors_dict['black'])
            self.extracted_colors_dict['red'] = convert.hsv_to_hex(self.extracted_colors_dict['red'])
            self.extracted_colors_dict['green'] = convert.hsv_to_hex(self.extracted_colors_dict['green'])
            self.extracted_colors_dict['yellow'] = convert.hsv_to_hex(self.extracted_colors_dict['yellow'])
            self.extracted_colors_dict['blue'] = convert.hsv_to_hex(self.extracted_colors_dict['blue'])
            self.extracted_colors_dict['magenta'] = convert.hsv_to_hex(self.extracted_colors_dict['magenta'])
            self.extracted_colors_dict['cyan'] = convert.hsv_to_hex(self.extracted_colors_dict['cyan'])
            self.extracted_colors_dict['white'] = convert.hsv_to_hex(self.extracted_colors_dict['white'])
            self.extracted_colors_dict['light black'] = convert.hsv_to_hex(self.extracted_colors_dict['light black'])
            self.extracted_colors_dict['light red'] = convert.hsv_to_hex(self.extracted_colors_dict['light red'])
            self.extracted_colors_dict['light green'] = convert.hsv_to_hex(self.extracted_colors_dict['light green'])
            self.extracted_colors_dict['light yellow'] = convert.hsv_to_hex(self.extracted_colors_dict['light yellow'])
            self.extracted_colors_dict['light blue'] = convert.hsv_to_hex(self.extracted_colors_dict['light blue'])
            self.extracted_colors_dict['light magenta'] = convert.hsv_to_hex(self.extracted_colors_dict['light magenta'])
            self.extracted_colors_dict['light cyan'] = convert.hsv_to_hex(self.extracted_colors_dict['light cyan'])
            self.extracted_colors_dict['light white'] = convert.hsv_to_hex(self.extracted_colors_dict['light white'])
            self.extracted_colors_dict['dark black'] = convert.hsv_to_hex(self.extracted_colors_dict['dark black'])
            self.extracted_colors_dict['dark red'] = convert.hsv_to_hex(self.extracted_colors_dict['dark red'])
            self.extracted_colors_dict['dark green'] = convert.hsv_to_hex(self.extracted_colors_dict['dark green'])
            self.extracted_colors_dict['dark yellow'] = convert.hsv_to_hex(self.extracted_colors_dict['dark yellow'])
            self.extracted_colors_dict['dark blue'] = convert.hsv_to_hex(self.extracted_colors_dict['dark blue'])
            self.extracted_colors_dict['dark magenta'] = convert.hsv_to_hex(self.extracted_colors_dict['dark magenta'])
            self.extracted_colors_dict['dark cyan'] = convert.hsv_to_hex(self.extracted_colors_dict['dark cyan'])
            self.extracted_colors_dict['dark white'] = convert.hsv_to_hex(self.extracted_colors_dict['dark white'])
        elif color_format == 'rgb':
            self.extracted_colors_dict['light background'] = convert.hsv_to_rgb(self.extracted_colors_dict['light background'])
            self.extracted_colors_dict['light foreground'] = convert.hsv_to_rgb(self.extracted_colors_dict['light foreground'])
            self.extracted_colors_dict['dark background'] = convert.hsv_to_rgb(self.extracted_colors_dict['dark background'])
            self.extracted_colors_dict['dark foreground'] = convert.hsv_to_rgb(self.extracted_colors_dict['dark foreground'])
            self.extracted_colors_dict['black'] = convert.hsv_to_rgb(self.extracted_colors_dict['black'])
            self.extracted_colors_dict['red'] = convert.hsv_to_rgb(self.extracted_colors_dict['red'])
            self.extracted_colors_dict['green'] = convert.hsv_to_rgb(self.extracted_colors_dict['green'])
            self.extracted_colors_dict['yellow'] = convert.hsv_to_rgb(self.extracted_colors_dict['yellow'])
            self.extracted_colors_dict['blue'] = convert.hsv_to_rgb(self.extracted_colors_dict['blue'])
            self.extracted_colors_dict['magenta'] = convert.hsv_to_rgb(self.extracted_colors_dict['magenta'])
            self.extracted_colors_dict['cyan'] = convert.hsv_to_rgb(self.extracted_colors_dict['cyan'])
            self.extracted_colors_dict['white'] = convert.hsv_to_rgb(self.extracted_colors_dict['white'])
            self.extracted_colors_dict['light black'] = convert.hsv_to_rgb(self.extracted_colors_dict['light black'])
            self.extracted_colors_dict['light red'] = convert.hsv_to_rgb(self.extracted_colors_dict['light red'])
            self.extracted_colors_dict['light green'] = convert.hsv_to_rgb(self.extracted_colors_dict['light green'])
            self.extracted_colors_dict['light yellow'] = convert.hsv_to_rgb(self.extracted_colors_dict['light yellow'])
            self.extracted_colors_dict['light blue'] = convert.hsv_to_rgb(self.extracted_colors_dict['light blue'])
            self.extracted_colors_dict['light magenta'] = convert.hsv_to_rgb(self.extracted_colors_dict['light magenta'])
            self.extracted_colors_dict['light cyan'] = convert.hsv_to_rgb(self.extracted_colors_dict['light cyan'])
            self.extracted_colors_dict['light white'] = convert.hsv_to_rgb(self.extracted_colors_dict['light white'])
            self.extracted_colors_dict['dark black'] = convert.hsv_to_rgb(self.extracted_colors_dict['dark black'])
            self.extracted_colors_dict['dark red'] = convert.hsv_to_rgb(self.extracted_colors_dict['dark red'])
            self.extracted_colors_dict['dark green'] = convert.hsv_to_rgb(self.extracted_colors_dict['dark green'])
            self.extracted_colors_dict['dark yellow'] = convert.hsv_to_rgb(self.extracted_colors_dict['dark yellow'])
            self.extracted_colors_dict['dark blue'] = convert.hsv_to_rgb(self.extracted_colors_dict['dark blue'])
            self.extracted_colors_dict['dark magenta'] = convert.hsv_to_rgb(self.extracted_colors_dict['dark magenta'])
            self.extracted_colors_dict['dark cyan'] = convert.hsv_to_rgb(self.extracted_colors_dict['dark cyan'])
            self.extracted_colors_dict['dark white'] = convert.hsv_to_rgb(self.extracted_colors_dict['dark white'])
        elif color_format == 'ansi':
            self.extracted_colors_dict['light background'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['light background']), background=True)
            self.extracted_colors_dict['light foreground'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['light foreground']))
            self.extracted_colors_dict['dark background'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['dark background']), background=True)
            self.extracted_colors_dict['dark foreground'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['dark foreground']))
            self.extracted_colors_dict['black'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['black']))
            self.extracted_colors_dict['red'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['red']))
            self.extracted_colors_dict['green'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['green']))
            self.extracted_colors_dict['yellow'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['yellow']))
            self.extracted_colors_dict['blue'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['blue']))
            self.extracted_colors_dict['magenta'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['magenta']))
            self.extracted_colors_dict['cyan'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['cyan']))
            self.extracted_colors_dict['white'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['white']))
            self.extracted_colors_dict['light black'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['light black']))
            self.extracted_colors_dict['light red'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['light red']))
            self.extracted_colors_dict['light green'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['light green']))
            self.extracted_colors_dict['light yellow'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['light yellow']))
            self.extracted_colors_dict['light blue'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['light blue']))
            self.extracted_colors_dict['light magenta'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['light magenta']))
            self.extracted_colors_dict['light cyan'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['light cyan']))
            self.extracted_colors_dict['light white'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['light white']))
            self.extracted_colors_dict['dark black'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['dark black']))
            self.extracted_colors_dict['dark red'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['dark red']))
            self.extracted_colors_dict['dark green'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['dark green']))
            self.extracted_colors_dict['dark yellow'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['dark yellow']))
            self.extracted_colors_dict['dark blue'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['dark blue']))
            self.extracted_colors_dict['dark magenta'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['dark magenta']))
            self.extracted_colors_dict['dark cyan'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['dark cyan']))
            self.extracted_colors_dict['dark white'] = convert.rgb_to_ansi(convert.hsv_to_rgb(self.extracted_colors_dict['dark white']))

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Generates palettes based on a dictionary of palette templates.
    #   @note   Palette templates follow a certain structure. Each palette
    #           template has a name (key) and a dictionary (value). For a
    #           more thorough explanation please refer to the Configuration
    #           File page on the PyPalEx GitHub's Wiki page:
    #           https://github.com/AlTimofeyev/pypalex/wiki/Configuration-File
    #
    #   @param  palette_templates   A dictionary of palette template dictionaries.
    #
    #   @return A dictionary of color palettes.
    def generate_palettes(self, palette_templates=None):
        if palette_templates is None or not palette_templates:
            return self.generate_default_palettes()

        palettes = {}
        for palette_name, colors_dict in palette_templates.items():
            # Default to using a dark palette type.
            background = self.extracted_colors_dict['dark background']
            foreground = self.extracted_colors_dict['light foreground']
            color0 = self.extracted_colors_dict['black']
            color7 = self.extracted_colors_dict['white']
            color8 = self.extracted_colors_dict['light black']
            color15 = self.extracted_colors_dict['light white']

            # All colors are set to black as a fail-safe.
            color1 = color2 = color3 = color4 = color5 = color6 = \
                color9 = color10 = color11 = color12 = color13 = color14 = self.extracted_colors_dict['black']

            for key, color_name in colors_dict.items():
                if key == 'palette-type':
                    # The dark palette type is assigned by default, so we only test for light.
                    if color_name == 'light':
                        background = self.extracted_colors_dict['light background']
                        foreground = self.extracted_colors_dict['dark foreground']
                        color8 = self.extracted_colors_dict['dark black']
                        color15 = self.extracted_colors_dict['dark white']
                elif color_name not in self.extracted_colors_dict:
                    continue
                elif key == 'color1':
                    color1 = self.extracted_colors_dict[color_name]
                elif key == 'color2':
                    color2 = self.extracted_colors_dict[color_name]
                elif key == 'color3':
                    color3 = self.extracted_colors_dict[color_name]
                elif key == 'color4':
                    color4 = self.extracted_colors_dict[color_name]
                elif key == 'color5':
                    color5 = self.extracted_colors_dict[color_name]
                elif key == 'color6':
                    color6 = self.extracted_colors_dict[color_name]
                elif key == 'color9':
                    color9 = self.extracted_colors_dict[color_name]
                elif key == 'color10':
                    color10 = self.extracted_colors_dict[color_name]
                elif key == 'color11':
                    color11 = self.extracted_colors_dict[color_name]
                elif key == 'color12':
                    color12 = self.extracted_colors_dict[color_name]
                elif key == 'color13':
                    color13 = self.extracted_colors_dict[color_name]
                elif key == 'color14':
                    color14 = self.extracted_colors_dict[color_name]

            palettes[palette_name] = {
                'background': background,
                'foreground': foreground,
                'color0': color0,
                'color1': color1,
                'color2': color2,
                'color3': color3,
                'color4': color4,
                'color5': color5,
                'color6': color6,
                'color7': color7,
                'color8': color8,
                'color9': color9,
                'color10': color10,
                'color11': color11,
                'color12': color12,
                'color13': color13,
                'color14': color14,
                'color15': color15
            }

        return palettes

    # **************************************************************************
    # **************************************************************************

    ##  Organizes the extracted colors dictionary.
    #   @details    The reorganization of the extracted colors' dictionary
    #               is done so that the (key, value) pairs appear in a
    #               specific order. This will be useful if the user wants
    #               to export the raw hierarchy of the data.
    #
    #   @param  self    The object pointer.
    def organize_extracted_dictionary(self):
        self.extracted_colors_dict = {
            'light background': self.extracted_colors_dict['light background'],
            'light foreground': self.extracted_colors_dict['light foreground'],
            'dark background': self.extracted_colors_dict['dark background'],
            'dark foreground': self.extracted_colors_dict['dark foreground'],
            'black': self.extracted_colors_dict['black'],
            'red': self.extracted_colors_dict['red'],
            'green': self.extracted_colors_dict['green'],
            'yellow': self.extracted_colors_dict['yellow'],
            'blue': self.extracted_colors_dict['blue'],
            'magenta': self.extracted_colors_dict['magenta'],
            'cyan': self.extracted_colors_dict['cyan'],
            'white': self.extracted_colors_dict['white'],
            'light black': self.extracted_colors_dict['light black'],
            'light red': self.extracted_colors_dict['light red'],
            'light green': self.extracted_colors_dict['light green'],
            'light yellow': self.extracted_colors_dict['light yellow'],
            'light blue': self.extracted_colors_dict['light blue'],
            'light magenta': self.extracted_colors_dict['light magenta'],
            'light cyan': self.extracted_colors_dict['light cyan'],
            'light white': self.extracted_colors_dict['light white'],
            'dark black': self.extracted_colors_dict['dark black'],
            'dark red': self.extracted_colors_dict['dark red'],
            'dark green': self.extracted_colors_dict['dark green'],
            'dark yellow': self.extracted_colors_dict['dark yellow'],
            'dark blue': self.extracted_colors_dict['dark blue'],
            'dark magenta': self.extracted_colors_dict['dark magenta'],
            'dark cyan': self.extracted_colors_dict['dark cyan'],
            'dark white': self.extracted_colors_dict['dark white']
        }

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Converts light color type to pastel.
    #
    #   @param  self    The object pointer.
    def convert_pastel_light(self):
        self.convert_pastel(self.extracted_colors_dict['light red'])
        self.convert_pastel(self.extracted_colors_dict['light yellow'])
        self.convert_pastel(self.extracted_colors_dict['light green'])
        self.convert_pastel(self.extracted_colors_dict['light cyan'])
        self.convert_pastel(self.extracted_colors_dict['light blue'])
        self.convert_pastel(self.extracted_colors_dict['light magenta'])

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Converts normal color type to pastel.
    #
    #   @param  self    The object pointer.
    def convert_pastel_normal(self):
        self.convert_pastel(self.extracted_colors_dict['red'])
        self.convert_pastel(self.extracted_colors_dict['yellow'])
        self.convert_pastel(self.extracted_colors_dict['green'])
        self.convert_pastel(self.extracted_colors_dict['cyan'])
        self.convert_pastel(self.extracted_colors_dict['blue'])
        self.convert_pastel(self.extracted_colors_dict['magenta'])

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Converts dark color type to pastel.
    #
    #   @param  self    The object pointer.
    def convert_pastel_dark(self):
        self.convert_pastel(self.extracted_colors_dict['dark red'])
        self.convert_pastel(self.extracted_colors_dict['dark yellow'])
        self.convert_pastel(self.extracted_colors_dict['dark green'])
        self.convert_pastel(self.extracted_colors_dict['dark cyan'])
        self.convert_pastel(self.extracted_colors_dict['dark blue'])
        self.convert_pastel(self.extracted_colors_dict['dark magenta'])

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Generates a default set of palettes from the extracted colors.
    #
    #   @return A dictionary of default color palettes.
    def generate_default_palettes(self):
        light_palette = {
            'background': self.extracted_colors_dict['light background'],
            'foreground': self.extracted_colors_dict['dark foreground'],
            'color0': self.extracted_colors_dict['black'],
            'color1': self.extracted_colors_dict['red'],
            'color2': self.extracted_colors_dict['green'],
            'color3': self.extracted_colors_dict['yellow'],
            'color4': self.extracted_colors_dict['blue'],
            'color5': self.extracted_colors_dict['magenta'],
            'color6': self.extracted_colors_dict['cyan'],
            'color7': self.extracted_colors_dict['white'],
            'color8': self.extracted_colors_dict['dark black'],
            'color9': self.extracted_colors_dict['dark red'],
            'color10': self.extracted_colors_dict['dark green'],
            'color11': self.extracted_colors_dict['dark yellow'],
            'color12': self.extracted_colors_dict['dark blue'],
            'color13': self.extracted_colors_dict['dark magenta'],
            'color14': self.extracted_colors_dict['dark cyan'],
            'color15': self.extracted_colors_dict['dark white']
        }

        dark_palette = {
            'background': self.extracted_colors_dict['dark background'],
            'foreground': self.extracted_colors_dict['light foreground'],
            'color0': self.extracted_colors_dict['black'],
            'color1': self.extracted_colors_dict['red'],
            'color2': self.extracted_colors_dict['green'],
            'color3': self.extracted_colors_dict['yellow'],
            'color4': self.extracted_colors_dict['blue'],
            'color5': self.extracted_colors_dict['magenta'],
            'color6': self.extracted_colors_dict['cyan'],
            'color7': self.extracted_colors_dict['white'],
            'color8': self.extracted_colors_dict['light black'],
            'color9': self.extracted_colors_dict['light red'],
            'color10': self.extracted_colors_dict['light green'],
            'color11': self.extracted_colors_dict['light yellow'],
            'color12': self.extracted_colors_dict['light blue'],
            'color13': self.extracted_colors_dict['light magenta'],
            'color14': self.extracted_colors_dict['light cyan'],
            'color15': self.extracted_colors_dict['light white']
        }

        palettes = {'light-theme': light_palette, 'dark-theme': dark_palette}

        return palettes

    # **************************************************************************
    # **************************************************************************

    ##  Converts/normalizes HSV color to pastel.
    #   @details    For values x in range [a, b], values x can be normalized
    #               to the new range [y, z] with the following equation:
    #               new_x = y + ( ((x-a) / (b-a)) * (z-y) )
    #   @note   I'm using the normalization formula from https://stats.stackexchange.com/a/281164
    #
    #   @param  self        The object pointer.
    #   @param  hsv_color   List HSV color to be converted to pastel.
    def convert_pastel(self, hsv_color):
        # Define the old and new bounds for the saturation and brightness ranges.
        old_sat_bounds = [const.SATURATION_TOLERANCE_RANGE[0], 100.0]
        new_sat_bounds = [const.PASTEL_SATURATION_RANGE[0], const.PASTEL_SATURATION_RANGE[1]]
        old_bright_bounds = [const.DARK_BRIGHTNESS_RANGE[0], const.LIGHT_BRIGHTNESS_RANGE[1]]
        new_bright_bounds = [const.PASTEL_BRIGHTNESS_RANGE[0], const.PASTEL_BRIGHTNESS_RANGE[1]]

        # Only convert saturation to pastel if it is outside the pastel saturation range.
        if hsv_color[1] < new_sat_bounds[0] or hsv_color[1] > new_sat_bounds[1]:
            hsv_color[1] = new_sat_bounds[0] + (
                    ((hsv_color[1] - old_sat_bounds[0]) / (old_sat_bounds[1] - old_sat_bounds[0]))
                    * (new_sat_bounds[1] - new_sat_bounds[0]))

        hsv_color[2] = new_bright_bounds[0] + (
                ((hsv_color[2] - old_bright_bounds[0]) / (old_bright_bounds[1] - old_bright_bounds[0]))
                * (new_bright_bounds[1] - new_bright_bounds[0]))

    # **************************************************************************
    # ********************* GLOBAL VARIABLE DOCUMENTATION **********************
    # **************************************************************************

    ##  @var    hsv_img_matrix_2d
    #   A 2D numpy array of pixels from an image in [h,s,v] format.
    ##  @var    image_name
    #   The name of the image file, without any extension (e.g. .jpg, .png, etc.).
    ##  @var    ratio_dict
    #   A dictionary that holds the ratio of base colors in an image and is
    #   used to identify the dominant color in an image.
    ##  @var    base_color_dict
    #   A dictionary of 2D numpy arrays for each of the 6 base colors.
    ##  @var    extracted_colors_dict
    #   A dictionary of extracted colors in [h,s,v] format.
