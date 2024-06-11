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
    ratio_dict = {'Red': red_ratio, 'Yellow': yellow_ration, 'Green': green_ration,
                  'Cyan': cyan_ratio, 'Blue': blue_ratio, 'Magenta': magenta_ratio}

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
    base_color_dict = {'Red': red, 'Yellow': yellow, 'Green': green,
                       'Cyan': cyan, 'Blue': blue, 'Magenta': magenta}

    return base_color_dict


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Extracts dominant light, normal, dark color palettes from each of the base colors.
#
#   @param  base_color_dict A dictionary of 2D numpy arrays for each of the base colors.
#
#   @return Dictionary of light, normal, dark color palettes for each of the base colors.
def extract_color_palettes(base_color_dict):
    base_colors = [base_color_dict['Red'], base_color_dict['Yellow'], base_color_dict['Green'],
                   base_color_dict['Cyan'], base_color_dict['Blue'], base_color_dict['Magenta']]

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

    extracted_colors_dict = {'Light Red': light_red_hsv_color, 'Light Yellow': light_yellow_hsv_color,
                             'Light Green': light_green_hsv_color, 'Light Cyan': light_cyan_hsv_color,
                             'Light Blue': light_blue_hsv_color, 'Light Magenta': light_magenta_hsv_color,
                             'Normal Red': norm_red_hsv_color, 'Normal Yellow': norm_yellow_hsv_color,
                             'Normal Green': norm_green_hsv_color, 'Normal Cyan': norm_cyan_hsv_color,
                             'Normal Blue': norm_blue_hsv_color, 'Normal Magenta': norm_magenta_hsv_color,
                             'Dark Red': dark_red_hsv_color, 'Dark Yellow': dark_yellow_hsv_color,
                             'Dark Green': dark_green_hsv_color, 'Dark Cyan': dark_cyan_hsv_color,
                             'Dark Blue': dark_blue_hsv_color, 'Dark Magenta': dark_magenta_hsv_color
                             }

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
    if len(base_color_dict['Red']) == 0:
        left_color, right_color = get_left_and_right_colors('Light Red')
        extracted_colors_dict['Light Red'] = borrow_color(extracted_colors_dict, 'Light Red', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('Normal Red')
        extracted_colors_dict['Normal Red'] = borrow_color(extracted_colors_dict, 'Normal Red', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('Dark Red')
        extracted_colors_dict['Dark Red'] = borrow_color(extracted_colors_dict, 'Dark Red', left_color, right_color)

    if len(base_color_dict['Yellow']) == 0:
        left_color, right_color = get_left_and_right_colors('Light Yellow')
        extracted_colors_dict['Light Yellow'] = borrow_color(extracted_colors_dict, 'Light Yellow', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('Normal Yellow')
        extracted_colors_dict['Normal Yellow'] = borrow_color(extracted_colors_dict, 'Normal Yellow', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('Dark Yellow')
        extracted_colors_dict['Dark Yellow'] = borrow_color(extracted_colors_dict, 'Dark Yellow', left_color, right_color)

    if len(base_color_dict['Green']) == 0:
        left_color, right_color = get_left_and_right_colors('Light Green')
        extracted_colors_dict['Light Green'] = borrow_color(extracted_colors_dict, 'Light Green', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('Normal Green')
        extracted_colors_dict['Normal Green'] = borrow_color(extracted_colors_dict, 'Normal Green', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('Dark Green')
        extracted_colors_dict['Dark Green'] = borrow_color(extracted_colors_dict, 'Dark Green', left_color, right_color)

    if len(base_color_dict['Cyan']) == 0:
        left_color, right_color = get_left_and_right_colors('Light Cyan')
        extracted_colors_dict['Light Cyan'] = borrow_color(extracted_colors_dict, 'Light Cyan', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('Normal Cyan')
        extracted_colors_dict['Normal Cyan'] = borrow_color(extracted_colors_dict, 'Normal Cyan', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('Dark Cyan')
        extracted_colors_dict['Dark Cyan'] = borrow_color(extracted_colors_dict, 'Dark Cyan', left_color, right_color)

    if len(base_color_dict['Blue']) == 0:
        left_color, right_color = get_left_and_right_colors('Light Blue')
        extracted_colors_dict['Light Blue'] = borrow_color(extracted_colors_dict, 'Light Blue', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('Normal Blue')
        extracted_colors_dict['Normal Blue'] = borrow_color(extracted_colors_dict, 'Normal Blue', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('Dark Blue')
        extracted_colors_dict['Dark Blue'] = borrow_color(extracted_colors_dict, 'Dark Blue', left_color, right_color)

    if len(base_color_dict['Magenta']) == 0:
        left_color, right_color = get_left_and_right_colors('Light Magenta')
        extracted_colors_dict['Light Magenta'] = borrow_color(extracted_colors_dict, 'Light Magenta', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('Normal Magenta')
        extracted_colors_dict['Normal Magenta'] = borrow_color(extracted_colors_dict, 'Normal Magenta', left_color, right_color)
        left_color, right_color = get_left_and_right_colors('Dark Magenta')
        extracted_colors_dict['Dark Magenta'] = borrow_color(extracted_colors_dict, 'Dark Magenta', left_color, right_color)


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

    extracted_colors_dict["Light Black"] = light_black
    extracted_colors_dict["Normal Black"] = norm_black
    extracted_colors_dict["Dark Black"] = dark_black
    extracted_colors_dict["Light White"] = light_white
    extracted_colors_dict["Normal White"] = norm_white
    extracted_colors_dict["Dark White"] = dark_white

    extracted_colors_dict["Light Background"] = light_background
    extracted_colors_dict["Light Foreground"] = light_foreground
    extracted_colors_dict["Dark Background"] = dark_background
    extracted_colors_dict["Dark Foreground"] = dark_foreground


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
    if origin_color_name == 'Light Red':
        return ['Light Yellow', 'Light Magenta']
    elif origin_color_name == 'Normal Red':
        return ['Normal Yellow', 'Normal Magenta']
    elif origin_color_name == 'Dark Red':
        return ['Dark Yellow', 'Dark Magenta']
    elif origin_color_name == 'Light Yellow':
        return ['Light Green', 'Light Red']
    elif origin_color_name == 'Normal Yellow':
        return ['Normal Green', 'Normal Red']
    elif origin_color_name == 'Dark Yellow':
        return ['Dark Green', 'Dark Red']
    elif origin_color_name == 'Light Green':
        return ['Light Cyan', 'Light Yellow']
    elif origin_color_name == 'Normal Green':
        return ['Normal Cyan', 'Normal Yellow']
    elif origin_color_name == 'Dark Green':
        return ['Dark Cyan', 'Dark Yellow']
    elif origin_color_name == 'Light Cyan':
        return ['Light Blue', 'Light Green']
    elif origin_color_name == 'Normal Cyan':
        return ['Normal Blue', 'Normal Green']
    elif origin_color_name == 'Dark Cyan':
        return ['Dark Blue', 'Dark Green']
    elif origin_color_name == 'Light Blue':
        return ['Light Magenta', 'Light Cyan']
    elif origin_color_name == 'Normal Blue':
        return ['Normal Magenta', 'Normal Cyan']
    elif origin_color_name == 'Dark Blue':
        return ['Dark Magenta', 'Dark Cyan']
    elif origin_color_name == 'Light Magenta':
        return ['Light Red', 'Light Blue']
    elif origin_color_name == 'Normal Magenta':
        return ['Normal Red', 'Normal Blue']
    elif origin_color_name == 'Dark Magenta':
        return ['Dark Red', 'Dark Blue']


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
    if origin == 'Light Red' or origin == 'Normal Red' or origin == 'Dark Red':
        optimal_hue = const.RED_HUE
    elif origin == 'Light Yellow' or origin == 'Normal Yellow' or origin == 'Dark Yellow':
        optimal_hue = const.YELLOW_HUE
    elif origin == 'Light Green' or origin == 'Normal Green' or origin == 'Dark Green':
        optimal_hue = const.GREEN_HUE
    elif origin == 'Light Cyan' or origin == 'Normal Cyan' or origin == 'Dark Cyan':
        optimal_hue = const.CYAN_HUE
    elif origin == 'Light Blue' or origin == 'Normal Blue' or origin == 'Dark Blue':
        optimal_hue = const.BLUE_HUE
    elif origin == 'Light Magenta' or origin == 'Normal Magenta' or origin == 'Dark Magenta':
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

    light_hue, temp_sat1, temp_bright1 = extracted_colors_dict["Light " + dominant_color_name]
    norm_hue, temp_sat2, temp_bright2 = extracted_colors_dict["Normal " + dominant_color_name]
    dark_hue, temp_sat3, temp_bright3 = extracted_colors_dict["Dark " + dominant_color_name]

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
