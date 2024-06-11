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
    #   @param  pastel_light        Flag to convert light color palette to pastel.
    #   @param  pastel_normal       Flag to convert normal color palette to pastel.
    #   @param  pastel_dark         Flag to convert dark color palette to pastel.
    def __init__(self, hsv_img_matrix_2d, output_filepath, pastel_light=False, pastel_normal=False, pastel_dark=False):
        self.hsv_img_matrix_2d = hsv_img_matrix_2d
        self.output_filepath = output_filepath
        self.pastel_light = pastel_light
        self.pastel_normal = pastel_normal
        self.pastel_dark = pastel_dark
        self.ratio_dict = {}
        self.base_color_dict = {}
        self.extracted_colors_dict = {}
        self.palette_dict = {}

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
        self.extracted_colors_dict = exutil.extract_color_palettes(self.base_color_dict)
        exutil.check_missing_colors(self.base_color_dict, self.extracted_colors_dict)
        exutil.generate_remaining_colors(self.extracted_colors_dict, self.ratio_dict)

        # Check for pastel option(s).
        self.check_pastel_conversion()

        # Construct a basic palette dictionary.
        self.construct_palette_dictionary()

    # **************************************************************************
    # **************************************************************************

    ##  Checks to see if any of the palettes should be converted to pastel.
    #
    #   @param  self    The object pointer.
    def check_pastel_conversion(self):
        if self.pastel_light:
            self.convert_pastel_light()

        if self.pastel_normal:
            self.convert_pastel_normal()

        if self.pastel_dark:
            self.convert_pastel_dark()

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Constructs a dictionary of all the extracted color palettes in hex format.
    #   @details    The extracted color palettes are organized in
    #               the dictionary as follows: light background,
    #               light foreground, dark background, dark foreground,
    #               light palette, normal palette, dark palette.
    #
    #   @param  self    The object pointer.
    def construct_palette_dictionary(self):
        self.palette_dict = {
            'light background': convert.hsv_to_hex(self.extracted_colors_dict['Light Background']),
            'light foreground': convert.hsv_to_hex(self.extracted_colors_dict['Light Foreground']),
            'dark background': convert.hsv_to_hex(self.extracted_colors_dict['Dark Background']),
            'dark foreground': convert.hsv_to_hex(self.extracted_colors_dict['Dark Foreground']),
            'light black': convert.hsv_to_hex(self.extracted_colors_dict['Light Black']),
            'light red': convert.hsv_to_hex(self.extracted_colors_dict['Light Red']),
            'light green': convert.hsv_to_hex(self.extracted_colors_dict['Light Green']),
            'light yellow': convert.hsv_to_hex(self.extracted_colors_dict['Light Yellow']),
            'light blue': convert.hsv_to_hex(self.extracted_colors_dict['Light Blue']),
            'light magenta': convert.hsv_to_hex(self.extracted_colors_dict['Light Magenta']),
            'light cyan': convert.hsv_to_hex(self.extracted_colors_dict['Light Cyan']),
            'light white': convert.hsv_to_hex(self.extracted_colors_dict['Light White']),
            'normal black': convert.hsv_to_hex(self.extracted_colors_dict['Normal Black']),
            'normal red': convert.hsv_to_hex(self.extracted_colors_dict['Normal Red']),
            'normal green': convert.hsv_to_hex(self.extracted_colors_dict['Normal Green']),
            'normal yellow': convert.hsv_to_hex(self.extracted_colors_dict['Normal Yellow']),
            'normal blue': convert.hsv_to_hex(self.extracted_colors_dict['Normal Blue']),
            'normal magenta': convert.hsv_to_hex(self.extracted_colors_dict['Normal Magenta']),
            'normal cyan': convert.hsv_to_hex(self.extracted_colors_dict['Normal Cyan']),
            'normal white': convert.hsv_to_hex(self.extracted_colors_dict['Normal White']),
            'dark black': convert.hsv_to_hex(self.extracted_colors_dict['Dark Black']),
            'dark red': convert.hsv_to_hex(self.extracted_colors_dict['Dark Red']),
            'dark green': convert.hsv_to_hex(self.extracted_colors_dict['Dark Green']),
            'dark yellow': convert.hsv_to_hex(self.extracted_colors_dict['Dark Yellow']),
            'dark blue': convert.hsv_to_hex(self.extracted_colors_dict['Dark Blue']),
            'dark magenta': convert.hsv_to_hex(self.extracted_colors_dict['Dark Magenta']),
            'dark cyan': convert.hsv_to_hex(self.extracted_colors_dict['Dark Cyan']),
            'dark white': convert.hsv_to_hex(self.extracted_colors_dict['Dark White']),
        }

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    ##  Constructs a dictionary of color schemes by combining color palettes.
    #   @details    Light color scheme contains the normal and dark
    #               color palettes. Dark color scheme contains the
    #               normal and light color palettes.
    #
    #   @param  self    The object pointer.
    #
    #   @return A dictionary of light and dark color schemes.
    def construct_scheme_dictionary(self):
        light_scheme = {
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

        dark_scheme = {
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

        color_schemes_dict = {
            'light': light_scheme,
            'dark': dark_scheme
        }

        return color_schemes_dict

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
    ##  @var    output_filepath
    #   Output file path with filename of where to store color palette.
    ##  @var    pastel_light
    #   Flag to convert light color palette to pastel.
    ##  @var    pastel_normal
    #   Flag to convert normal color palette to pastel.
    ##  @var    pastel_dark
    #   Flag to convert dark color palette to pastel.
    ##  @var    ratio_dict
    #   A dictionary that holds the ratio of base colors in an image and is
    #   used to identify the dominant color in an image.
    ##  @var    base_color_dict
    #   A dictionary of 2D numpy arrays for each of the 6 base colors.
    ##  @var    extracted_colors_dict
    #   A dictionary of extracted colors in [h,s,v] format.
    ##  @var    palette_dict
    #   A dictionary of light, normal, and dark color palettes in hex format.
