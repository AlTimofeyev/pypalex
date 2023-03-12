##  @file   Extractor.py
#   @brief  Extraction utility class for extracting colors from the image.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on February 10, 2022.
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 6, 2023.


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
    #   @param  output_filepath     Output file path with filename of where to store color palette.
    #   @param  pastel              Flag to convert all extracted color types to pastel.
    #   @param  pastel_light        Flag to convert light colors to pastel.
    #   @param  pastel_normal       Flag to convert normal colors to pastel.
    #   @param  pastel_dark         Flag to convert dark colors to pastel.
    def __init__(self, hsv_img_matrix_2d, output_filepath, pastel=False, pastel_light=False, pastel_normal=False, pastel_dark=False):
        self.hsv_img_matrix_2d = hsv_img_matrix_2d
        self.output_filepath = output_filepath
        self.pastel = pastel
        self.pastel_light = pastel_light
        self.pastel_normal = pastel_normal
        self.pastel_dark = pastel_dark
        self.ratio_dict = {}
        self.base_color_dict = {}
        self.extracted_colors_dict = {}
        self.color_palette_dict = {}

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

        # Check for pastel option(s).
        self.check_pastel_conversion()

        # Construct palette dictionary.
        self.construct_palette_dictionary()

    # **************************************************************************
    # **************************************************************************

    ##  Checks to see if any of the palettes should be converted to pastel.
    #
    #   @param  self    The object pointer.
    def check_pastel_conversion(self):
        if self.pastel:
            self.convert_pastel_light()
            self.convert_pastel_normal()
            self.convert_pastel_dark()
            return

        if self.pastel_light:
            self.convert_pastel_light()

        if self.pastel_normal:
            self.convert_pastel_normal()

        if self.pastel_dark:
            self.convert_pastel_dark()

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Constructs color palette dictionary.
    #
    #   @param  self    The object pointer.
    def construct_palette_dictionary(self):
        light_palette = {
            'background': convert.hsv_to_hex(self.extracted_colors_dict['Light Background']),
            'foreground': convert.hsv_to_hex(self.extracted_colors_dict['Dark Foreground']),
            'black': convert.hsv_to_hex(self.extracted_colors_dict['Normal Black']),
            'red': convert.hsv_to_hex(self.extracted_colors_dict['Normal Red']),
            'green': convert.hsv_to_hex(self.extracted_colors_dict['Normal Green']),
            'yellow': convert.hsv_to_hex(self.extracted_colors_dict['Normal Yellow']),
            'blue': convert.hsv_to_hex(self.extracted_colors_dict['Normal Blue']),
            'magenta': convert.hsv_to_hex(self.extracted_colors_dict['Normal Magenta']),
            'cyan': convert.hsv_to_hex(self.extracted_colors_dict['Normal Cyan']),
            'white': convert.hsv_to_hex(self.extracted_colors_dict['Normal White']),
            'bright black': convert.hsv_to_hex(self.extracted_colors_dict['Dark Black']),
            'bright red': convert.hsv_to_hex(self.extracted_colors_dict['Dark Red']),
            'bright green': convert.hsv_to_hex(self.extracted_colors_dict['Dark Green']),
            'bright yellow': convert.hsv_to_hex(self.extracted_colors_dict['Dark Yellow']),
            'bright blue': convert.hsv_to_hex(self.extracted_colors_dict['Dark Blue']),
            'bright magenta': convert.hsv_to_hex(self.extracted_colors_dict['Dark Magenta']),
            'bright cyan': convert.hsv_to_hex(self.extracted_colors_dict['Dark Cyan']),
            'bright white': convert.hsv_to_hex(self.extracted_colors_dict['Dark White'])
        }

        dark_palette = {
            'background': convert.hsv_to_hex(self.extracted_colors_dict['Dark Background']),
            'foreground': convert.hsv_to_hex(self.extracted_colors_dict['Light Foreground']),
            'black': convert.hsv_to_hex(self.extracted_colors_dict['Normal Black']),
            'red': convert.hsv_to_hex(self.extracted_colors_dict['Normal Red']),
            'green': convert.hsv_to_hex(self.extracted_colors_dict['Normal Green']),
            'yellow': convert.hsv_to_hex(self.extracted_colors_dict['Normal Yellow']),
            'blue': convert.hsv_to_hex(self.extracted_colors_dict['Normal Blue']),
            'magenta': convert.hsv_to_hex(self.extracted_colors_dict['Normal Magenta']),
            'cyan': convert.hsv_to_hex(self.extracted_colors_dict['Normal Cyan']),
            'white': convert.hsv_to_hex(self.extracted_colors_dict['Normal White']),
            'bright black': convert.hsv_to_hex(self.extracted_colors_dict['Light Black']),
            'bright red': convert.hsv_to_hex(self.extracted_colors_dict['Light Red']),
            'bright green': convert.hsv_to_hex(self.extracted_colors_dict['Light Green']),
            'bright yellow': convert.hsv_to_hex(self.extracted_colors_dict['Light Yellow']),
            'bright blue': convert.hsv_to_hex(self.extracted_colors_dict['Light Blue']),
            'bright magenta': convert.hsv_to_hex(self.extracted_colors_dict['Light Magenta']),
            'bright cyan': convert.hsv_to_hex(self.extracted_colors_dict['Light Cyan']),
            'bright white': convert.hsv_to_hex(self.extracted_colors_dict['Light White'])
        }

        self.color_palette_dict['light'] = light_palette
        self.color_palette_dict['dark'] = dark_palette

    # **************************************************************************
    # **************************************************************************

    ##  Converts light palette to pastel.
    #
    #   @param  self    The object pointer.
    def convert_pastel_light(self):
        self.convert_pastel(self.extracted_colors_dict['Light Red'])
        self.convert_pastel(self.extracted_colors_dict['Light Yellow'])
        self.convert_pastel(self.extracted_colors_dict['Light Green'])
        self.convert_pastel(self.extracted_colors_dict['Light Cyan'])
        self.convert_pastel(self.extracted_colors_dict['Light Blue'])
        self.convert_pastel(self.extracted_colors_dict['Light Magenta'])

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Converts normal palette to pastel.
    #
    #   @param  self    The object pointer.
    def convert_pastel_normal(self):
        self.convert_pastel(self.extracted_colors_dict['Normal Red'])
        self.convert_pastel(self.extracted_colors_dict['Normal Yellow'])
        self.convert_pastel(self.extracted_colors_dict['Normal Green'])
        self.convert_pastel(self.extracted_colors_dict['Normal Cyan'])
        self.convert_pastel(self.extracted_colors_dict['Normal Blue'])
        self.convert_pastel(self.extracted_colors_dict['Normal Magenta'])

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Converts dark palette to pastel.
    #
    #   @param  self    The object pointer.
    def convert_pastel_dark(self):
        self.convert_pastel(self.extracted_colors_dict['Dark Red'])
        self.convert_pastel(self.extracted_colors_dict['Dark Yellow'])
        self.convert_pastel(self.extracted_colors_dict['Dark Green'])
        self.convert_pastel(self.extracted_colors_dict['Dark Cyan'])
        self.convert_pastel(self.extracted_colors_dict['Dark Blue'])
        self.convert_pastel(self.extracted_colors_dict['Dark Magenta'])

    # **************************************************************************
    # **************************************************************************

    ##  Converts/normalizes HSV color to pastel.
    #   @details    For values x in range [a, b], values x can be converted
    #               to the new range [y, z] with the following equation:
    #               new_x = (z-y) * ((x-a) / (b-a)) + y
    #
    #   @param  self        The object pointer.
    #   @param  hsv_color   List HSV color to be converted to pastel.
    def convert_pastel(self, hsv_color):
        # Define the old and new ranges.
        old_sat, new_sat = const.SATURATION_RANGE, const.PASTEL_SATURATION_RANGE
        old_sat_range = old_sat[1] - old_sat[0]
        new_sat_range = new_sat[1] - new_sat[0]

        old_brightness, new_brightness = const.BRIGHTNESS_RANGE, const.PASTEL_BRIGHTNESS_RANGE
        old_bright_range = old_brightness[1] - old_brightness[0]
        new_bright_range = new_brightness[1] - new_brightness[0]

        # Convert saturation and brightness to pastel range.
        hsv_color[1] = new_sat_range * ((hsv_color[1] - old_sat[0]) / old_sat_range) + new_sat[0]
        hsv_color[2] = new_bright_range * ((hsv_color[2] - old_brightness[0]) / old_bright_range) + new_brightness[0]

    # **************************************************************************
    # ********************* GLOBAL VARIABLE DOCUMENTATION **********************
    # **************************************************************************

    ##  @var    hsv_img_matrix_2d
    #   A 2D numpy array of pixels from an image in [h,s,v] format.
    ##  @var    output_filepath
    #   Output file path with filename of where to store color palette.
    ##  @var    pastel
    #   Flag to convert all extracted color types to pastel.
    ##  @var    pastel_light
    #   Flag to convert light colors to pastel.
    ##  @var    pastel_normal
    #   Flag to convert normal colors to pastel.
    ##  @var    pastel_dark
    #   Flag to convert dark colors to pastel.
    ##  @var    ratio_dict
    #   A dictionary that holds the ratio of base colors in an image and is
    #   used to identify the dominant color in an image.
    ##  @var    base_color_dict
    #   A dictionary of 2D numpy arrays for each of the 6 base colors.
    ##  @var    extracted_colors_dict
    #   A Dictionary of extracted colors in [h,s,v] format.
    ##  @var    color_palette_dict
    #   A Dictionary of dictionaries for light and dark color schemes
    #   that are in HEX string format.
