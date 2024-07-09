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


# ---- IMPORTS ----
import multiprocessing
import numpy
import random
import math
import statistics as stats
from . import constants as const


##  Extracts the ratios of hues per pixel.
#
#   @param  hsv_img_matrix_2d   A 2D numpy array of pixels from an image in [h,s,v] format.
#
#   @return Dictionary of hue ratios (percentage) in set [0.0, 100.0]
def extract_ratios(hsv_img_matrix_2d):
    pixels = 0
    red_pixel = 0
    yellow_pixel = 0
    green_pixel = 0
    cyan_pixel = 0
    blue_pixel = 0
    magenta_pixel = 0

    for pixel in hsv_img_matrix_2d:
        pixels += 1
        hue = pixel[0]
        if ((const.RED_HUE_RANGE_MAX[0] <= hue < const.RED_HUE_RANGE_MAX[1])
                or (const.RED_HUE_RANGE_MIN[0] <= hue < const.RED_HUE_RANGE_MIN[1])):
            red_pixel += 1
        elif const.YELLOW_HUE_RANGE[0] <= hue < const.YELLOW_HUE_RANGE[1]:
            yellow_pixel += 1
        elif const.GREEN_HUE_RANGE[0] <= hue < const.GREEN_HUE_RANGE[1]:
            green_pixel += 1
        elif const.CYAN_HUE_RANGE[0] <= hue < const.CYAN_HUE_RANGE[1]:
            cyan_pixel += 1
        elif const.BLUE_HUE_RANGE[0] <= hue < const.BLUE_HUE_RANGE[1]:
            blue_pixel += 1
        elif const.MAGENTA_HUE_RANGE[0] <= hue < const.MAGENTA_HUE_RANGE[1]:
            magenta_pixel += 1

    # Calculate ratios.
    red_ratio = (red_pixel / pixels) * 100
    yellow_ration = (yellow_pixel / pixels) * 100
    green_ration = (green_pixel / pixels) * 100
    cyan_ratio = (cyan_pixel / pixels) * 100
    blue_ratio = (blue_pixel / pixels) * 100
    magenta_ratio = (magenta_pixel / pixels) * 100

    # Assign the ratio dictionary.
    ratio_dict = {'red': red_ratio, 'yellow': yellow_ration, 'green': green_ration,
                  'cyan': cyan_ratio, 'blue': blue_ratio, 'magenta': magenta_ratio}

    return ratio_dict


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Constructs dictionary of base colors from an array of HSV pixel values.
#   @details    Base colors are classified as [red, yellow, green, cyan, blue, magenta].
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
            const.YELLOW_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.YELLOW_HUE_RANGE[1]):
        end_idx += 1
    yellow = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.GREEN_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.GREEN_HUE_RANGE[1]):
        end_idx += 1
    green = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.CYAN_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.CYAN_HUE_RANGE[1]):
        end_idx += 1
    cyan = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.BLUE_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.BLUE_HUE_RANGE[1]):
        end_idx += 1
    blue = hsv_img_matrix_2d[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsv_img_matrix_2d) and (
            const.MAGENTA_HUE_RANGE[0] <= hsv_img_matrix_2d[end_idx][0] < const.MAGENTA_HUE_RANGE[1]):
        end_idx += 1
    magenta = hsv_img_matrix_2d[start_idx:end_idx]

    red = numpy.concatenate([red, hsv_img_matrix_2d[end_idx:]])     # Remainder of colors are part of red.

    # Colors in each color array are sorted by hue (1st column) in ascending order.
    base_color_dict = {'red': red, 'yellow': yellow, 'green': green,
                       'cyan': cyan, 'blue': blue, 'magenta': magenta}

    return base_color_dict


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Extracts dominant light, normal and dark colors from each of the base colors.
#
#   @param  base_color_dict A dictionary of 2D numpy arrays for each of the base colors.
#
#   @return Dictionary of light, normal and dark color types for each of the base colors.
def extract_colors(base_color_dict):
    base_colors = [base_color_dict['red'], base_color_dict['yellow'], base_color_dict['green'],
                   base_color_dict['cyan'], base_color_dict['blue'], base_color_dict['magenta']]

    # Multi-thread the extraction process.
    pool = multiprocessing.Pool(6)
    async_result = pool.map_async(extract_color_types, base_colors)
    pool.close()
    pool.join()

    extracted_results = []
    for value in async_result.get():
        extracted_results.append(value)

    dominant_red_colors, dominant_yellow_colors, dominant_green_colors, dominant_cyan_colors, dominant_blue_colors, dominant_magenta_colors = extracted_results

    light_red_hsv_color, norm_red_hsv_color, dark_red_hsv_color = dominant_red_colors
    light_yellow_hsv_color, norm_yellow_hsv_color, dark_yellow_hsv_color = dominant_yellow_colors
    light_green_hsv_color, norm_green_hsv_color, dark_green_hsv_color = dominant_green_colors
    light_cyan_hsv_color, norm_cyan_hsv_color, dark_cyan_hsv_color = dominant_cyan_colors
    light_blue_hsv_color, norm_blue_hsv_color, dark_blue_hsv_color = dominant_blue_colors
    light_magenta_hsv_color, norm_magenta_hsv_color, dark_magenta_hsv_color = dominant_magenta_colors

    extracted_colors_dict = {'light red': light_red_hsv_color, 'light yellow': light_yellow_hsv_color,
                             'light green': light_green_hsv_color, 'light cyan': light_cyan_hsv_color,
                             'light blue': light_blue_hsv_color, 'light magenta': light_magenta_hsv_color,
                             'red': norm_red_hsv_color, 'yellow': norm_yellow_hsv_color,
                             'green': norm_green_hsv_color, 'cyan': norm_cyan_hsv_color,
                             'blue': norm_blue_hsv_color, 'magenta': norm_magenta_hsv_color,
                             'dark red': dark_red_hsv_color, 'dark yellow': dark_yellow_hsv_color,
                             'dark green': dark_green_hsv_color, 'dark cyan': dark_cyan_hsv_color,
                             'dark blue': dark_blue_hsv_color, 'dark magenta': dark_magenta_hsv_color}

    return extracted_colors_dict


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Checks for any missing colors in the base color dictionary and borrows them from the surrounding colors.
#
#   @internal
#   Example of colors on color a wheel being shown in linear format:
#   ________________________________________________________
#   || (Left side)..........................(Right side)  ||
#   || ---⦧-------⦧-------⦧------⦧------⦧-------⦧-----  ||
#   || |.red...magenta...blue...cyan...green...yellow.|  ||
#   || ----⦧-------⦧-------⦧------⦧-------⦧-------⦧--- ||
#   || |.green...yellow...red...magenta...blue...cyan.| ||
#   ------------------------------------------------------
#   @endinternal
#
#   @param  base_color_dict         A dictionary of 2D numpy arrays for each of the base colors.
#   @param  extracted_colors_dict   A Dictionary of extracted colors.
def check_missing_colors(base_color_dict, extracted_colors_dict):
    if len(base_color_dict['red']) == 0:
        left_color, right_color = get_left_and_right_colors('light red')
        extracted_colors_dict['light red'] = borrow_color(extracted_colors_dict, 'light red', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('red')
        extracted_colors_dict['red'] = borrow_color(extracted_colors_dict, 'red', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('dark red')
        extracted_colors_dict['dark red'] = borrow_color(extracted_colors_dict, 'dark red', left_color, right_color)

    if len(base_color_dict['yellow']) == 0:
        left_color, right_color = get_left_and_right_colors('light yellow')
        extracted_colors_dict['light yellow'] = borrow_color(extracted_colors_dict, 'light yellow', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('yellow')
        extracted_colors_dict['yellow'] = borrow_color(extracted_colors_dict, 'yellow', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('dark yellow')
        extracted_colors_dict['dark yellow'] = borrow_color(extracted_colors_dict, 'dark yellow', left_color, right_color)

    if len(base_color_dict['green']) == 0:
        left_color, right_color = get_left_and_right_colors('light green')
        extracted_colors_dict['light green'] = borrow_color(extracted_colors_dict, 'light green', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('green')
        extracted_colors_dict['green'] = borrow_color(extracted_colors_dict, 'green', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('dark green')
        extracted_colors_dict['dark green'] = borrow_color(extracted_colors_dict, 'dark green', left_color, right_color)

    if len(base_color_dict['cyan']) == 0:
        left_color, right_color = get_left_and_right_colors('light cyan')
        extracted_colors_dict['light cyan'] = borrow_color(extracted_colors_dict, 'light cyan', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('cyan')
        extracted_colors_dict['cyan'] = borrow_color(extracted_colors_dict, 'cyan', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('dark cyan')
        extracted_colors_dict['dark cyan'] = borrow_color(extracted_colors_dict, 'dark cyan', left_color, right_color)

    if len(base_color_dict['blue']) == 0:
        left_color, right_color = get_left_and_right_colors('light blue')
        extracted_colors_dict['light blue'] = borrow_color(extracted_colors_dict, 'light blue', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('blue')
        extracted_colors_dict['blue'] = borrow_color(extracted_colors_dict, 'blue', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('dark blue')
        extracted_colors_dict['dark blue'] = borrow_color(extracted_colors_dict, 'dark blue', left_color, right_color)

    if len(base_color_dict['magenta']) == 0:
        left_color, right_color = get_left_and_right_colors('light magenta')
        extracted_colors_dict['light magenta'] = borrow_color(extracted_colors_dict, 'light magenta', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('magenta')
        extracted_colors_dict['magenta'] = borrow_color(extracted_colors_dict, 'magenta', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('dark magenta')
        extracted_colors_dict['dark magenta'] = borrow_color(extracted_colors_dict, 'dark magenta', left_color, right_color)


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
#   @details    A color type is either a light, normal, or
#               dark version of a base color.
#
#   @param  hsv_base_color_matrix   A 2D numpy array of a base color where
#                                   every element is a list in [h,s,v] format.
#
#   @return List of dominant color types, where each color type is a numpy array in [h,s,v] format.
def extract_color_types(hsv_base_color_matrix):
    if len(hsv_base_color_matrix) == 0:
        return [numpy.array([]), numpy.array([]), numpy.array([])]

    light_colors, norm_colors, dark_colors, black_colors, achromatic_light_colors, \
    achromatic_norm_colors, achromatic_dark_colors, achromatic_black_colors = sort_by_sat_and_bright_value(hsv_base_color_matrix)

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

##  Gets the color names of the colors that are to the left and right of the originating color.
#   @details    There are two ways to think about left and right on a color wheel:
#               from the inside looking outward and from the outside looking inward.
#               This has an effect on how we think of the linear format of the color
#               wheel. For this package we will think about left and right colors
#               using the latter option.
#
#   @internal
#   Example of colors on a color wheel being shown in linear format:
#   ________________________________________________________
#   || (Left side)..........................(Right side)  ||
#   || ---⦧-------⦧-------⦧------⦧------⦧-------⦧-----  ||
#   || |.red...magenta...blue...cyan...green...yellow.|  ||
#   || ----⦧-------⦧-------⦧------⦧-------⦧-------⦧--- ||
#   || |.green...yellow...red...magenta...blue...cyan.| ||
#   ------------------------------------------------------
#   @endinternal
#
#   @param  origin_color_name   The name of the originating color.
#
#   @return List of color names that are to the left and right of the originating color.
def get_left_and_right_colors(origin_color_name):
    if origin_color_name == 'light red':
        return ['light yellow', 'light magenta']
    elif origin_color_name == 'red':
        return ['yellow', 'magenta']
    elif origin_color_name == 'dark red':
        return ['dark yellow', 'dark magenta']
    elif origin_color_name == 'light yellow':
        return ['light green', 'light red']
    elif origin_color_name == 'yellow':
        return ['green', 'red']
    elif origin_color_name == 'dark yellow':
        return ['dark green', 'dark red']
    elif origin_color_name == 'light green':
        return ['light cyan', 'light yellow']
    elif origin_color_name == 'green':
        return ['cyan', 'yellow']
    elif origin_color_name == 'dark green':
        return ['dark cyan', 'dark yellow']
    elif origin_color_name == 'light cyan':
        return ['light blue', 'light green']
    elif origin_color_name == 'cyan':
        return ['blue', 'green']
    elif origin_color_name == 'dark cyan':
        return ['dark blue', 'dark green']
    elif origin_color_name == 'light blue':
        return ['light magenta', 'light cyan']
    elif origin_color_name == 'blue':
        return ['magenta', 'cyan']
    elif origin_color_name == 'dark blue':
        return ['dark magenta', 'dark cyan']
    elif origin_color_name == 'light magenta':
        return ['light red', 'light blue']
    elif origin_color_name == 'magenta':
        return ['red', 'blue']
    elif origin_color_name == 'dark magenta':
        return ['dark red', 'dark blue']


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Borrows a color from one of the extracted color types of the base colors.
#
#   @param  extracted_colors_dict   A Dictionary of extracted colors.
#   @param  origin                  The name of the originating color.
#   @param  borrow_left             The name of the color to borrow from, to the left of origin.
#   @param  borrow_right            The name of the color to borrow from, to the right of origin.
#
#   @return A numpy array of a borrowed color.
def borrow_color(extracted_colors_dict, origin, borrow_left, borrow_right):
    potential_left, potential_right = [], []

    if borrow_left is not None:
        borrowed_color = extracted_colors_dict[borrow_left]
        if len(borrowed_color) == 0:    # ---- If no left color sample, recurse further to the left.
            left_color, right_color = get_left_and_right_colors(borrow_left)
            borrowed_color = borrow_color(extracted_colors_dict, origin, left_color, None)
        potential_left = numpy.array(borrowed_color)

    if borrow_right is not None:
        borrowed_color = extracted_colors_dict[borrow_right]
        if len(borrowed_color) == 0:    # ---- If no right color sample, recurse further to the right.
            left_color, right_color = get_left_and_right_colors(borrow_right)
            borrowed_color = borrow_color(extracted_colors_dict, origin, None, right_color)
        potential_right = numpy.array(borrowed_color)

    # ---- Shift Hues.
    if len(potential_left) != 0:
        potential_left[0] -= 20
        potential_left[0] = 360 + potential_left[0] if potential_left[0] < 0 else potential_left[0]
    if len(potential_right) != 0:
        potential_right[0] += 20
        potential_right[0] = potential_right[0] % 360

    # ---- If only one potential color has been borrowed, return it.
    if len(potential_left) != 0 and len(potential_right) == 0:
        return potential_left
    elif len(potential_right) != 0 and len(potential_left) == 0:
        return potential_right

    # ---- Calculate distance to the optimal hue of original color, defined in constants.
    optimal_hue = const.RED_HUE     # -- Default
    if origin == 'light red' or origin == 'red' or origin == 'dark red':
        optimal_hue = const.RED_HUE
    elif origin == 'light yellow' or origin == 'yellow' or origin == 'dark yellow':
        optimal_hue = const.YELLOW_HUE
    elif origin == 'light green' or origin == 'green' or origin == 'dark green':
        optimal_hue = const.GREEN_HUE
    elif origin == 'light cyan' or origin == 'cyan' or origin == 'dark cyan':
        optimal_hue = const.CYAN_HUE
    elif origin == 'light blue' or origin == 'blue' or origin == 'dark blue':
        optimal_hue = const.BLUE_HUE
    elif origin == 'light magenta' or origin == 'magenta' or origin == 'dark magenta':
        optimal_hue = const.MAGENTA_HUE

    distance_from_left = min(abs(optimal_hue - potential_left[0]), 360 - abs(optimal_hue - potential_left[0]))
    distance_from_right = min(abs(optimal_hue - potential_right[0]), 360 - abs(optimal_hue - potential_right[0]))

    # ---- Return the colors that are closest to the origin color.
    if distance_from_left < distance_from_right:
        return potential_left
    else:
        return potential_right


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Calculates the dominant hue.
#   @details    The dominant hue, also referred to as the
#               average hue, is based on the color ratios
#               and the colors extracted from an image.
#
#   @param  extracted_colors_dict   A Dictionary of extracted colors.
#   @param  ratios                  A Dictionary of ratios of the base colors in the image.
#
#   @return The dominant hue in an image.
def get_dominant_hue(extracted_colors_dict, ratios):
    highest_percentage = 0.0
    dominant_color_array = []

    for color_name, percentage in ratios.items():
        highest_percentage = max(highest_percentage, percentage)

    for color_name, percentage in ratios.items():
        if percentage == highest_percentage:
            dominant_color_array.append(color_name)

    index = random.randrange(len(dominant_color_array)) if len(dominant_color_array) > 0 else -1
    dominant_color_name = dominant_color_array[index]

    light_hue, temp_sat1, temp_bright1 = extracted_colors_dict["light " + dominant_color_name]
    norm_hue, temp_sat2, temp_bright2 = extracted_colors_dict[dominant_color_name]
    dark_hue, temp_sat3, temp_bright3 = extracted_colors_dict["dark " + dominant_color_name]

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
#   @param  dominant_hue    The dominant hue of an image.
#
#   @return List of black and white color types in [h,s,v] format.
def generate_black_and_white(dominant_hue):
    light_black = numpy.array([dominant_hue, 40.0, 30.0])
    norm_black = numpy.array([dominant_hue, 65.0, 25.0])
    dark_black = numpy.array([dominant_hue, 40.0, 15.0])

    light_white = numpy.array([dominant_hue, 3.0, 95.0])
    norm_white = numpy.array([dominant_hue, 4.0, 89.0])
    dark_white = numpy.array([dominant_hue, 7.0, 84.0])

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
#   @param  dominant_hue        The dominant hue of an image.
#   @param  complementary_hue   The complimentary hue to the dominant hue.
#
#   @return Numpy array of light and dark background and foreground colors in [h,s,v] format.
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
#               black or achromatic version of a base color.
#
#   @param  hsv_base_color_matrix   A 2D numpy array of a base color, where
#                                   each element is a list in [h,s,v] format.
#
#   @return A list of color types, where each element is a 2D numpy array
#           of a color type whose elements are a list in [h,s,v] format.
def sort_by_sat_and_bright_value(hsv_base_color_matrix):
    light_colors, norm_colors, dark_colors, black_colors = [], [], [], []
    achromatic_light, achromatic_norm, achromatic_dark, achromatic_black = [], [], [], []

    for pixel in hsv_base_color_matrix:
        _, saturation, brightness = pixel
        if brightness > const.LIGHT_BRIGHTNESS_RANGE[0]:    # -------- If light color.
            if saturation < const.SATURATION_TOLERANCE_RANGE[0]:
                achromatic_light.append(pixel)
            else:
                light_colors.append(pixel)
        elif brightness > const.NORM_BRIGHTNESS_RANGE[0]:   # -------- If normal color.
            if saturation < const.SATURATION_TOLERANCE_RANGE[0]:
                achromatic_norm.append(pixel)
            else:
                norm_colors.append(pixel)
        elif brightness > const.DARK_BRIGHTNESS_RANGE[0]:   # -------- If dark color.
            if saturation < const.SATURATION_TOLERANCE_RANGE[0]:
                achromatic_dark.append(pixel)
            else:
                dark_colors.append(pixel)
        else:                                               # -------- If black color.
            if saturation < const.SATURATION_TOLERANCE_RANGE[0]:
                achromatic_black.append(pixel)
            else:
                black_colors.append(pixel)

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
#   @return A numpy array of a dominant color from a color type in [h,s,v] format.
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
            dark_color[2] = new_bounds[1] - (((light_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
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
            light_color[2] = new_bounds[1] - (((dark_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
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
            dark_color[2] = new_bounds[1] - (((light_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
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
            light_color[2] = new_bounds[1] - (((dark_color[2] - old_bounds[0]) / (old_bounds[1] - old_bounds[0]))
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
        hue, sat, bright = hsv_color
        hue_dist = min(abs(hue-centroid[0]), 360-abs(hue-centroid[0])) / 180.0
        sat_dist = abs(sat - centroid[1]) / 100.0
        bright_dist = abs(bright - centroid[2]) / 100.0

        distance = math.sqrt(hue_dist**2 + sat_dist**2 + bright_dist**2)

        distances_from_centroid.append(distance)
        shortest_distance = min(shortest_distance, distance)

    closest = []
    for idx, dist in enumerate(distances_from_centroid):
        if dist != shortest_distance:
            continue
        closest.append(hsv_color_type_matrix[idx])

    return closest
