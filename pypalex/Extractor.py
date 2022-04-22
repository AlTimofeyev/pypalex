"""!
#######################################################################
@author Al Timofeyev
@date   February 10, 2022
@brief  Extraction utility class for extracting colors from the image.
#######################################################################
"""

# ---- IMPORTS ----
import numpy
from . import extraction_utils as exutil
from . import conversion_utils as convert


class Extractor:
    """! Extracts colors using ONLY the colors in the image. """

    # ---- CONSTRUCTOR ----
    def __init__(self, full_hsl_img_array, output_path, pastel=False, pastel_light=False, pastel_normal=False, pastel_dark=False):
        """!
        @brief  Extractor Constructor.
        @param  self    The object pointer.
        @param  full_hsl_img_array  A 2D numpy array of all the pixels from image, in hsl format.
        @param  output_path Output path and filename of where to store color palette.
        @param  pastel          Flag to convert all extracted color palettes to pastel.
        @param  pastel_light    Flag to convert light palette to pastel.
        @param  pastel_normal   Flag to convert normal palette to pastel.
        @param  pastel_dark     Flag to convert dark palette to pastel.
        """
        self.ratio_dict: dict[str, float] = {}
        self.base_color_dict: dict[str, numpy.ndarray] = {}
        self.dom_color_dict: dict[str, list] = {}
        self.color_palette_dict: dict[str, dict[str, str]] = {}
        ## Output path and filename of where to store color palette.
        self.output_path = output_path
        ## A 2D numpy array of all the pixels from image, in hsl format.
        self.full_hsl_img_array = full_hsl_img_array
        self.pastel = pastel
        self.pastel_light = pastel_light
        self.pastel_normal = pastel_normal
        self.pastel_dark = pastel_dark

    # ---- MAIN ----
    def run(self):
        """!
        @brief  Performs extraction of colors.
        @param  self    The object pointer.
        """
        # Organize colors.
        self.ratio_dict = exutil.extract_ratios(self.full_hsl_img_array)
        self.base_color_dict = exutil.construct_base_color_dictionary(self.full_hsl_img_array)
        exutil.check_missing_colors(self.base_color_dict)

        # Extract colors.
        self.dom_color_dict = exutil.extract_dominant_colors(self.base_color_dict)
        exutil.generate_remaining_colors(self.dom_color_dict, self.ratio_dict)

        # Check for pastel option(s).
        self.check_pastel_conversion()

        # Construct palette dictionary.
        self.construct_palette_dictionary()

    # ***********************************************************************
    # ***********************************************************************

    def construct_palette_dictionary(self):
        """!
        @brief  Constructs color palette dictionary.
        @param  self    The object pointer.
        """
        light_palette: dict[str, str] = {}
        normal_palette: dict[str, str] = {}
        dark_palette: dict[str, str] = {}

        light_palette['background'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Background']))
        light_palette['foreground'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Foreground']))
        light_palette['black'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Black']))
        light_palette['red'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Red']))
        light_palette['green'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Green']))
        light_palette['yellow'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Yellow']))
        light_palette['blue'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Blue']))
        light_palette['magenta'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Magenta']))
        light_palette['cyan'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Cyan']))
        light_palette['white'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal White']))
        light_palette['bright black'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Black']))
        light_palette['bright red'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Red']))
        light_palette['bright green'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Green']))
        light_palette['bright yellow'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Yellow']))
        light_palette['bright blue'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Blue']))
        light_palette['bright magenta'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Magenta']))
        light_palette['bright cyan'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Cyan']))
        light_palette['bright white'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark White']))

        normal_palette['background'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Background']))
        normal_palette['foreground'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Foreground']))
        normal_palette['black'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Black']))
        normal_palette['red'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Red']))
        normal_palette['green'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Green']))
        normal_palette['yellow'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Yellow']))
        normal_palette['blue'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Blue']))
        normal_palette['magenta'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Magenta']))
        normal_palette['cyan'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Cyan']))
        normal_palette['white'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark White']))
        normal_palette['bright black'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Black']))
        normal_palette['bright red'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Red']))
        normal_palette['bright green'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Green']))
        normal_palette['bright yellow'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Yellow']))
        normal_palette['bright blue'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Blue']))
        normal_palette['bright magenta'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Magenta']))
        normal_palette['bright cyan'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Cyan']))
        normal_palette['bright white'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light White']))

        dark_palette['background'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Background']))
        dark_palette['foreground'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Dark Foreground']))
        dark_palette['black'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Black']))
        dark_palette['red'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Red']))
        dark_palette['green'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Green']))
        dark_palette['yellow'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Yellow']))
        dark_palette['blue'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Blue']))
        dark_palette['magenta'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Magenta']))
        dark_palette['cyan'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal Cyan']))
        dark_palette['white'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Normal White']))
        dark_palette['bright black'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Black']))
        dark_palette['bright red'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Red']))
        dark_palette['bright green'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Green']))
        dark_palette['bright yellow'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Yellow']))
        dark_palette['bright blue'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Blue']))
        dark_palette['bright magenta'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Magenta']))
        dark_palette['bright cyan'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light Cyan']))
        dark_palette['bright white'] = convert.rgb_to_hex(convert.hsl_to_rgb(self.dom_color_dict['Light White']))

        self.color_palette_dict['light'] = light_palette
        self.color_palette_dict['normal'] = normal_palette
        self.color_palette_dict['dark'] = dark_palette

    # ***********************************************************************
    # ***********************************************************************

    def check_pastel_conversion(self):
        """!
        @brief  Checks to see if any of the palettes should be converted to pastel.
        @param  self    The object pointer.
        """
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

    # ***********************************************************************
    # ***********************************************************************

    def convert_pastel(self, hsl_color):
        """!
        @brief  Converts/normalizes hsl color to pastel.
        @details    For values x in range [a, b], values x can be converted
                    to the new range [y, z] with the following equation:
                    new_x = (z-y) * ((x-min_x) / (max_x-min_x)) + y
                    where a = min_x and b = max_x from the old range.
        @param  self        The object pointer.
        @param  hsl_color   HSL color to be converted to pastel.
        """
        # Define the old and new ranges.
        old_sat_range = [5, 100]    # This range is from "check_sat_and_light()" in extraction_utils.
        new_sat_range = [15, 35]
        old_lit_range = [15, 90]    # This range is from "check_sat_and_light()" in extraction_utils.
        new_lit_range = [30, 80]

        # Convert saturation to pastel range.
        hsl_color[1] = (new_sat_range[1] - new_sat_range[0]) * (
                (hsl_color[1] - old_sat_range[0]) / (old_sat_range[1] - old_sat_range[0])) + new_sat_range[0]

        # Convert lightness to pastel range.
        hsl_color[2] = (new_lit_range[1] - new_lit_range[0]) * (
                (hsl_color[2] - old_lit_range[0]) / (old_lit_range[1] - old_lit_range[0])) + new_lit_range[0]

    # ---------------------------------------------------------------
    # ---------------------------------------------------------------

    def convert_pastel_light(self):
        """!
        @brief  Converts light palette to pastel.
        @param  self    The object pointer.
        """
        self.convert_pastel(self.dom_color_dict['Light Red'])
        self.convert_pastel(self.dom_color_dict['Light Yellow'])
        self.convert_pastel(self.dom_color_dict['Light Green'])
        self.convert_pastel(self.dom_color_dict['Light Cyan'])
        self.convert_pastel(self.dom_color_dict['Light Blue'])
        self.convert_pastel(self.dom_color_dict['Light Magenta'])

    # ---------------------------------------------------------------
    # ---------------------------------------------------------------

    def convert_pastel_normal(self):
        """!
        @brief  Converts normal palette to pastel.
        @param  self    The object pointer.
        """
        self.convert_pastel(self.dom_color_dict['Normal Red'])
        self.convert_pastel(self.dom_color_dict['Normal Yellow'])
        self.convert_pastel(self.dom_color_dict['Normal Green'])
        self.convert_pastel(self.dom_color_dict['Normal Cyan'])
        self.convert_pastel(self.dom_color_dict['Normal Blue'])
        self.convert_pastel(self.dom_color_dict['Normal Magenta'])

    # ---------------------------------------------------------------
    # ---------------------------------------------------------------

    def convert_pastel_dark(self):
        """!
        @brief  Converts dark palette to pastel.
        @param  self    The object pointer.
        """
        self.convert_pastel(self.dom_color_dict['Dark Red'])
        self.convert_pastel(self.dom_color_dict['Dark Yellow'])
        self.convert_pastel(self.dom_color_dict['Dark Green'])
        self.convert_pastel(self.dom_color_dict['Dark Cyan'])
        self.convert_pastel(self.dom_color_dict['Dark Blue'])
        self.convert_pastel(self.dom_color_dict['Dark Magenta'])
