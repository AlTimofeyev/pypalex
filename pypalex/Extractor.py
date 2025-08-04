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
#   - Modified by Al Timofeyev on October 12, 2024.
#   - Modified by Al Timofeyev on August 3, 2025.


# ---- IMPORTS ----
import math
import statistics as stats
from PIL import Image

from . import image_utils as imutils
from . import extraction_utils as exutil
from . import conversion_utils as convert
from . import constants as const


##  Extracts colors given a matrix of HSV values extracted from an image.
class Extractor:

    ##  Extractor Constructor.
    #
    #   @param  self    The object pointer.
    def __init__(self):
        self.hsv_img_matrix_2d = []
        self.image_name = None
        self.color_format = None
        self.ratio_dict = {}
        self.base_color_dict = {}
        self.extracted_colors_dict = {}

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Loads the Extrator class with the provided image.
    #
    #   @param  self                The object pointer.
    #   @param  absolute_image_path A string that represents the absolute path to an image.
    #   @param  image_name          A string that represents the name of the image or any name you want to provide with the current image being used.
    def load(self, absolute_image_path, image_name=None):
        # Reset all global variables.
        self.image_name = image_name
        self.color_format = 'hsv'
        self.ratio_dict = {}
        self.base_color_dict = {}
        self.extracted_colors_dict = {}

        # Load the image data.
        image = Image.open(absolute_image_path)
        self.hsv_img_matrix_2d = imutils.process_image(image)

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Main method for Extractor class.
    #   @details    Performs extraction of colors.
    #
    #   @param  self    The object pointer.
    def run(self):
        # If the extractor hasn't been loaded with an image.
        if len(self.hsv_img_matrix_2d) == 0:
            return

        # Organize colors.
        self.ratio_dict = exutil.extract_ratios(self.hsv_img_matrix_2d)
        self.base_color_dict = exutil.construct_base_color_dictionary(self.hsv_img_matrix_2d)

        # Extract colors.
        self.extracted_colors_dict = exutil.extract_colors(self.base_color_dict, ratios=self.ratio_dict)
        exutil.check_missing_colors(self.base_color_dict, self.extracted_colors_dict)
        exutil.generate_remaining_colors(self.extracted_colors_dict, self.ratio_dict)

        # Organize the extracted colors in an order that is suitable for raw file-saving.
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
    #   @details    There are 4 color formats to choose from:
    #               hsv, rgb, hex and ansi.
    #
    #   @note   There is a loss in precision when converting between color
    #           formats more than once. If you would like to convert color
    #           formats more than once while maintaining precision of the
    #           colors, please use an auxiliary dictionary to store copies
    #           of the original extracted colors before converting to a
    #           different format.
    #
    #   @param  self                The object pointer.
    #   @param  new_color_format    A string that represents the format each color should have (e.g. 'hsv', 'rgb', 'hex', 'ansi').
    #   @param  colors_dict         A dictionary of color names and their color values (optional parameter and can be a palette dictionary).
    def set_color_format(self, new_color_format, colors_dict=None):
        new_color_format = new_color_format.lower()     # Dummy-proof, make sure color format is lowercase.

        extracted_colors_dict_used = colors_dict is None

        if extracted_colors_dict_used:
            colors_dict = self.extracted_colors_dict

        if new_color_format == 'hsv' and self.color_format == 'hsv':
            # Just convert color values from numpy arrays into lists
            # and clean up their hsv values to be whole integers.
            for color_name, color_value in colors_dict.items():
                colors_dict[color_name] = [int(color_value[0]), round(color_value[1]), round(color_value[2])]
            return

        if new_color_format == self.color_format:   # Ignore cases where new and current color format are the same.
            return

        if new_color_format not in {'hsv', 'rgb', 'hex', 'ansi'}:   # Make sure new color format is supported.
            return

        # Function lookup table.
        function_lookup = {'hsv_to_rgb': convert.hsv_to_rgb, 'hsv_to_hex': convert.hsv_to_hex, 'hsv_to_ansi': convert.hsv_to_ansi,
                           'rgb_to_hsv': convert.rgb_to_hsv, 'rgb_to_hex': convert.rgb_to_hex, 'rgb_to_ansi': convert.rgb_to_ansi,
                           'hex_to_hsv': convert.hex_to_hsv, 'hex_to_rgb': convert.hex_to_rgb, 'hex_to_ansi': convert.hex_to_ansi,
                           'ansi_to_hsv': convert.ansi_to_hsv, 'ansi_to_rgb': convert.ansi_to_rgb, 'ansi_to_hex': convert.ansi_to_hex}

        function_name = self.color_format + '_to_' + new_color_format

        for color_name, color_value in colors_dict.items():
            if new_color_format == 'ansi' and color_name in {'background', 'light background', 'dark background'}:
                colors_dict[color_name] = function_lookup[function_name](color_value, background=True)
            else:
                colors_dict[color_name] = function_lookup[function_name](color_value)

        # If we changed the color format of the extracted colors dictionary,
        # we need to update the color format for this Extractor object.
        if extracted_colors_dict_used:
            self.color_format = new_color_format

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Generates palettes based on a dictionary of palette templates.
    #   @note   Palette templates follow a certain structure. Each palette
    #           template has a name (key) and a dictionary (value). For a
    #           more thorough explanation please refer to the Configuration
    #           File page on the PyPalEx GitHub's Wiki page:
    #           https://github.com/AlTimofeyev/pypalex/wiki/Configuration-File
    #
    #   @param  self                The object pointer.
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

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Generates two adaptive palettes based on the dominant color of each color-pair.
    #   @details    Color-pairs are pairs of colors that are adjacent
    #               on the color wheel. Color-pairs include [rose, red],
    #               [orange, yellow], [chartreuse, green], [spring, cyan],
    #               [azure, blue] and [violet, magenta].
    #
    #   @note   The Goldilocks naming convention is a tribute to the
    #           goldilocks zone (meaning "ideal" colors).
    #
    #   @param  self                The object pointer.
    #   @param  light_palette_name  A string representation of the light palette name.
    #   @param  dark_palette_name   A string representation of the dark palette name.
    #
    #   @return A dictionary with two palettes.
    def generate_adaptive_palettes(self, light_palette_name='goldilocks-light', dark_palette_name='goldilocks-dark'):
        # The extracted colors need to be in HSV format.
        if self.color_format != 'hsv':
            return {}

        dom_color_name = exutil.get_dominant_color_name(self.ratio_dict)

        # Get 6 goldilocks color sets (color set = [normal, light, dark]).
        goldilocks_colorset1 = self.get_goldilocks_colorset('rose', 'red', dom_color_name)
        goldilocks_colorset2 = self.get_goldilocks_colorset('orange', 'yellow', dom_color_name)
        goldilocks_colorset3 = self.get_goldilocks_colorset('chartreuse', 'green', dom_color_name)
        goldilocks_colorset4 = self.get_goldilocks_colorset('spring', 'cyan', dom_color_name)
        goldilocks_colorset5 = self.get_goldilocks_colorset('azure', 'blue', dom_color_name)
        goldilocks_colorset6 = self.get_goldilocks_colorset('violet', 'magenta', dom_color_name)

        # Organize palettes using the color sets.
        light_palette = {
            'background': self.extracted_colors_dict['light background'],
            'foreground': self.extracted_colors_dict['dark foreground'],
            'color0': self.extracted_colors_dict['black'],
            'color1': goldilocks_colorset1[0],
            'color2': goldilocks_colorset3[0],
            'color3': goldilocks_colorset2[0],
            'color4': goldilocks_colorset5[0],
            'color5': goldilocks_colorset6[0],
            'color6': goldilocks_colorset4[0],
            'color7': self.extracted_colors_dict['white'],
            'color8': self.extracted_colors_dict['dark black'],
            'color9': goldilocks_colorset1[2],
            'color10': goldilocks_colorset3[2],
            'color11': goldilocks_colorset2[2],
            'color12': goldilocks_colorset5[2],
            'color13': goldilocks_colorset6[2],
            'color14': goldilocks_colorset4[2],
            'color15': self.extracted_colors_dict['dark white']
        }

        dark_palette = {
            'background': self.extracted_colors_dict['dark background'],
            'foreground': self.extracted_colors_dict['light foreground'],
            'color0': self.extracted_colors_dict['black'],
            'color1': goldilocks_colorset1[0],
            'color2': goldilocks_colorset3[0],
            'color3': goldilocks_colorset2[0],
            'color4': goldilocks_colorset5[0],
            'color5': goldilocks_colorset6[0],
            'color6': goldilocks_colorset4[0],
            'color7': self.extracted_colors_dict['white'],
            'color8': self.extracted_colors_dict['light black'],
            'color9': goldilocks_colorset1[1],
            'color10': goldilocks_colorset3[1],
            'color11': goldilocks_colorset2[1],
            'color12': goldilocks_colorset5[1],
            'color13': goldilocks_colorset6[1],
            'color14': goldilocks_colorset4[1],
            'color15': self.extracted_colors_dict['light white']
        }

        palettes = {light_palette_name: light_palette, dark_palette_name: dark_palette}

        return palettes

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ## Generates two mood palettes, starting with the dominant color in the image.
    #
    #   @param  self                The object pointer.
    #   @param  light_palette_name  A string representation of the light palette name.
    #   @param  dark_palette_name   A string representation of the dark palette name.
    #
    #   @return A dictionary with two palettes.
    def generate_mood_palettes(self, light_palette_name='light-mood', dark_palette_name='dark-mood'):
        #   ___________________________________________________________
        #   || (Left side).............................(Right side)  ||
        #   || ------⦧------⦧--------⦧---------⦧----------⦧------  ||
        #   || |...red...orange...yellow...chartreuse...green....|  ||
        #   || -----⦧--------⦧-------⦧------⦧------⦧--------⦧---- ||
        #   || |.violet...magenta...rose...red...orange...yellow.| ||
        #   ---------------------------------------------------------
        color_names = ['red', 'orange', 'yellow', 'chartreuse', 'green', 'spring', 'cyan', 'azure', 'blue', 'violet', 'magenta', 'rose']

        dom_color_name = exutil.get_dominant_color_name(self.ratio_dict)

        # Calculate the ratio values of colors to the left and to the right of the dominant color.
        # This will identify which side has more dominant colors that appear more frequently.
        start_color_idx = self.get_color_index(dom_color_name)
        left_ratio, right_ratio = 0.0, 0.0
        for i in range(1, 6):
            left_ratio += self.ratio_dict[color_names[start_color_idx - i]]
            right_ratio += self.ratio_dict[color_names[(start_color_idx + i) % len(color_names)]]

        # Define the starting, left and right positions in the palettes.
        start_code_idx = self.get_color_code_index(dom_color_name)
        left_code_idx = start_code_idx - 1
        right_code_idx = start_code_idx + 1

        # Identify which side the dominant colors will be assigned to.
        dom_colors_assigned_to = None

        # if left side has more color codes available in the palette.
        if start_code_idx > 2:
            # if colors to the left of dominant color appear more
            # often than colors to the right of dominant color.
            if left_ratio > right_ratio:
                dom_colors_assigned_to = 'left'
            else:
                dom_colors_assigned_to = 'right'
        # if right side has more color codes available in the palette.
        else:
            # if colors to the left of dominant color appear more
            # often than colors to the right of dominant color.
            if left_ratio > right_ratio:
                dom_colors_assigned_to = 'right'
            else:
                dom_colors_assigned_to = 'left'

        # Initialize color codes with default values.
        standard_colors = ['black', 'black', 'black', 'black', 'black', 'black']
        high_intensity_colors1 = ['black', 'black', 'black', 'black', 'black', 'black']
        high_intensity_colors2 = ['black', 'black', 'black', 'black', 'black', 'black']

        # Assign the initial starting color to the color codes.
        standard_colors[start_code_idx] = self.extracted_colors_dict[dom_color_name]
        high_intensity_colors1[start_code_idx] = self.extracted_colors_dict['light ' + dom_color_name]
        high_intensity_colors2[start_code_idx] = self.extracted_colors_dict['dark ' + dom_color_name]

        # Assign colors to the color codes.
        for i in range(1, 6):
            left_color_name, right_color_name = 'black', 'black'    # failsafe color

            if dom_colors_assigned_to == 'left':
                left_color_name = color_names[start_color_idx - i]
                right_color_name = color_names[(start_color_idx + i) % len(color_names)]
            elif dom_colors_assigned_to == 'right':
                left_color_name = color_names[(start_color_idx + i) % len(color_names)]
                right_color_name = color_names[start_color_idx - i]

            if left_code_idx > -1:
                standard_colors[left_code_idx] = self.extracted_colors_dict[left_color_name]
                high_intensity_colors1[left_code_idx] = self.extracted_colors_dict['light ' + left_color_name]
                high_intensity_colors2[left_code_idx] = self.extracted_colors_dict['dark ' + left_color_name]
                left_code_idx -= 1

            if right_code_idx < 6:
                standard_colors[right_code_idx] = self.extracted_colors_dict[right_color_name]
                high_intensity_colors1[right_code_idx] = self.extracted_colors_dict['light ' + right_color_name]
                high_intensity_colors2[right_code_idx] = self.extracted_colors_dict['dark ' + right_color_name]
                right_code_idx += 1

        # Organize palettes using the color codes.
        light_palette = {
            'background': self.extracted_colors_dict['light background'],
            'foreground': self.extracted_colors_dict['dark foreground'],
            'color0': self.extracted_colors_dict['black'],
            'color1': standard_colors[0],
            'color2': standard_colors[1],
            'color3': standard_colors[2],
            'color4': standard_colors[3],
            'color5': standard_colors[4],
            'color6': standard_colors[5],
            'color7': self.extracted_colors_dict['white'],
            'color8': self.extracted_colors_dict['dark black'],
            'color9': high_intensity_colors2[0],
            'color10': high_intensity_colors2[1],
            'color11': high_intensity_colors2[2],
            'color12': high_intensity_colors2[3],
            'color13': high_intensity_colors2[4],
            'color14': high_intensity_colors2[5],
            'color15': self.extracted_colors_dict['dark white']
        }

        dark_palette = {
            'background': self.extracted_colors_dict['dark background'],
            'foreground': self.extracted_colors_dict['light foreground'],
            'color0': self.extracted_colors_dict['black'],
            'color1': standard_colors[0],
            'color2': standard_colors[1],
            'color3': standard_colors[2],
            'color4': standard_colors[3],
            'color5': standard_colors[4],
            'color6': standard_colors[5],
            'color7': self.extracted_colors_dict['white'],
            'color8': self.extracted_colors_dict['light black'],
            'color9': high_intensity_colors1[0],
            'color10': high_intensity_colors1[1],
            'color11': high_intensity_colors1[2],
            'color12': high_intensity_colors1[3],
            'color13': high_intensity_colors1[4],
            'color14': high_intensity_colors1[5],
            'color15': self.extracted_colors_dict['light white']
        }

        palettes = {light_palette_name: light_palette, dark_palette_name: dark_palette}

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
            'orange': self.extracted_colors_dict['orange'],
            'yellow': self.extracted_colors_dict['yellow'],
            'chartreuse': self.extracted_colors_dict['chartreuse'],
            'green': self.extracted_colors_dict['green'],
            'spring': self.extracted_colors_dict['spring'],
            'cyan': self.extracted_colors_dict['cyan'],
            'azure': self.extracted_colors_dict['azure'],
            'blue': self.extracted_colors_dict['blue'],
            'violet': self.extracted_colors_dict['violet'],
            'magenta': self.extracted_colors_dict['magenta'],
            'rose': self.extracted_colors_dict['rose'],
            'white': self.extracted_colors_dict['white'],
            'light black': self.extracted_colors_dict['light black'],
            'light red': self.extracted_colors_dict['light red'],
            'light orange': self.extracted_colors_dict['light orange'],
            'light yellow': self.extracted_colors_dict['light yellow'],
            'light chartreuse': self.extracted_colors_dict['light chartreuse'],
            'light green': self.extracted_colors_dict['light green'],
            'light spring': self.extracted_colors_dict['light spring'],
            'light cyan': self.extracted_colors_dict['light cyan'],
            'light azure': self.extracted_colors_dict['light azure'],
            'light blue': self.extracted_colors_dict['light blue'],
            'light violet': self.extracted_colors_dict['light violet'],
            'light magenta': self.extracted_colors_dict['light magenta'],
            'light rose': self.extracted_colors_dict['light rose'],
            'light white': self.extracted_colors_dict['light white'],
            'dark black': self.extracted_colors_dict['dark black'],
            'dark red': self.extracted_colors_dict['dark red'],
            'dark orange': self.extracted_colors_dict['dark orange'],
            'dark yellow': self.extracted_colors_dict['dark yellow'],
            'dark chartreuse': self.extracted_colors_dict['dark chartreuse'],
            'dark green': self.extracted_colors_dict['dark green'],
            'dark spring': self.extracted_colors_dict['dark spring'],
            'dark cyan': self.extracted_colors_dict['dark cyan'],
            'dark azure': self.extracted_colors_dict['dark azure'],
            'dark blue': self.extracted_colors_dict['dark blue'],
            'dark violet': self.extracted_colors_dict['dark violet'],
            'dark magenta': self.extracted_colors_dict['dark magenta'],
            'dark rose': self.extracted_colors_dict['dark rose'],
            'dark white': self.extracted_colors_dict['dark white']
        }

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Converts light color type to pastel.
    #
    #   @param  self    The object pointer.
    def convert_pastel_light(self):
        self.convert_pastel(self.extracted_colors_dict['light red'])
        self.convert_pastel(self.extracted_colors_dict['light orange'])
        self.convert_pastel(self.extracted_colors_dict['light yellow'])
        self.convert_pastel(self.extracted_colors_dict['light chartreuse'])
        self.convert_pastel(self.extracted_colors_dict['light green'])
        self.convert_pastel(self.extracted_colors_dict['light spring'])
        self.convert_pastel(self.extracted_colors_dict['light cyan'])
        self.convert_pastel(self.extracted_colors_dict['light azure'])
        self.convert_pastel(self.extracted_colors_dict['light blue'])
        self.convert_pastel(self.extracted_colors_dict['light violet'])
        self.convert_pastel(self.extracted_colors_dict['light magenta'])
        self.convert_pastel(self.extracted_colors_dict['light rose'])

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Converts normal color type to pastel.
    #
    #   @param  self    The object pointer.
    def convert_pastel_normal(self):
        self.convert_pastel(self.extracted_colors_dict['red'])
        self.convert_pastel(self.extracted_colors_dict['orange'])
        self.convert_pastel(self.extracted_colors_dict['yellow'])
        self.convert_pastel(self.extracted_colors_dict['chartreuse'])
        self.convert_pastel(self.extracted_colors_dict['green'])
        self.convert_pastel(self.extracted_colors_dict['spring'])
        self.convert_pastel(self.extracted_colors_dict['cyan'])
        self.convert_pastel(self.extracted_colors_dict['azure'])
        self.convert_pastel(self.extracted_colors_dict['blue'])
        self.convert_pastel(self.extracted_colors_dict['violet'])
        self.convert_pastel(self.extracted_colors_dict['magenta'])
        self.convert_pastel(self.extracted_colors_dict['rose'])

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Converts dark color type to pastel.
    #
    #   @param  self    The object pointer.
    def convert_pastel_dark(self):
        self.convert_pastel(self.extracted_colors_dict['dark red'])
        self.convert_pastel(self.extracted_colors_dict['dark orange'])
        self.convert_pastel(self.extracted_colors_dict['dark yellow'])
        self.convert_pastel(self.extracted_colors_dict['dark chartreuse'])
        self.convert_pastel(self.extracted_colors_dict['dark green'])
        self.convert_pastel(self.extracted_colors_dict['dark spring'])
        self.convert_pastel(self.extracted_colors_dict['dark cyan'])
        self.convert_pastel(self.extracted_colors_dict['dark azure'])
        self.convert_pastel(self.extracted_colors_dict['dark blue'])
        self.convert_pastel(self.extracted_colors_dict['dark violet'])
        self.convert_pastel(self.extracted_colors_dict['dark magenta'])
        self.convert_pastel(self.extracted_colors_dict['dark rose'])

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Generates a default set of palettes from the extracted colors.
    #
    #   @param  self    The object pointer.
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

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Retrieves a list of 3 color types.
    #   @details    The color types are chosen by using a
    #               color pair and the name of a dominant color.
    #
    #   @param  self                The object pointer.
    #   @param  color_name1         A string that represents the base name of a color.
    #   @param  color_name2         A string that represents the base name of a color.
    #   @param  dom_color_name      A string that represents the base name of the dominant color in the image.
    #
    #   @return A list of 3 color types.
    def get_goldilocks_colorset(self, color_name1, color_name2, dom_color_name):
        norm_color, light_color, dark_color = [], [], []

        norm_color = self.get_closest_to_goldilocks(color_name1, color_name2, dom_color_name)
        light_color = self.get_closest_to_goldilocks(color_name1, color_name2, dom_color_name, color_type='light')
        dark_color = self.get_closest_to_goldilocks(color_name1, color_name2, dom_color_name, color_type='dark')

        return [norm_color, light_color, dark_color]

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Gets the index of a base color as it would appear in a linear cyclical array.
    #
    #   @note   For example of colors on color a wheel being shown in linear cyclical
    #           format, please refer to the internal code comment block for this function.
    #
    #   @internal
    #   Example of colors on color a wheel being shown in linear cyclical format:
    #   ___________________________________________________________
    #   || (Left side).............................(Right side)  ||
    #   || ------⦧------⦧--------⦧---------⦧----------⦧------  ||
    #   || |...red...orange...yellow...chartreuse...green....|  ||
    #   || -----⦧--------⦧-------⦧------⦧------⦧--------⦧---- ||
    #   || |.violet...magenta...rose...red...orange...yellow.| ||
    #   ---------------------------------------------------------
    #   @endinternal
    #
    #   @param  self        The object pointer.
    #   @param  color_name  A string that represents the base name of a color.
    #
    #   @return Integer value that represents the index of a base color in a cyclical array.
    def get_color_index(self, color_name):
        # Linear representation of the colors in a cyclical array.
        # ['red', 'orange', 'yellow', 'chartreuse', 'green', 'spring', 'cyan', 'azure', 'blue', 'violet', 'magenta', 'rose']
        if color_name == 'orange':
            return 1
        elif color_name == 'yellow':
            return 2
        elif color_name == 'chartreuse':
            return 3
        elif color_name == 'green':
            return 4
        elif color_name == 'spring':
            return 5
        elif color_name == 'cyan':
            return 6
        elif color_name == 'azure':
            return 7
        elif color_name == 'blue':
            return 8
        elif color_name == 'violet':
            return 9
        elif color_name == 'magenta':
            return 10
        elif color_name == 'rose':
            return 11

        return 0    # Red is the default index, 0.

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Gets the color code index of a base color as it would appear in a color palette.
    #   @details    A color code is the NAME of a color as it appears in
    #               terminal / CLI color palettes (i.e. color0, color1,
    #               color2, ... , color15). A color code index is the index
    #               of said color where it would appear in a color palette.
    #
    #   @note   For more information about these ANSI escape codes,
    #           here are some sources:
    #           https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
    #           https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences/33206814#33206814
    #           https://stackoverflow.com/questions/45782766/color-python-output-given-rrggbb-hex-value/45782972#45782972
    #
    #   @param  self        The object pointer.
    #   @param  color_name  A string that represents the base name of a color.
    #
    #   @return Integer value that represents the index of a color code in a palette.
    def get_color_code_index(self, color_name):
        # The standard 6 colors occupy indices [1, 6] in a color
        # palette. But since we are excluding black and white
        # colors, which occupy indices 0 and 7, we can shift our
        # thinking to imagine the standard 6 colors to occupy
        # indices [0, 5].
        # [red, green, yellow, blue, magenta, cyan]
        # An additional 6 standard colors occupy the same index locations.
        # [rose, chartreuse, orange, azure, violet, spring]
        if color_name == 'orange' or color_name == 'yellow':
            return 2
        elif color_name == 'chartreuse' or color_name == 'green':
            return 1
        elif color_name == 'spring' or color_name == 'cyan':
            return 5
        elif color_name == 'azure' or color_name == 'blue':
            return 3
        elif color_name == 'violet' or color_name == 'magenta':
            return 4

        return 0    # Red or Rose is the default color code index, 0.

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

        hsv_color[1] = new_sat_bounds[0] + (
                ((hsv_color[1] - old_sat_bounds[0]) / (old_sat_bounds[1] - old_sat_bounds[0]))
                * (new_sat_bounds[1] - new_sat_bounds[0]))

        hsv_color[2] = new_bright_bounds[0] + (
                ((hsv_color[2] - old_bright_bounds[0]) / (old_bright_bounds[1] - old_bright_bounds[0]))
                * (new_bright_bounds[1] - new_bright_bounds[0]))

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    def get_closest_to_goldilocks(self, color_name1, color_name2, dom_color_name, color_type=''):
        spacing = '' if color_type == '' else ' '
        ratio_color_type = 'norm' if color_type == '' else color_type

        color1 = self.extracted_colors_dict[color_type + spacing + color_name1]
        color2 = self.extracted_colors_dict[color_type + spacing + color_name2]
        dom_color = self.extracted_colors_dict[color_type + spacing + dom_color_name]

        # Calculate distances between each of the colors and the dominant color.
        color1_dist = exutil.calculate_dist_between_2_colors(color1, dom_color)
        color2_dist = exutil.calculate_dist_between_2_colors(color2, dom_color)

        # Determine if we can identify which color to return based on the base color ratios.
        if self.ratio_dict[color_name1] != 0 and self.ratio_dict[color_name2] == 0:
            return color1
        elif self.ratio_dict[color_name1] == 0 and self.ratio_dict[color_name2] != 0:
            return color2
        elif self.ratio_dict[color_name1] == 0 and self.ratio_dict[color_name2] == 0:
            # if both ratios happen to be zero, try selecting based on distance.
            if color1_dist < color2_dist:
                return color1
            elif color2_dist < color1_dist:
                return color2

        # Explanation of what my thought process is
        # for the selection process below:
        # ---------------------------------------------------------------
        # Use the TYPE ratio to get a percentage of the WHOLE ratio,
        # then use that to get a ratioed (dampened) distance.
        # EX : Red = 53.258%, Light Red = 23.523%
        # using the Light Red type ratio, we are gonna get a percentage of the WHOLE ratio.
        # Red * (Light Red / 100.0) =
        # 53.258 * (23.523 / 100.0) =
        # 53.258 * .23523 = 12.52787934 %
        #
        # Then we use this new percentage on the distance :
        # ratioed_dist = color_dist / 12.52787934
        #
        # This should produce ideal and consistent results.

        color1_ratio_percentage, color2_ratio_percentage = float("inf"), float("inf")
        color1_dampened_dist, color2_dampened_dist = float("inf"), float("inf")
        color1_whole_dampened_dist, color2_whole_dampened_dist = float("inf"), float("inf")

        # Use the ratio of each color type to get a percentage from the whole ratio of a base color.
        # color_ratio_percentage = whole_ratio * (type_ratio / 100.0)
        if self.ratio_dict[ratio_color_type + ' ' + color_name1] > 0.0:
            color1_ratio_percentage = self.ratio_dict[color_name1] * (self.ratio_dict[ratio_color_type + ' ' + color_name1] / 100.0)
        if self.ratio_dict[ratio_color_type + ' ' + color_name2] > 0.0:
            color2_ratio_percentage = self.ratio_dict[color_name2] * (self.ratio_dict[ratio_color_type + ' ' + color_name2] / 100.0)

        # Use a percentage of a color ratio to affect and dampen the original calculated distance.
        if color1_ratio_percentage != float("inf"):
            color1_dampened_dist = color1_dist / color1_ratio_percentage
        if color2_ratio_percentage != float("inf"):
            color2_dampened_dist = color2_dist / color2_ratio_percentage

        # Use the WHOLE color ratio to affect and dampen the original calculated distance.
        if self.ratio_dict[color_name1] > 0:
            color1_whole_dampened_dist = color1_dist / self.ratio_dict[color_name1]
        if self.ratio_dict[color_name2] > 0:
            color2_whole_dampened_dist = color2_dist / self.ratio_dict[color_name2]

        # THIS IS THE PREFERRED METHOD OF IDENTIFYING THE IDEAL COLOR FOR NOW!!!
        if color1_dampened_dist < color2_dampened_dist:
            return color1
        elif color1_dampened_dist > color2_dampened_dist:
            return color2
        elif color1_whole_dampened_dist < color2_whole_dampened_dist:
            return color1
        elif color1_whole_dampened_dist > color2_whole_dampened_dist:
            return color2
        else:
            # If both ratios aren't zero but the ratioed values are the same,
            # try selecting based on distance.
            if color1_dist < color2_dist:
                return color1
            elif color2_dist < color1_dist:
                return color2

        # As a failsafe, use the average of both colors if the selection
        # process fails with both dampened-distance and distance values.
        cos_color1_hue = math.cos(math.radians(color1[0]))
        cos_color2_hue = math.cos(math.radians(color2[0]))
        cos_hue_types = [cos_color1_hue, cos_color2_hue]

        sin_color1_hue = math.sin(math.radians(color1[0]))
        sin_color2_hue = math.sin(math.radians(color2[0]))
        sin_hue_types = [sin_color1_hue, sin_color2_hue]

        average_hue = math.atan2(stats.mean(sin_hue_types), stats.mean(cos_hue_types))
        average_hue = round(math.degrees(average_hue)) % 360

        average_sat = (color1[1] + color2[1]) / 2.0
        average_bright = (color1[2] + color2[2]) / 2.0

        avg_color = [average_hue, average_sat, average_bright]

        return avg_color

    # **************************************************************************
    # ********************* GLOBAL VARIABLE DOCUMENTATION **********************
    # **************************************************************************

    ##  @var    hsv_img_matrix_2d
    #   A 2D numpy array of pixels from an image in [h,s,v] format.
    ##  @var    image_name
    #   The name of the image file, without any extension (e.g. .jpg, .png, etc.).
    ##  @var    color_format
    #   A string that represents the format each color should have (e.g. 'hsv', 'rgb', 'hex', 'ansi').
    ##  @var    ratio_dict
    #   A dictionary that holds the ratio of base colors in an image and is
    #   used to identify the dominant color in an image.
    ##  @var    base_color_dict
    #   A dictionary of 2D numpy arrays for each of the 6 base colors.
    ##  @var    extracted_colors_dict
    #   A dictionary of extracted colors in [h,s,v] format.
