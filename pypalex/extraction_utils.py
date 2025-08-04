##  @file   extraction_utils.py
#   @brief  Utilities for extracting colors from the image.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on February 10, 2022.
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 6, 2023.
#   - Modified by Al Timofeyev on March 22, 2023.
#   - Modified by Al Timofeyev on April 6, 2023.
#   - Modified by Al Timofeyev on May 31, 2024.
#   - Modified by Al Timofeyev on June 10, 2024.
#   - Modified by Al Timofeyev on July 8, 2024.
#   - Modified by Al Timofeyev on October 12, 2024.


# ---- IMPORTS ----
import multiprocessing
import numpy
import random
import math
import statistics as stats
from . import constants as const


##  Extracts the ratios of hues per pixel.
#
#   @param  hsv_img_matrix_2d   A 2D numpy array of pixels, where each element/pixel
#                               is a list of color values in [h,s,v] format.
#
#   @return Dictionary of hue ratios (percentage) in set [0.0, 100.0]
def extract_ratios(hsv_img_matrix_2d):
    ratio_dict = {'red': 0.0, 'orange': 0.0, 'yellow': 0.0, 'chartreuse': 0.0, 'green': 0.0, 'spring': 0.0,
                  'cyan': 0.0, 'azure': 0.0, 'blue': 0.0, 'violet': 0.0, 'magenta': 0.0, 'rose': 0.0,
                  'norm red': 0.0, 'light red': 0.0, 'dark red': 0.0,
                  'norm orange': 0.0, 'light orange': 0.0, 'dark orange': 0.0,
                  'norm yellow': 0.0, 'light yellow': 0.0, 'dark yellow': 0.0,
                  'norm chartreuse': 0.0, 'light chartreuse': 0.0, 'dark chartreuse': 0.0,
                  'norm green': 0.0, 'light green': 0.0, 'dark green': 0.0,
                  'norm spring': 0.0, 'light spring': 0.0, 'dark spring': 0.0,
                  'norm cyan': 0.0, 'light cyan': 0.0, 'dark cyan': 0.0,
                  'norm azure': 0.0, 'light azure': 0.0, 'dark azure': 0.0,
                  'norm blue': 0.0, 'light blue': 0.0, 'dark blue': 0.0,
                  'norm violet': 0.0, 'light violet': 0.0, 'dark violet': 0.0,
                  'norm magenta': 0.0, 'light magenta': 0.0, 'dark magenta': 0.0,
                  'norm rose': 0.0, 'light rose': 0.0, 'dark rose': 0.0}

    if len(hsv_img_matrix_2d) == 0:
        return ratio_dict

    pixels = float(len(hsv_img_matrix_2d))

    red_pixels = 0.0
    orange_pixels = 0.0
    yellow_pixels = 0.0
    chartreuse_pixels = 0.0
    green_pixels = 0.0
    spring_pixels = 0.0
    cyan_pixels = 0.0
    azure_pixels = 0.0
    blue_pixels = 0.0
    violet_pixels = 0.0
    magenta_pixels = 0.0
    rose_pixels = 0.0

    for pixel in hsv_img_matrix_2d:
        hue = pixel[0]

        if const.ORANGE_HUE_RANGE[0] <= hue < const.ORANGE_HUE_RANGE[1]:
            orange_pixels += 1
        elif const.YELLOW_HUE_RANGE[0] <= hue < const.YELLOW_HUE_RANGE[1]:
            yellow_pixels += 1
        elif const.CHARTREUSE_HUE_RANGE[0] <= hue < const.CHARTREUSE_HUE_RANGE[1]:
            chartreuse_pixels += 1
        elif const.GREEN_HUE_RANGE[0] <= hue < const.GREEN_HUE_RANGE[1]:
            green_pixels += 1
        elif const.SPRING_HUE_RANGE[0] <= hue < const.SPRING_HUE_RANGE[1]:
            spring_pixels += 1
        elif const.CYAN_HUE_RANGE[0] <= hue < const.CYAN_HUE_RANGE[1]:
            cyan_pixels += 1
        elif const.AZURE_HUE_RANGE[0] <= hue < const.AZURE_HUE_RANGE[1]:
            azure_pixels += 1
        elif const.BLUE_HUE_RANGE[0] <= hue < const.BLUE_HUE_RANGE[1]:
            blue_pixels += 1
        elif const.VIOLET_HUE_RANGE[0] <= hue < const.VIOLET_HUE_RANGE[1]:
            violet_pixels += 1
        elif const.MAGENTA_HUE_RANGE[0] <= hue < const.MAGENTA_HUE_RANGE[1]:
            magenta_pixels += 1
        elif const.ROSE_HUE_RANGE[0] <= hue < const.ROSE_HUE_RANGE[1]:
            rose_pixels += 1
        else:  # We don't need to do the last check because we already know it'll be red.
            red_pixels += 1

    # Calculate ratios.
    red_ratio = (red_pixels / pixels) * 100
    orange_ratio = (orange_pixels / pixels) * 100
    yellow_ratio = (yellow_pixels / pixels) * 100
    chartreuse_ratio = (chartreuse_pixels / pixels) * 100
    green_ratio = (green_pixels / pixels) * 100
    spring_ratio = (spring_pixels / pixels) * 100
    cyan_ratio = (cyan_pixels / pixels) * 100
    azure_ratio = (azure_pixels / pixels) * 100
    blue_ratio = (blue_pixels / pixels) * 100
    violet_ratio = (violet_pixels / pixels) * 100
    magenta_ratio = (magenta_pixels / pixels) * 100
    rose_ratio = (rose_pixels / pixels) * 100

    # Assign to the ratio dictionary.
    ratio_dict['red'] = red_ratio
    ratio_dict['orange'] = orange_ratio
    ratio_dict['yellow'] = yellow_ratio
    ratio_dict['chartreuse'] = chartreuse_ratio
    ratio_dict['green'] = green_ratio
    ratio_dict['spring'] = spring_ratio
    ratio_dict['cyan'] = cyan_ratio
    ratio_dict['azure'] = azure_ratio
    ratio_dict['blue'] = blue_ratio
    ratio_dict['violet'] = violet_ratio
    ratio_dict['magenta'] = magenta_ratio
    ratio_dict['rose'] = rose_ratio

    # All other values are calculated during the extraction phase in the Extractor class.
    return ratio_dict


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Constructs dictionary of base colors from an array of HSV pixel values.
#   @details    Base colors are classified as [red, orange,
#               yellow, chartreuse, green, spring, cyan,
#               azure, blue, violet, magenta, rose].
#
#   @note   This function operates on the assumption that all the elements
#           in the hsv_img_matrix_2d array are sorted in ascending order
#           using the hue (h) value.
#
#   @param  hsv_img_matrix_2d   A 2D numpy array of pixels from an image, in [h,s,v] format.
#
#   @return Dictionary of base colors.
def construct_base_color_dictionary(hsv_img_matrix_2d):
    # Using index slicing since array is sorted, and it's much faster.
    start_idx, end_idx = 0, 0
    while end_idx < len(hsv_img_matrix_2d) and (
            const.RED_HUE_RANGE_MIN[0] <= hsv_img_matrix_2d[end_idx][0] < const.RED_HUE_RANGE_MIN[1]):
        end_idx += 1
    red = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.ORANGE_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.ORANGE_HUE_RANGE[1]):
        end_idx += 1
    orange = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.YELLOW_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.YELLOW_HUE_RANGE[1]):
        end_idx += 1
    yellow = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.CHARTREUSE_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.CHARTREUSE_HUE_RANGE[1]):
        end_idx += 1
    chartreuse = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.GREEN_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.GREEN_HUE_RANGE[1]):
        end_idx += 1
    green = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.SPRING_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.SPRING_HUE_RANGE[1]):
        end_idx += 1
    spring = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.CYAN_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.CYAN_HUE_RANGE[1]):
        end_idx += 1
    cyan = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.AZURE_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.AZURE_HUE_RANGE[1]):
        end_idx += 1
    azure = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.BLUE_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.BLUE_HUE_RANGE[1]):
        end_idx += 1
    blue = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.VIOLET_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.VIOLET_HUE_RANGE[1]):
        end_idx += 1
    violet = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.MAGENTA_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.MAGENTA_HUE_RANGE[1]):
        end_idx += 1
    magenta = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.ROSE_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.ROSE_HUE_RANGE[1]):
        end_idx += 1
    rose = hsv_img_matrix_2d[start_idx:end_idx]

    red = numpy.concatenate([red, hsv_img_matrix_2d[end_idx:]])  # Remainder of colors are part of red.

    # Colors in each color array are sorted by hue (1st column) in ascending order.
    base_color_dict = {'red': red, 'orange': orange, 'yellow': yellow, 'chartreuse': chartreuse,
                       'green': green, 'spring': spring, 'cyan': cyan, 'azure': azure,
                       'blue': blue, 'violet': violet, 'magenta': magenta, 'rose': rose}

    return base_color_dict


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Extracts dominant light, normal and dark colors from each of the base colors.
#
#   @param  base_color_dict A dictionary of 2D numpy arrays for each of the base colors.
#   @param  ratios          A dictionary of color ratios (percentages) in set [0.0, 100.0] for each of the base colors.
#
#   @return Dictionary of light, normal and dark color types for each of the base colors.
def extract_colors(base_color_dict, ratios=None):
    # Create a copy of ratios dictionary for multiprocessing.
    if ratios is None:
        process_ratios = multiprocessing.Manager().dict()
    else:
        process_ratios = multiprocessing.Manager().dict(ratios)

    base_colors = [(base_color_dict['red'], 'red', process_ratios),
                   (base_color_dict['orange'], 'orange', process_ratios),
                   (base_color_dict['yellow'], 'yellow', process_ratios),
                   (base_color_dict['chartreuse'], 'chartreuse', process_ratios),
                   (base_color_dict['green'], 'green', process_ratios),
                   (base_color_dict['spring'], 'spring', process_ratios),
                   (base_color_dict['cyan'], 'cyan', process_ratios),
                   (base_color_dict['azure'], 'azure', process_ratios),
                   (base_color_dict['blue'], 'blue', process_ratios),
                   (base_color_dict['violet'], 'violet', process_ratios),
                   (base_color_dict['magenta'], 'magenta', process_ratios),
                   (base_color_dict['rose'], 'rose', process_ratios)]

    # Multi-thread the extraction process.
    pool = multiprocessing.Pool(6)
    async_result = pool.map_async(extract_color_types, base_colors)
    pool.close()
    pool.join()

    # Copy over the ratio types
    if ratios is not None:
        for color_name, color_ratio in process_ratios.items():
            if color_name not in {'red', 'orange', 'yellow', 'chartreuse', 'green', 'spring',
                                  'cyan', 'azure', 'blue', 'violet', 'magenta', 'rose'}:
                ratios[color_name] = color_ratio

    # Retrieve results from multiprocessing pool.
    extracted_results = []
    for value in async_result.get():
        extracted_results.append(value)

    dominant_red_colors, dominant_orange_colors, dominant_yellow_colors, dominant_chartreuse_colors, \
        dominant_green_colors, dominant_spring_colors, dominant_cyan_colors, dominant_azure_colors, \
        dominant_blue_colors, dominant_violet_colors, dominant_magenta_colors, dominant_rose_colors = extracted_results

    light_red_hsv_color, norm_red_hsv_color, dark_red_hsv_color = dominant_red_colors
    light_orange_hsv_color, norm_orange_hsv_color, dark_orange_hsv_color = dominant_orange_colors
    light_yellow_hsv_color, norm_yellow_hsv_color, dark_yellow_hsv_color = dominant_yellow_colors
    light_chartreuse_hsv_color, norm_chartreuse_hsv_color, dark_chartreuse_hsv_color = dominant_chartreuse_colors
    light_green_hsv_color, norm_green_hsv_color, dark_green_hsv_color = dominant_green_colors
    light_spring_hsv_color, norm_spring_hsv_color, dark_spring_hsv_color = dominant_spring_colors
    light_cyan_hsv_color, norm_cyan_hsv_color, dark_cyan_hsv_color = dominant_cyan_colors
    light_azure_hsv_color, norm_azure_hsv_color, dark_azure_hsv_color = dominant_azure_colors
    light_blue_hsv_color, norm_blue_hsv_color, dark_blue_hsv_color = dominant_blue_colors
    light_violet_hsv_color, norm_violet_hsv_color, dark_violet_hsv_color = dominant_violet_colors
    light_magenta_hsv_color, norm_magenta_hsv_color, dark_magenta_hsv_color = dominant_magenta_colors
    light_rose_hsv_color, norm_rose_hsv_color, dark_rose_hsv_color = dominant_rose_colors

    extracted_colors_dict = {'light red': light_red_hsv_color, 'light orange': light_orange_hsv_color,
                             'light yellow': light_yellow_hsv_color, 'light chartreuse': light_chartreuse_hsv_color,
                             'light green': light_green_hsv_color, 'light spring': light_spring_hsv_color,
                             'light cyan': light_cyan_hsv_color, 'light azure': light_azure_hsv_color,
                             'light blue': light_blue_hsv_color, 'light violet': light_violet_hsv_color,
                             'light magenta': light_magenta_hsv_color, 'light rose': light_rose_hsv_color,
                             'red': norm_red_hsv_color, 'orange': norm_orange_hsv_color,
                             'yellow': norm_yellow_hsv_color, 'chartreuse': norm_chartreuse_hsv_color,
                             'green': norm_green_hsv_color, 'spring': norm_spring_hsv_color,
                             'cyan': norm_cyan_hsv_color, 'azure': norm_azure_hsv_color,
                             'blue': norm_blue_hsv_color, 'violet': norm_violet_hsv_color,
                             'magenta': norm_magenta_hsv_color, 'rose': norm_rose_hsv_color,
                             'dark red': dark_red_hsv_color, 'dark orange': dark_orange_hsv_color,
                             'dark yellow': dark_yellow_hsv_color, 'dark chartreuse': dark_chartreuse_hsv_color,
                             'dark green': dark_green_hsv_color, 'dark spring': dark_spring_hsv_color,
                             'dark cyan': dark_cyan_hsv_color, 'dark azure': dark_azure_hsv_color,
                             'dark blue': dark_blue_hsv_color, 'dark violet': dark_violet_hsv_color,
                             'dark magenta': dark_magenta_hsv_color, 'dark rose': dark_rose_hsv_color}

    return extracted_colors_dict


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Checks for any missing colors in the base color dictionary and borrows them from the surrounding colors.
#
#   @internal
#   Example of colors on color a wheel being shown in linear format:
#   ___________________________________________________________
#   || (Left side).............................(Right side)  ||
#   || ------⦧------⦧--------⦧---------⦧----------⦧------  ||
#   || |...red...orange...yellow...chartreuse...green....|  ||
#   || -----⦧--------⦧-------⦧------⦧------⦧--------⦧---- ||
#   || |.violet...magenta...rose...red...orange...yellow.| ||
#   ---------------------------------------------------------
#   @endinternal
#
#   @param  base_color_dict         A dictionary of 2D numpy arrays for each of the base colors.
#   @param  extracted_colors_dict   A dictionary of extracted colors.
def check_missing_colors(base_color_dict, extracted_colors_dict):
    if len(base_color_dict['red']) == 0:
        set_missing_color(extracted_colors_dict, 'red')

    if len(base_color_dict['orange']) == 0:
        set_missing_color(extracted_colors_dict, 'orange')

    if len(base_color_dict['yellow']) == 0:
        set_missing_color(extracted_colors_dict, 'yellow')

    if len(base_color_dict['chartreuse']) == 0:
        set_missing_color(extracted_colors_dict, 'chartreuse')

    if len(base_color_dict['green']) == 0:
        set_missing_color(extracted_colors_dict, 'green')

    if len(base_color_dict['spring']) == 0:
        set_missing_color(extracted_colors_dict, 'spring')

    if len(base_color_dict['cyan']) == 0:
        set_missing_color(extracted_colors_dict, 'cyan')

    if len(base_color_dict['azure']) == 0:
        set_missing_color(extracted_colors_dict, 'azure')

    if len(base_color_dict['blue']) == 0:
        set_missing_color(extracted_colors_dict, 'blue')

    if len(base_color_dict['violet']) == 0:
        set_missing_color(extracted_colors_dict, 'violet')

    if len(base_color_dict['magenta']) == 0:
        set_missing_color(extracted_colors_dict, 'magenta')

    if len(base_color_dict['rose']) == 0:
        set_missing_color(extracted_colors_dict, 'rose')


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Generate the remaining black and white, and background and foreground colors.
#
#   @param  extracted_colors_dict   A Dictionary of extracted colors.
#   @param  ratios                  A Dictionary of ratios of the base colors in the image.
def generate_remaining_colors(extracted_colors_dict, ratios):
    # Get the most dominant and complementary hues.
    dominant_hue = get_dominant_hue(extracted_colors_dict, ratios)
    complementary_hue = (dominant_hue + 180) % 360

    # Generate the remaining colors.
    black_colors, white_colors = generate_black_and_white(dominant_hue)
    light_theme, dark_theme = generate_background_and_foreground(dominant_hue, complementary_hue)

    light_black, norm_black, dark_black = black_colors
    light_white, norm_white, dark_white = white_colors
    light_background, light_foreground = light_theme
    dark_background, dark_foreground = dark_theme

    extracted_colors_dict['light black'] = light_black
    extracted_colors_dict['black'] = norm_black
    extracted_colors_dict['dark black'] = dark_black
    extracted_colors_dict['light white'] = light_white
    extracted_colors_dict['white'] = norm_white
    extracted_colors_dict['dark white'] = dark_white

    extracted_colors_dict['light background'] = light_background
    extracted_colors_dict['light foreground'] = light_foreground
    extracted_colors_dict['dark background'] = dark_background
    extracted_colors_dict['dark foreground'] = dark_foreground


# **************************************************************************
# **************************************************************************

##  Extracts the dominant color types from a base color.
#   @details    A color type is either a light, normal or
#               dark version of a base color.
#
#   @param  color_data  A tuple whose elements are a 2D numpy array of a base color, color name string and ratios dictionary.
#
#   @return List of dominant color types, where each color type is a numpy array in [h,s,v] format.
def extract_color_types(color_data):
    hsv_base_color_matrix, color_name, ratios = color_data

    if len(hsv_base_color_matrix) == 0:
        return [numpy.array([]), numpy.array([]), numpy.array([])]

    color_types = sort_by_sat_and_bright_value(hsv_base_color_matrix, color_name, ratios)

    light_colors, norm_colors, dark_colors, black_colors, achromatic_light_colors, \
        achromatic_norm_colors, achromatic_dark_colors, achromatic_black_colors = color_types

    light_color = extract_dominant_color(light_colors)
    norm_color = extract_dominant_color(norm_colors)
    dark_color = extract_dominant_color(dark_colors)
    black_color = extract_dominant_color(black_colors)

    achromatic_light = extract_dominant_color(achromatic_light_colors)
    achromatic_norm = extract_dominant_color(achromatic_norm_colors)
    achromatic_dark = extract_dominant_color(achromatic_dark_colors)
    achromatic_black = extract_dominant_color(achromatic_black_colors)

    check_missing_color_types(light_color, norm_color, dark_color, black_color,
                              achromatic_light, achromatic_norm, achromatic_dark, achromatic_black)

    return [light_color, norm_color, dark_color]


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Sets a specified color in the extracted colors dictionary by borrowing from other extracted colors.
#
#   @note   There are 12 base colors to choose from:
#           red, orange, yellow, chartreuse, green, spring,
#           cyan, azure, blue, violet, magenta and rose.
#
#   @param  extracted_colors_dict   A dictionary of extracted colors, where each color is a list in HSV format.
#   @param  color_name              A string that represents one of the 12 base colors which will be set.
def set_missing_color(extracted_colors_dict, color_name):
    left_color, right_color = get_left_and_right_colors(color_name)
    extracted_colors_dict['light ' + color_name] = borrow_color(extracted_colors_dict, color_name, left_color, right_color, color_type='light')
    extracted_colors_dict[color_name] = borrow_color(extracted_colors_dict, color_name, left_color, right_color)
    extracted_colors_dict['dark ' + color_name] = borrow_color(extracted_colors_dict, color_name, left_color, right_color, color_type='dark')


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Calculates the dominant hue.
#   @details    The dominant hue, also referred to as the
#               average hue, is based on the color ratios
#               and the colors extracted from an image.
#
#   @param  extracted_colors_dict   A Dictionary of extracted colors.
#   @param  ratios                  A Dictionary of ratios of the colors in the image (contains base and type color ratios).
#
#   @return An integer that represents the dominant hue in an image.
def get_dominant_hue(extracted_colors_dict, ratios):
    dominant_color_name = get_dominant_color_name(ratios)

    # Identify all 3 color types of dominant color.
    light_hue, temp_sat1, temp_bright1 = extracted_colors_dict["light " + dominant_color_name]
    norm_hue, temp_sat2, temp_bright2 = extracted_colors_dict[dominant_color_name]
    dark_hue, temp_sat3, temp_bright3 = extracted_colors_dict["dark " + dominant_color_name]

    # Get the average hue using the dominant colors' 2 color types.
    cos_light_hue = math.cos(math.radians(light_hue))
    cos_norm_hue = math.cos(math.radians(norm_hue))
    cos_dark_hue = math.cos(math.radians(dark_hue))
    cos_hue_types = [cos_light_hue, cos_norm_hue, cos_dark_hue]

    sin_light_hue = math.sin(math.radians(light_hue))
    sin_norm_hue = math.sin(math.radians(norm_hue))
    sin_dark_hue = math.sin(math.radians(dark_hue))
    sin_hue_types = [sin_light_hue, sin_norm_hue, sin_dark_hue]

    average_hue = math.atan2(stats.mean(sin_hue_types), stats.mean(cos_hue_types))
    average_hue = round(math.degrees(average_hue)) % 360

    return average_hue


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Generates black and white color types using the dominant hue.
#   @details    The saturation and brightness values, for the black
#               and white color types, needs to be hardcoded in
#               order to not interfere with the background and
#               foreground colors.
#
#   @param  dominant_hue    An integer that represents the dominant hue in an image.
#
#   @return List of black and white color types in [h,s,v] format.
def generate_black_and_white(dominant_hue):
    light_black = numpy.array([dominant_hue, 15.0, 38.0])
    norm_black = numpy.array([dominant_hue, 18.0, 30.0])
    dark_black = numpy.array([dominant_hue, 25.0, 25.0])

    light_white = numpy.array([dominant_hue, 8.5, 95.0])
    norm_white = numpy.array([dominant_hue, 7.0, 88.0])
    dark_white = numpy.array([dominant_hue, 9.0, 84.0])

    return [[light_black, norm_black, dark_black], [light_white, norm_white, dark_white]]


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Generates the background and foreground colors.
#   @details    The background and foreground colors are based
#               on the dominant hue in an image and it's
#               complimentary hue. The saturation and brightness
#               values for the background and foreground colors
#               need to be hardcoded to be easier to look at.
#
#   @param  dominant_hue        An integer that represents the dominant hue in an image.
#   @param  complementary_hue   An integer that represents the complimentary hue to the dominant hue.
#
#   @return A list of light and dark background and foreground colors in [h,s,v] format.
def generate_background_and_foreground(dominant_hue, complementary_hue):
    light_background_color = numpy.array([dominant_hue, 3.0, 95.0])
    light_foreground_color = numpy.array([complementary_hue, 3.0, 95.0])

    dark_background_color = numpy.array([dominant_hue, 20.0, 17.0])
    dark_foreground_color = numpy.array([complementary_hue, 45.0, 20.0])

    return [[light_background_color, light_foreground_color], [dark_background_color, dark_foreground_color]]


# **************************************************************************
# **************************************************************************

##  Sorts the colors by their saturation and brightness values.
#   @details    A color type is either a light, normal, dark,
#               black or achromatic version of a base color. The
#               ratios for the light, normal and dark color types
#               are also calculated.
#
#   @param  hsv_base_color_matrix   A 2D numpy array of a base color, where each element is a list in [h,s,v] format.
#   @param  color_name              A string that represents the name of a base color.
#   @param  ratios                  A dictionary of color ratios (percentages) in set [0.0, 100.0] for each of the base colors.
#
#   @return A list of color types, where each element is a 2D numpy array of a color type whose elements are a list in [h,s,v] format.
def sort_by_sat_and_bright_value(hsv_base_color_matrix, color_name, ratios):
    if len(hsv_base_color_matrix) == 0:
        return [numpy.asarray([]), numpy.asarray([]), numpy.asarray([]), numpy.asarray([]),
                numpy.asarray([]), numpy.asarray([]), numpy.asarray([]), numpy.asarray([])]

    total_base_color_pixels = len(hsv_base_color_matrix)
    light_pixels, norm_pixels, dark_pixels = 0.0, 0.0, 0.0

    light_colors, norm_colors, dark_colors, black_colors = [], [], [], []
    achromatic_light, achromatic_norm, achromatic_dark, achromatic_black = [], [], [], []

    for pixel in hsv_base_color_matrix:
        _, saturation, brightness = pixel
        if brightness > const.LIGHT_BRIGHTNESS_RANGE[0]:    # -------- If light color.
            if saturation < const.SATURATION_TOLERANCE_RANGE[0]:
                achromatic_light.append(pixel)
            else:
                light_pixels += 1
                light_colors.append(pixel)
        elif brightness > const.NORM_BRIGHTNESS_RANGE[0]:   # -------- If normal color.
            if saturation < const.SATURATION_TOLERANCE_RANGE[0]:
                achromatic_norm.append(pixel)
            else:
                norm_pixels += 1
                norm_colors.append(pixel)
        elif brightness > const.DARK_BRIGHTNESS_RANGE[0]:   # -------- If dark color.
            if saturation < const.SATURATION_TOLERANCE_RANGE[0]:
                achromatic_dark.append(pixel)
            else:
                dark_pixels += 1
                dark_colors.append(pixel)
        else:                                               # -------- If black color.
            if saturation < const.SATURATION_TOLERANCE_RANGE[0]:
                achromatic_black.append(pixel)
            else:
                black_colors.append(pixel)

    # Calculate the ratios for each color type.
    light_ratio = (light_pixels / total_base_color_pixels) * 100.0
    norm_ratio = (norm_pixels / total_base_color_pixels) * 100.0
    dark_ratio = (dark_pixels / total_base_color_pixels) * 100.0

    # Add the color type ratios to the ratio dictionary.
    ratios['light ' + color_name] = light_ratio
    ratios['norm ' + color_name] = norm_ratio
    ratios['dark ' + color_name] = dark_ratio

    return [numpy.asarray(light_colors), numpy.asarray(norm_colors), numpy.asarray(dark_colors), numpy.asarray(black_colors),
            numpy.asarray(achromatic_light), numpy.asarray(achromatic_norm), numpy.asarray(achromatic_dark), numpy.asarray(achromatic_black)]


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Extracts the dominant color from a color type.
#   @details    A color type is either a light, normal, or
#               dark version of a base color.
#
#   @param  hsv_color_type_matrix   A 2D numpy array of a color type where
#                                   every element is a list in [h,s,v] format.
#
#   @return A numpy array of a dominant color in [h,s,v] format.
def extract_dominant_color(hsv_color_type_matrix):
    # Calculate centroid.
    centroid = calculate_centroid(hsv_color_type_matrix)

    # Find color that is closest to centroid by 3-dimensional distance.
    dom_colors = find_closest_to_centroid(hsv_color_type_matrix, centroid)

    dom_color = numpy.array([-1, -1.0, -1.0])
    if len(dom_colors) > 0:
        dom_color[:] = dom_colors[numpy.random.choice(len(dom_colors))]

    return dom_color


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Checks to make sure all the color types have been properly set.
#   @details    If a color type is missing, then it will
#               be derived from the existing color types.
#   @note   I'm using the normalization formula from https://stats.stackexchange.com/a/281164
#
#   @param  light_color         A numpy array of a light color type in [h,s,v] format.
#   @param  norm_color          A numpy array of a normal color type in [h,s,v] format.
#   @param  dark_color          A numpy array of a dark color type in [h,s,v] format.
#   @param  black_color         A numpy array of a black color type in [h,s,v] format.
#   @param  achromatic_light    A numpy array of an achromatic light color type in [h,s,v] format.
#   @param  achromatic_norm     A numpy array of an achromatic normal color type in [h,s,v] format.
#   @param  achromatic_dark     A numpy array of an achromatic dark color type in [h,s,v] format.
#   @param  achromatic_black    A numpy array of an achromatic black color type in [h,s,v] format.
def check_missing_color_types(light_color, norm_color, dark_color, black_color,
                              achromatic_light, achromatic_norm, achromatic_dark, achromatic_black):
    has_light = light_set = light_color[0] != -1
    has_norm = norm_set = norm_color[0] != -1
    has_dark = dark_set = dark_color[0] != -1
    has_black = black_set = black_color[0] != -1

    has_achro_light = achromatic_light[0] != -1
    has_achro_norm = achromatic_norm[0] != -1
    has_achro_dark = achromatic_dark[0] != -1
    has_achro_black = achromatic_black[0] != -1

    # Check and set black color using existing color types.
    if not has_black:
        if has_achro_black:
            black_color[0], black_color[2] = achromatic_black[0], achromatic_black[2]
            old_bounds = [0, const.SATURATION_TOLERANCE_RANGE[0]]
            new_bounds = [const.SATURATION_TOLERANCE_RANGE[0], const.SATURATION_TOLERANCE_RANGE[1]]
            black_color[1] = new_bounds[0] + (((achromatic_black[1] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                              * (new_bounds[1] - new_bounds[0]))
            black_set = True

    # Check and set dark color using existing color types.
    if not has_dark:
        if has_black:
            dark_color[0] = black_color[0]
            dark_color[1] = black_color[1]
            old_bounds = [const.BLACK_BRIGHTNESS_RANGE[0], const.BLACK_BRIGHTNESS_RANGE[1]]
            new_bounds = [const.DARK_BRIGHTNESS_RANGE[0], const.DARK_BRIGHTNESS_RANGE[1]]
            dark_color[2] = new_bounds[0] + (((black_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                             * (new_bounds[1] - new_bounds[0]))
        elif has_light:
            dark_color[0] = light_color[0]
            dark_color[1] = light_color[1]
            old_bounds = [const.LIGHT_BRIGHTNESS_RANGE[0], const.LIGHT_BRIGHTNESS_RANGE[1]]
            new_bounds = [const.DARK_BRIGHTNESS_RANGE[0], const.DARK_BRIGHTNESS_RANGE[1]]
            dark_color[2] = new_bounds[0] + (((light_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                             * (new_bounds[1] - new_bounds[0]))
        elif has_norm:
            dark_color[0] = norm_color[0]
            sat_diff = math.sqrt(100 - norm_color[1]) if norm_color[1] < 50 else math.sqrt(norm_color[1])
            dark_color[1] = norm_color[1] + sat_diff if norm_color[1] < 50 else norm_color[1] - sat_diff
            old_bounds = [const.NORM_BRIGHTNESS_RANGE[0], const.NORM_BRIGHTNESS_RANGE[1]]
            new_bounds = [const.DARK_BRIGHTNESS_RANGE[0], const.DARK_BRIGHTNESS_RANGE[1]]
            dark_color[2] = new_bounds[0] + (((norm_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                             * (new_bounds[1] - new_bounds[0]))
        elif has_achro_dark:
            dark_color[0], dark_color[2] = achromatic_dark[0], achromatic_dark[2]
            old_bounds = [0, const.SATURATION_TOLERANCE_RANGE[0]]
            new_bounds = [const.SATURATION_TOLERANCE_RANGE[0], const.SATURATION_TOLERANCE_RANGE[1]]
            dark_color[1] = new_bounds[0] + (((achromatic_dark[1] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                             * (new_bounds[1] - new_bounds[0]))

        if dark_color[0] != -1:     # If the dark color has been set by one of the options above.
            dark_set = True

    # Check and set light color using existing color types.
    if not has_light:
        if has_dark:
            light_color[0] = dark_color[0]
            light_color[1] = dark_color[1]
            old_bounds = [const.DARK_BRIGHTNESS_RANGE[0], const.DARK_BRIGHTNESS_RANGE[1]]
            new_bounds = [const.LIGHT_BRIGHTNESS_RANGE[0], const.LIGHT_BRIGHTNESS_RANGE[1]]
            light_color[2] = new_bounds[0] + (((dark_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                              * (new_bounds[1] - new_bounds[0]))
        elif has_norm:
            light_color[0] = norm_color[0]
            sat_diff = math.sqrt(100 - norm_color[1]) if norm_color[1] < 50 else math.sqrt(norm_color[1])
            light_color[1] = norm_color[1] + sat_diff if norm_color[1] < 50 else norm_color[1] - sat_diff
            old_bounds = [const.NORM_BRIGHTNESS_RANGE[0], const.NORM_BRIGHTNESS_RANGE[1]]
            new_bounds = [const.LIGHT_BRIGHTNESS_RANGE[0], const.LIGHT_BRIGHTNESS_RANGE[1]]
            light_color[2] = new_bounds[0] + (((norm_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                              * (new_bounds[1] - new_bounds[0]))
        elif has_achro_light:
            light_color[0], light_color[2] = achromatic_light[0], achromatic_light[2]
            old_bounds = [0, const.SATURATION_TOLERANCE_RANGE[0]]
            new_bounds = [const.SATURATION_TOLERANCE_RANGE[0], const.SATURATION_TOLERANCE_RANGE[1]]
            light_color[1] = new_bounds[0] + (((achromatic_light[1] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                              * (new_bounds[1] - new_bounds[0]))

        if light_color[0] != -1:    # If the light color has been set by one of the options above.
            light_set = True

    # Check and set normal color using existing color types.
    if not has_norm:
        if has_dark and has_light:
            cos_light_hue, cos_dark_hue = math.cos(math.radians(light_color[0])), math.cos(math.radians(dark_color[0]))
            sin_light_hue, sin_dark_hue = math.sin(math.radians(light_color[0])), math.sin(math.radians(dark_color[0]))
            norm_color[0] = math.atan2(stats.mean([sin_light_hue, sin_dark_hue]), stats.mean([cos_light_hue, cos_dark_hue]))
            norm_color[0] = round(math.degrees(norm_color[0])) % 360
            norm_color[1] = (light_color[1] + dark_color[1]) / 2
            light_percent = (light_color[2] - const.LIGHT_BRIGHTNESS_RANGE[0]) / (const.LIGHT_BRIGHTNESS_RANGE[1] - const.LIGHT_BRIGHTNESS_RANGE[0])
            dark_percent = (dark_color[2] - const.DARK_BRIGHTNESS_RANGE[0]) / (const.DARK_BRIGHTNESS_RANGE[1] - const.DARK_BRIGHTNESS_RANGE[0])
            avg_light_dark_brightness = (light_percent + dark_percent) / 2
            norm_color[2] = const.NORM_BRIGHTNESS_RANGE[0] + (
                    (const.NORM_BRIGHTNESS_RANGE[1] - const.NORM_BRIGHTNESS_RANGE[0]) * avg_light_dark_brightness)
        elif has_achro_norm:
            norm_color[0], norm_color[2] = achromatic_norm[0], achromatic_norm[2]
            old_bounds = [0, const.SATURATION_TOLERANCE_RANGE[0]]
            new_bounds = [const.SATURATION_TOLERANCE_RANGE[0], const.SATURATION_TOLERANCE_RANGE[1]]
            norm_color[1] = new_bounds[0] + (((achromatic_norm[1] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                             * (new_bounds[1] - new_bounds[0]))

        if norm_color[0] != -1:     # If the normal color has been set by one of the options above.
            norm_set = True

    # Double check for color types that haven't been set yet by using
    # color types that have been set with the previous checks above.
    # Check and set dark color using borrowed color types.
    if not dark_set:
        if black_set:
            dark_color[0] = black_color[0]
            dark_color[1] = black_color[1]
            old_bounds = [const.BLACK_BRIGHTNESS_RANGE[0], const.BLACK_BRIGHTNESS_RANGE[1]]
            new_bounds = [const.DARK_BRIGHTNESS_RANGE[0], const.DARK_BRIGHTNESS_RANGE[1]]
            dark_color[2] = new_bounds[0] + (((black_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                             * (new_bounds[1] - new_bounds[0]))
        elif light_set:
            dark_color[0] = light_color[0]
            dark_color[1] = light_color[1]
            old_bounds = [const.LIGHT_BRIGHTNESS_RANGE[0], const.LIGHT_BRIGHTNESS_RANGE[1]]
            new_bounds = [const.DARK_BRIGHTNESS_RANGE[0], const.DARK_BRIGHTNESS_RANGE[1]]
            dark_color[2] = new_bounds[0] + (((light_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                             * (new_bounds[1] - new_bounds[0]))
        elif norm_set:
            dark_color[0] = norm_color[0]
            sat_diff = math.sqrt(100 - norm_color[1]) if norm_color[1] < 50 else math.sqrt(norm_color[1])
            dark_color[1] = norm_color[1] + sat_diff if norm_color[1] < 50 else norm_color[1] - sat_diff
            old_bounds = [const.NORM_BRIGHTNESS_RANGE[0], const.NORM_BRIGHTNESS_RANGE[1]]
            new_bounds = [const.DARK_BRIGHTNESS_RANGE[0], const.DARK_BRIGHTNESS_RANGE[1]]
            dark_color[2] = new_bounds[0] + (((norm_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                             * (new_bounds[1] - new_bounds[0]))

        if dark_color[0] != -1:     # If the dark color has been set by one of the options above.
            dark_set = True

    # Check and set light color using borrowed color types.
    if not light_set:
        if dark_set:
            light_color[0] = dark_color[0]
            light_color[1] = dark_color[1]
            old_bounds = [const.DARK_BRIGHTNESS_RANGE[0], const.DARK_BRIGHTNESS_RANGE[1]]
            new_bounds = [const.LIGHT_BRIGHTNESS_RANGE[0], const.LIGHT_BRIGHTNESS_RANGE[1]]
            light_color[2] = new_bounds[0] + (((dark_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                              * (new_bounds[1] - new_bounds[0]))
        elif norm_set:
            light_color[0] = norm_color[0]
            sat_diff = math.sqrt(100 - norm_color[1]) if norm_color[1] < 50 else math.sqrt(norm_color[1])
            light_color[1] = norm_color[1] + sat_diff if norm_color[1] < 50 else norm_color[1] - sat_diff
            old_bounds = [const.NORM_BRIGHTNESS_RANGE[0], const.NORM_BRIGHTNESS_RANGE[1]]
            new_bounds = [const.LIGHT_BRIGHTNESS_RANGE[0], const.LIGHT_BRIGHTNESS_RANGE[1]]
            light_color[2] = new_bounds[0] + (((norm_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
                                              * (new_bounds[1] - new_bounds[0]))

        if light_color[0] != -1:    # If the light color has been set by one of the options above.
            light_set = True

    # Check and set normal color using borrowed color types.
    if not norm_set:
        cos_light_hue, cos_dark_hue = math.cos(math.radians(light_color[0])), math.cos(math.radians(dark_color[0]))
        sin_light_hue, sin_dark_hue = math.sin(math.radians(light_color[0])), math.sin(math.radians(dark_color[0]))
        norm_color[0] = math.atan2(stats.mean([sin_light_hue, sin_dark_hue]), stats.mean([cos_light_hue, cos_dark_hue]))
        norm_color[0] = round(math.degrees(norm_color[0])) % 360
        norm_color[1] = (light_color[1] + dark_color[1]) / 2
        light_percent = (light_color[2] - const.LIGHT_BRIGHTNESS_RANGE[0]) / (const.LIGHT_BRIGHTNESS_RANGE[1] - const.LIGHT_BRIGHTNESS_RANGE[0])
        dark_percent = (dark_color[2] - const.DARK_BRIGHTNESS_RANGE[0]) / (const.DARK_BRIGHTNESS_RANGE[1] - const.DARK_BRIGHTNESS_RANGE[0])
        avg_light_dark_brightness = (light_percent + dark_percent) / 2
        norm_color[2] = const.NORM_BRIGHTNESS_RANGE[0] + (
                (const.NORM_BRIGHTNESS_RANGE[1] - const.NORM_BRIGHTNESS_RANGE[0]) * avg_light_dark_brightness)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Gets the color names of the colors that are to the left and right of the originating color.
#   @details    There are two ways to think about left and right on a color wheel:
#               from the top of the color wheel looking at the top-most color or
#               from the bottom of the color wheel looking at the bottom-most color.
#               This has an effect on how we think of the linear format of the color
#               wheel. For this package we will think about left and right colors
#               using the former option (top of the color wheel).
#
#   @internal
#   Example of colors on a color wheel being shown in linear format:
#   ___________________________________________________________
#   || (Left side).............................(Right side)  ||
#   || ------⦧------⦧--------⦧---------⦧----------⦧------  ||
#   || |...red...orange...yellow...chartreuse...green....|  ||
#   || -----⦧--------⦧-------⦧------⦧------⦧--------⦧---- ||
#   || |.violet...magenta...rose...red...orange...yellow.| ||
#   ---------------------------------------------------------
#   @endinternal
#
#   @note   There are 12 base colors to choose from:
#           red, orange, yellow, chartreuse, green, spring,
#           cyan, azure, blue, violet, magenta and rose.
#
#   @param  origin_color_name   A string that represents the name of the originating color.
#   @param  color_type          A string that represents the type of color ('light', 'dark', '' for normal).
#
#   @return List of color names that are to the left and right of the originating color.
def get_left_and_right_colors(origin_color_name, color_type=''):
    color_type += '' if color_type == '' else ' '

    if origin_color_name == 'red':
        left_color, right_color = color_type + 'rose', color_type + 'orange'
        return [left_color, right_color]
    elif origin_color_name == 'orange':
        left_color, right_color = color_type + 'red', color_type + 'yellow'
        return [left_color, right_color]
    elif origin_color_name == 'yellow':
        left_color, right_color = color_type + 'orange', color_type + 'chartreuse'
        return [left_color, right_color]
    elif origin_color_name == 'chartreuse':
        left_color, right_color = color_type + 'yellow', color_type + 'green'
        return [left_color, right_color]
    elif origin_color_name == 'green':
        left_color, right_color = color_type + 'chartreuse', color_type + 'spring'
        return [left_color, right_color]
    elif origin_color_name == 'spring':
        left_color, right_color = color_type + 'green', color_type + 'cyan'
        return [left_color, right_color]
    elif origin_color_name == 'cyan':
        left_color, right_color = color_type + 'spring', color_type + 'azure'
        return [left_color, right_color]
    elif origin_color_name == 'azure':
        left_color, right_color = color_type + 'cyan', color_type + 'blue'
        return [left_color, right_color]
    elif origin_color_name == 'blue':
        left_color, right_color = color_type + 'azure', color_type + 'violet'
        return [left_color, right_color]
    elif origin_color_name == 'violet':
        left_color, right_color = color_type + 'blue', color_type + 'magenta'
        return [left_color, right_color]
    elif origin_color_name == 'magenta':
        left_color, right_color = color_type + 'violet', color_type + 'rose'
        return [left_color, right_color]
    elif origin_color_name == 'rose':
        left_color, right_color = color_type + 'magenta', color_type + 'red'
        return [left_color, right_color]


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Borrows a color from one of the extracted color types of the base colors.
#
#   @param  extracted_colors_dict   A dictionary of extracted colors.
#   @param  origin                  A string that represents the name of the originating color.
#   @param  borrow_left             A string that represents the name of the color to borrow from, to the left of origin.
#   @param  borrow_right            A string that represents the name of the color to borrow from, to the right of origin.
#   @param  color_type              A string that represents the type of color ('light', 'dark', '' for normal).
#
#   @return A numpy array of a borrowed color.
def borrow_color(extracted_colors_dict, origin, borrow_left, borrow_right, color_type=''):
    potential_left, potential_right = [], []
    left_hue_shift, right_hue_shift = 0, 0

    spacing = '' if color_type == '' else ' '

    if borrow_left is not None:
        color_name = color_type + spacing + borrow_left
        borrowed_color = extracted_colors_dict[color_name]
        if len(borrowed_color) == 0:  # ---- If no left color sample, recurse further to the left.
            left_color, right_color = get_left_and_right_colors(borrow_left)
            borrowed_color = borrow_color(extracted_colors_dict, origin, left_color, None, color_type=color_type)
        potential_left = numpy.array(borrowed_color)
        left_hue_shift = get_hue_shift_value(potential_left[0], 30.0)

    if borrow_right is not None:
        color_name = color_type + spacing + borrow_right
        borrowed_color = extracted_colors_dict[color_name]
        if len(borrowed_color) == 0:  # ---- If no right color sample, recurse further to the right.
            left_color, right_color = get_left_and_right_colors(borrow_right)
            borrowed_color = borrow_color(extracted_colors_dict, origin, None, right_color, color_type=color_type)
        potential_right = numpy.array(borrowed_color)
        right_hue_shift = get_hue_shift_value(potential_right[0], 30.0)

    # ---- Shift Hues.
    if len(potential_left) != 0:
        potential_left[0] += left_hue_shift
        potential_left[0] = potential_left[0] % 360
    if len(potential_right) != 0:
        potential_right[0] -= right_hue_shift
        potential_right[0] = 360 + potential_right[0] if potential_right[0] < 0 else potential_right[0]

    # ---- If only one potential color has been borrowed, return it.
    if len(potential_left) != 0 and len(potential_right) == 0:
        return potential_left
    elif len(potential_left) == 0 and len(potential_right) != 0:
        return potential_right

    # ---- Calculate distance to the optimal hue of original color, defined in constants.
    optimal_hue = const.RED_HUE  # -- Default
    if origin == 'orange':
        optimal_hue = const.ORANGE_HUE
    elif origin == 'yellow':
        optimal_hue = const.YELLOW_HUE
    elif origin == 'chartreuse':
        optimal_hue = const.CHARTREUSE_HUE
    elif origin == 'green':
        optimal_hue = const.GREEN_HUE
    elif origin == 'spring':
        optimal_hue = const.SPRING_HUE
    elif origin == 'cyan':
        optimal_hue = const.CYAN_HUE
    elif origin == 'azure':
        optimal_hue = const.AZURE_HUE
    elif origin == 'blue':
        optimal_hue = const.BLUE_HUE
    elif origin == 'violet':
        optimal_hue = const.VIOLET_HUE
    elif origin == 'magenta':
        optimal_hue = const.MAGENTA_HUE
    elif origin == 'rose':
        optimal_hue = const.ROSE_HUE

    distance_from_left = min(abs(optimal_hue - potential_left[0]), 360 - abs(optimal_hue - potential_left[0]))
    distance_from_right = min(abs(optimal_hue - potential_right[0]), 360 - abs(optimal_hue - potential_right[0]))

    # ---- Return the colors that are closest to the origin color.
    if distance_from_left < distance_from_right:
        return potential_left
    else:
        return potential_right


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Get the base name of the dominant color from a dictionary of ratios.
#
#   @param  ratios  A dictionary that contains ratios for the 12 base
#                   colors as well as for each of their color types.
#
#   @return A string that represents the name of the dominant color from one of the 12 base colors.
def get_dominant_color_name(ratios):
    highest_percentage = 0.0
    dominant_color_array = []

    # Get the highest percentage from the base colors ONLY.
    for color_name, percentage in ratios.items():
        if color_name in {'red', 'orange', 'yellow', 'chartreuse', 'green', 'spring',
                          'cyan', 'azure', 'blue', 'violet', 'magenta', 'rose'}:
            highest_percentage = max(highest_percentage, percentage)

    # Get the list of base colors that match the highest percentage.
    for color_name, percentage in ratios.items():
        if color_name in {'red', 'orange', 'yellow', 'chartreuse', 'green', 'spring',
                          'cyan', 'azure', 'blue', 'violet', 'magenta', 'rose'} and percentage == highest_percentage:
            dominant_color_array.append(color_name)

    # Pick a random color from the list if there's more than one.
    index = random.randrange(len(dominant_color_array)) if len(dominant_color_array) > 1 else 0
    dominant_color_name = dominant_color_array[index]

    return dominant_color_name


# **************************************************************************
# **************************************************************************

##  Calculates the centroid for a color type.
#   @details    The centroid is basically the average color of
#               a set of colors in [h,s,v] format. The centroid
#               is a point in 3-dimensional space. The following
#               sources were used to make this algorithm:
#               http://mkweb.bcgsc.ca/color-summarizer/?faq#averagehue and
#               https://stackoverflow.com/a/8170595/17047816
#
#   @param  hsv_color_type_matrix   A 2D numpy array of a color type in [h,s,v] format.
#
#   @return List of centroid color values in [h,s,l] format.
def calculate_centroid(hsv_color_type_matrix):
    if len(hsv_color_type_matrix) == 0:
        return [-1, -1.0, -1.0]

    average_saturation, average_brightness = 0.0, 0.0
    cos_hues, sin_hues = [], []

    for hsv_color in hsv_color_type_matrix:
        cos_hues.append(math.cos(math.radians(hsv_color[0])))
        sin_hues.append(math.sin(math.radians(hsv_color[0])))
        average_saturation += hsv_color[1]
        average_brightness += hsv_color[2]

    average_saturation = average_saturation / len(hsv_color_type_matrix)
    average_brightness = average_brightness / len(hsv_color_type_matrix)
    average_hue = math.atan2(stats.mean(sin_hues), stats.mean(cos_hues))
    average_hue = round(math.degrees(average_hue)) % 360

    centroid_hsv_color = [average_hue, average_saturation, average_brightness]

    return centroid_hsv_color


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Finds a color from a color type that is closest to the centroid.
#   @details    The distance between the centroid color and each of the
#               other individual colors is calculated in 3-dimensional
#               space using the Euclidean Distance formula from the following sources:
#               https://stackoverflow.com/a/35114586/17047816 and
#               https://byjus.com/maths/distance-between-two-points-3d/.
#
#   @param  hsv_color_type_matrix   A 2D numpy array of a color type where
#                                   every element is a list in [h,s,v] format.
#   @param  centroid                List of centroid color values in [h,s,l] format.
#
#   @return List of all the colors in [h,s,v] format that are the shortest distance away from the centroid.
def find_closest_to_centroid(hsv_color_type_matrix, centroid):
    if len(hsv_color_type_matrix) == 0:
        return []

    distances_from_centroid = []
    shortest_distance = math.inf

    # Calculate the distance between each color and the centroid.
    # All values are normalized to be in the range [0.0, 1.0] for this process.
    for hsv_color in hsv_color_type_matrix:
        distance = calculate_dist_between_2_colors(hsv_color, centroid)

        distances_from_centroid.append(distance)
        shortest_distance = min(shortest_distance, distance)

    closest = []
    for idx, dist in enumerate(distances_from_centroid):
        if dist != shortest_distance:
            continue
        closest.append(hsv_color_type_matrix[idx])

    return closest


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Gets the appropriate percentage to shift a hue value based on the hue provided.
#   @details    The shift percentage tells use by how much
#               to shift a hue value based on what range the
#               hue is in.
#
#   @param  hue                 An integer that represents a hue value in range [0, 359].
#   @param  shift_percentage    A float that represents the percentage in range [0.0, 100.0] by which to shift hue.
#
#   @return An integer that represents the value by which to shift the hue.
def get_hue_shift_value(hue, shift_percentage):
    # Normalize percentage to be in range [0.0, 1.0]
    shift_percentage /= 100.0

    # Red range is used by default.
    range_difference = (const.RED_HUE_RANGE_MIN[1] - const.RED_HUE_RANGE_MIN[0]) + \
                       (const.RED_HUE_RANGE_MAX[1] - const.RED_HUE_RANGE_MAX[0])

    if const.ORANGE_HUE_RANGE[0] <= hue < const.ORANGE_HUE_RANGE[1]:
        range_difference = const.ORANGE_HUE_RANGE[1] - const.ORANGE_HUE_RANGE[0]
    elif const.YELLOW_HUE_RANGE[0] <= hue < const.YELLOW_HUE_RANGE[1]:
        range_difference = const.YELLOW_HUE_RANGE[1] - const.YELLOW_HUE_RANGE[0]
    elif const.CHARTREUSE_HUE_RANGE[0] <= hue < const.CHARTREUSE_HUE_RANGE[1]:
        range_difference = const.CHARTREUSE_HUE_RANGE[1] - const.CHARTREUSE_HUE_RANGE[0]
    elif const.GREEN_HUE_RANGE[0] <= hue < const.GREEN_HUE_RANGE[1]:
        range_difference = const.GREEN_HUE_RANGE[1] - const.GREEN_HUE_RANGE[0]
    elif const.SPRING_HUE_RANGE[0] <= hue < const.SPRING_HUE_RANGE[1]:
        range_difference = const.SPRING_HUE_RANGE[1] - const.SPRING_HUE_RANGE[0]
    elif const.CYAN_HUE_RANGE[0] <= hue < const.CYAN_HUE_RANGE[1]:
        range_difference = const.CYAN_HUE_RANGE[1] - const.CYAN_HUE_RANGE[0]
    elif const.AZURE_HUE_RANGE[0] <= hue < const.AZURE_HUE_RANGE[1]:
        range_difference = const.AZURE_HUE_RANGE[1] - const.AZURE_HUE_RANGE[0]
    elif const.BLUE_HUE_RANGE[0] <= hue < const.BLUE_HUE_RANGE[1]:
        range_difference = const.BLUE_HUE_RANGE[1] - const.BLUE_HUE_RANGE[0]
    elif const.VIOLET_HUE_RANGE[0] <= hue < const.VIOLET_HUE_RANGE[1]:
        range_difference = const.VIOLET_HUE_RANGE[1] - const.VIOLET_HUE_RANGE[0]
    elif const.MAGENTA_HUE_RANGE[0] <= hue < const.MAGENTA_HUE_RANGE[1]:
        range_difference = const.MAGENTA_HUE_RANGE[1] - const.MAGENTA_HUE_RANGE[0]
    elif const.ROSE_HUE_RANGE[0] <= hue < const.ROSE_HUE_RANGE[1]:
        range_difference = const.ROSE_HUE_RANGE[1] - const.ROSE_HUE_RANGE[0]

    return round(range_difference * shift_percentage)


# **************************************************************************
# **************************************************************************

##  Calculates the distance between 2 HSV colors.
#
#   @param  hsv_color1  A list or numpy array of a color in HSV format [h, s, v].
#   @param  hsv_color2  A list or numpy array of a color in HSV format [h, s, v].
#
#   @return A float value that represents the distance between 2 colors.
def calculate_dist_between_2_colors(hsv_color1, hsv_color2):
    # All values are normalized to be in the range [0.0, 1.0] for this process.
    hue_dist = min(abs(hsv_color1[0] - hsv_color2[0]), 360 - abs(hsv_color1[0] - hsv_color2[0])) / 180.0
    sat_dist = abs(hsv_color1[1] - hsv_color2[1]) / 100.0
    bright_dist = abs(hsv_color1[2] - hsv_color2[2]) / 100.0

    distance = math.sqrt(hue_dist ** 2 + sat_dist ** 2 + bright_dist ** 2)

    return distance
