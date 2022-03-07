"""!
#######################################################################
@author Al Timofeyev
@date   February 10, 2022
@brief  Utilities for extracting colors from the image.
#######################################################################
"""

# ---- IMPORTS ----
import numpy
import random
from . import constants as const


def extract_ratios(hsl_img_array):
    """!
    @brief  Extracts the ratios of hues per pixel.
    @param  hsl_img_array   2D Array of pixels in hsl array format.
    @return Dictionary of hue ratios (percentage) in set [0.000, 100.000]
    """
    pixels = 0
    red_pixel = 0
    yellow_pixel = 0
    green_pixel = 0
    cyan_pixel = 0
    blue_pixel = 0
    magenta_pixel = 0

    for pixel in hsl_img_array:
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
    red_ratio = round((red_pixel / pixels) * 100, 3)
    yellow_ration = round((yellow_pixel / pixels) * 100, 3)
    green_ration = round((green_pixel / pixels) * 100, 3)
    cyan_ratio = round((cyan_pixel / pixels) * 100, 3)
    blue_ratio = round((blue_pixel / pixels) * 100, 3)
    magenta_ratio = round((magenta_pixel / pixels) * 100, 3)

    # Assign the ratio dictionary.
    ratio_dict = {'Red': red_ratio, 'Yellow': yellow_ration, 'Green': green_ration,
                  'Cyan': cyan_ratio, 'Blue': blue_ratio, 'Magenta': magenta_ratio}

    return ratio_dict


# ***********************************************************************
# ***********************************************************************

def construct_base_color_dictionary(hsl_img_array):
    """!
    @brief  Constructs dictionary of base colors from array of hsl pixel values.
    @param  hsl_img_array   2D Array of pixels in hsl array format.
    @return Dictionary of base colors.
    """
    # Using index slicing since array is sorted, and it's much faster.
    start_idx, end_idx = 0, 0
    while end_idx < len(hsl_img_array) and (
            const.RED_HUE_RANGE_MIN[0] <= hsl_img_array[end_idx][0] < const.RED_HUE_RANGE_MIN[1]):
        end_idx += 1
    red = hsl_img_array[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsl_img_array) and (
            const.YELLOW_HUE_RANGE[0] <= hsl_img_array[end_idx][0] < const.YELLOW_HUE_RANGE[1]):
        end_idx += 1
    yellow = hsl_img_array[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsl_img_array) and (
            const.GREEN_HUE_RANGE[0] <= hsl_img_array[end_idx][0] < const.GREEN_HUE_RANGE[1]):
        end_idx += 1
    green = hsl_img_array[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsl_img_array) and (
            const.CYAN_HUE_RANGE[0] <= hsl_img_array[end_idx][0] < const.CYAN_HUE_RANGE[1]):
        end_idx += 1
    cyan = hsl_img_array[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsl_img_array) and (
            const.BLUE_HUE_RANGE[0] <= hsl_img_array[end_idx][0] < const.BLUE_HUE_RANGE[1]):
        end_idx += 1
    blue = hsl_img_array[start_idx:end_idx]

    start_idx = end_idx
    while end_idx < len(hsl_img_array) and (
            const.MAGENTA_HUE_RANGE[0] <= hsl_img_array[end_idx][0] < const.MAGENTA_HUE_RANGE[1]):
        end_idx += 1
    magenta = hsl_img_array[start_idx:end_idx]

    red = numpy.concatenate([red, hsl_img_array[end_idx:]]) # Remainder of colors are part of red.

    # Colors in each color array are sorted in ascending hue order (1st column).
    base_color_dict: dict[str, numpy.ndarray] = {'Red': red, 'Yellow': yellow, 'Green': green,
                                                 'Cyan': cyan, 'Blue': blue, 'Magenta': magenta}

    return base_color_dict


# ***********************************************************************
# ***********************************************************************

def check_missing_colors(base_color_dict):
    """!
    @brief  Checks for any missing colors in the base color dictionary and borrows them from the surrounding colors.
    @internal
    Example of colors on color wheel being shown in linear format:
    ________________________________________________________
    || (Left side)..........................(Right side)  ||
    || ---⦧-------⦧-------⦧------⦧------⦧-------⦧-----  ||
    || |.red...magenta...blue...cyan...green...yellow.|  ||
    || ----⦧-------⦧-------⦧------⦧-------⦧-------⦧--- ||
    || |.green...yellow...red...magenta...blue...cyan.| ||
    ------------------------------------------------------
    @endinternal
    @param  base_color_dict Dictionary with arrays of all the base colors.
    """
    if len(base_color_dict['Red']) == 0:
        base_color_dict['Red'] = borrow_for_color_red(base_color_dict, False, False)
    if len(base_color_dict['Cyan']) == 0:
        base_color_dict['Cyan'] = borrow_for_color_cyan(base_color_dict, False, False)
    if len(base_color_dict['Yellow']) == 0:
        base_color_dict['Yellow'] = borrow_for_color_yellow(base_color_dict, False, False)
    if len(base_color_dict['Blue']) == 0:
        base_color_dict['Blue'] = borrow_for_color_blue(base_color_dict, False, False)
    if len(base_color_dict['Green']) == 0:
        base_color_dict['Green'] = borrow_for_color_green(base_color_dict, False, False)
    if len(base_color_dict['Magenta']) == 0:
        base_color_dict['Magenta'] = borrow_for_color_magenta(base_color_dict, False, False)


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def borrow_for_color_red(base_color_dict, from_left, from_right):
    """!
    @brief  Borrows colors for the base color red.
    @param  base_color_dict Dictionary with arrays of all the base colors.
    @param  from_left   Boolean flag for recursive calls, if we came from the left.
    @param  from_right  Boolean flag for recursive calls, if we came from the right.
    @return A list/array sample of a potential color substitute.
    """
    potential_red_yel, potential_red_mag = [], []

    if not from_left and not from_right:  # ---- Coming from origin, borrow from left and right.
        sample_size = len(base_color_dict['Yellow'])
        borrowed_yellow = base_color_dict['Yellow']
        if sample_size == 0:  # ---- If no yellow color, borrow for yellow.
            borrowed_yellow = borrow_for_color_yellow(base_color_dict, from_left, True)
            sample_size = len(borrowed_yellow)
        elif sample_size > 1:
            sample_size //= 2
        potential_red_yel = numpy.array(borrowed_yellow[:sample_size])
        sample_size = len(base_color_dict['Magenta'])
        borrowed_magenta = base_color_dict['Magenta']
        if sample_size == 0:  # ---- If no magenta color, borrow for magenta.
            borrowed_magenta = borrow_for_color_magenta(base_color_dict, True, from_right)
            sample_size = len(borrowed_magenta)
        elif sample_size > 1:
            sample_size //= 2
        potential_red_mag = numpy.array(borrowed_magenta[-sample_size:])

    elif from_left:  # ---- Coming from left (yellow), borrow from right (magenta).
        sample_size = len(base_color_dict['Magenta'])
        borrowed_magenta = base_color_dict['Magenta']
        if sample_size == 0:  # ---- If no magenta color, borrow for magenta.
            borrowed_magenta = borrow_for_color_magenta(base_color_dict, True, from_right)
            sample_size = len(borrowed_magenta)
        elif sample_size > 1:
            sample_size //= 2
        potential_red_mag = numpy.array(borrowed_magenta[-sample_size:])

    elif from_right:  # ---- Coming from right (magenta), borrow from left (yellow).
        sample_size = len(base_color_dict['Yellow'])
        borrowed_yellow = base_color_dict['Yellow']
        if sample_size == 0:  # ---- If no yellow color, borrow for yellow.
            borrowed_yellow = borrow_for_color_yellow(base_color_dict, from_left, True)
            sample_size = len(borrowed_yellow)
        elif sample_size > 1:
            sample_size //= 2
        potential_red_yel = numpy.array(borrowed_yellow[:sample_size])

    # ---- Shift Hues.
    if len(potential_red_yel) != 0:
        yel_hue_column = potential_red_yel[:, 0] - 25
        yel_hue_column = [360 + x if x < 0 else x for x in yel_hue_column]
        potential_red_yel[:, 0] = yel_hue_column
    if len(potential_red_mag) != 0:
        mag_hue_column = potential_red_mag[:, 0] + 25
        mag_hue_column = [x % 360 for x in mag_hue_column]
        potential_red_mag[:, 0] = mag_hue_column

    # ---- If only one potential color has been borrowed, return it.
    if len(potential_red_yel) != 0 and len(potential_red_mag) == 0:
        return potential_red_yel
    elif len(potential_red_mag) != 0 and len(potential_red_yel) == 0:
        return potential_red_mag

    # ---- Calculate differences.
    yel_diff = abs(const.RED_HUE_MIN - potential_red_yel[0][0])     # Hue of first pixel [0] is closer to red min.
    mag_diff = abs(const.RED_HUE_MAX - potential_red_mag[-1][0])    # Hue of last pixel [-1] is closer to red max.

    # ---- Return the hue closest to red.
    if yel_diff < mag_diff:
        return potential_red_yel
    else:
        return potential_red_mag


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def borrow_for_color_yellow(base_color_dict, from_left, from_right):
    """!
    @brief  Borrows colors for the base color yellow.
    @param  base_color_dict Dictionary with arrays of all the base colors.
    @param  from_left   Boolean flag for recursive calls, if we came from the left.
    @param  from_right  Boolean flag for recursive calls, if we came from the right.
    @return A list/array sample of a potential color substitute.
    """
    potential_yel_grn, potential_yel_red = [], []

    if not from_left and not from_right:  # ---- Coming from origin, borrow from left and right.
        sample_size = len(base_color_dict['Green'])
        borrowed_green = base_color_dict['Green']
        if sample_size == 0:  # ---- If no green color, borrow for green.
            borrowed_green = borrow_for_color_green(base_color_dict, from_left, True)
            sample_size = len(borrowed_green)
        elif sample_size > 1:
            sample_size //= 2
        potential_yel_grn = numpy.array(borrowed_green[:sample_size])
        sample_size = len(base_color_dict['Red'])
        borrowed_red = base_color_dict['Red']
        if sample_size == 0:  # ---- If no red color, borrow for red.
            borrowed_red = borrow_for_color_red(base_color_dict, True, from_right)
            sample_size = len(borrowed_red)
        elif sample_size > 1:
            sample_size //= 2
        potential_yel_red = numpy.array(borrowed_red[-sample_size:])

    elif from_left:  # ---- Coming from left (green), borrow from right (red).
        sample_size = len(base_color_dict['Red'])
        borrowed_red = base_color_dict['Red']
        if sample_size == 0:  # ---- If no red color, borrow for red.
            borrowed_red = borrow_for_color_red(base_color_dict, True, from_right)
            sample_size = len(borrowed_red)
        elif sample_size > 1:
            sample_size //= 2
        potential_yel_red = numpy.array(borrowed_red[-sample_size:])

    elif from_right:  # ---- Coming from right (red), borrow from left (green).
        sample_size = len(base_color_dict['Green'])
        borrowed_green = base_color_dict['Green']
        if sample_size == 0:  # ---- If no green color, borrow for green.
            borrowed_green = borrow_for_color_green(base_color_dict, from_left, True)
            sample_size = len(borrowed_green)
        elif sample_size > 1:
            sample_size //= 2
        potential_yel_grn = numpy.array(borrowed_green[:sample_size])

    # ---- Shift Hues.
    if len(potential_yel_grn) != 0:
        grn_hue_column = potential_yel_grn[:, 0] - 25
        grn_hue_column = [360 + x if x < 0 else x for x in grn_hue_column]
        potential_yel_grn[:, 0] = grn_hue_column
    if len(potential_yel_red) != 0:
        red_hue_column = potential_yel_red[:, 0] + 25
        red_hue_column = [x % 360 for x in red_hue_column]
        potential_yel_red[:, 0] = red_hue_column

    # ---- If only one potential color has been borrowed, return it.
    if len(potential_yel_grn) != 0 and len(potential_yel_red) == 0:
        return potential_yel_grn
    elif len(potential_yel_red) != 0 and len(potential_yel_grn) == 0:
        return potential_yel_red

    # ---- Calculate differences.
    grn_diff = abs(const.YELLOW_HUE - potential_yel_grn[0][0])  # Hue of first pixel [0] is closer to yellow.
    red_diff = abs(const.YELLOW_HUE - potential_yel_red[-1][0]) # Hue of last pixel [-1] is closer to yellow.

    # ---- Return the hue closest to yellow.
    if grn_diff < red_diff:
        return potential_yel_grn
    else:
        return potential_yel_red


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def borrow_for_color_green(base_color_dict, from_left, from_right):
    """!
    @brief  Borrows colors for the base color green.
    @param  base_color_dict Dictionary with arrays of all the base colors.
    @param  from_left   Boolean flag for recursive calls, if we came from the left.
    @param  from_right  Boolean flag for recursive calls, if we came from the right.
    @return A list/array sample of a potential color substitute.
    """
    potential_grn_cyn, potential_grn_yel = [], []

    if not from_left and not from_right:  # ---- Coming from origin, borrow from left and right.
        sample_size = len(base_color_dict['Cyan'])
        borrowed_cyan = base_color_dict['Cyan']
        if sample_size == 0:  # ---- If no cyan color, borrow for cyan.
            borrowed_cyan = borrow_for_color_cyan(base_color_dict, from_left, True)
            sample_size = len(borrowed_cyan)
        elif sample_size > 1:
            sample_size //= 2
        potential_grn_cyn = numpy.array(borrowed_cyan[:sample_size])
        sample_size = len(base_color_dict['Yellow'])
        borrowed_yellow = base_color_dict['Yellow']
        if sample_size == 0:  # ---- If no yellow color, borrow for yellow.
            borrowed_yellow = borrow_for_color_yellow(base_color_dict, True, from_right)
            sample_size = len(borrowed_yellow)
        elif sample_size > 1:
            sample_size //= 2
        potential_grn_yel = numpy.array(borrowed_yellow[-sample_size:])

    elif from_left:  # ---- Coming from left (cyan), borrow from right (yellow).
        sample_size = len(base_color_dict['Yellow'])
        borrowed_yellow = base_color_dict['Yellow']
        if sample_size == 0:  # ---- If no yellow color, borrow for yellow.
            borrowed_yellow = borrow_for_color_yellow(base_color_dict, True, from_right)
            sample_size = len(borrowed_yellow)
        elif sample_size > 1:
            sample_size //= 2
        potential_grn_yel = numpy.array(borrowed_yellow[-sample_size:])

    elif from_right:  # ---- Coming from right (yellow), borrow from left (cyan).
        sample_size = len(base_color_dict['Cyan'])
        borrowed_cyan = base_color_dict['Cyan']
        if sample_size == 0:  # ---- If no cyan color, borrow for cyan.
            borrowed_cyan = borrow_for_color_cyan(base_color_dict, from_left, True)
            sample_size = len(borrowed_cyan)
        elif sample_size > 1:
            sample_size //= 2
        potential_grn_cyn = numpy.array(borrowed_cyan[:sample_size])

    # ---- Shift Hues.
    if len(potential_grn_cyn) != 0:
        cyn_hue_column = potential_grn_cyn[:, 0] - 25
        cyn_hue_column = [360 + x if x < 0 else x for x in cyn_hue_column]
        potential_grn_cyn[:, 0] = cyn_hue_column
    if len(potential_grn_yel) != 0:
        yel_hue_column = potential_grn_yel[:, 0] + 25
        yel_hue_column = [x % 360 for x in yel_hue_column]
        potential_grn_yel[:, 0] = yel_hue_column

    # ---- If only one potential color has been borrowed, return it.
    if len(potential_grn_cyn) != 0 and len(potential_grn_yel) == 0:
        return potential_grn_cyn
    elif len(potential_grn_yel) != 0 and len(potential_grn_cyn) == 0:
        return potential_grn_yel

    # ---- Calculate differences.
    cyn_diff = abs(const.GREEN_HUE - potential_grn_cyn[0][0])   # Hue of first pixel [0] is closer to green.
    yel_diff = abs(const.GREEN_HUE - potential_grn_yel[-1][0])  # Hue of last pixel [-1] is closer to green.

    # ---- Return the hue closest to green.
    if cyn_diff < yel_diff:
        return potential_grn_cyn
    else:
        return potential_grn_yel


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def borrow_for_color_cyan(base_color_dict, from_left, from_right):
    """!
    @brief  Borrows colors for the base color cyan.
    @param  base_color_dict Dictionary with arrays of all the base colors.
    @param  from_left   Boolean flag for recursive calls, if we came from the left.
    @param  from_right  Boolean flag for recursive calls, if we came from the right.
    @return A list/array sample of a potential color substitute.
    """
    potential_cyn_blu, potential_cyn_grn = [], []

    if not from_left and not from_right:  # ---- Coming from origin, borrow from left and right.
        sample_size = len(base_color_dict['Blue'])
        borrowed_blue = base_color_dict['Blue']
        if sample_size == 0:  # ---- If no blue color, borrow for blue.
            borrowed_blue = borrow_for_color_blue(base_color_dict, from_left, True)
            sample_size = len(borrowed_blue)
        elif sample_size > 1:
            sample_size //= 2
        potential_cyn_blu = numpy.array(borrowed_blue[:sample_size])
        sample_size = len(base_color_dict['Green'])
        borrowed_green = base_color_dict['Green']
        if sample_size == 0:  # ---- If no green color, borrow for green.
            borrowed_green = borrow_for_color_green(base_color_dict, True, from_right)
            sample_size = len(borrowed_green)
        elif sample_size > 1:
            sample_size //= 2
        potential_cyn_grn = numpy.array(borrowed_green[-sample_size:])

    elif from_left:  # ---- Coming from left (blue), borrow from right (green).
        sample_size = len(base_color_dict['Green'])
        borrowed_green = base_color_dict['Green']
        if sample_size == 0:  # ---- If no green color, borrow for green.
            borrowed_green = borrow_for_color_green(base_color_dict, True, from_right)
            sample_size = len(borrowed_green)
        elif sample_size > 1:
            sample_size //= 2
        potential_cyn_grn = numpy.array(borrowed_green[-sample_size:])

    elif from_right:  # ---- Coming from right (green), borrow from left (blue).
        sample_size = len(base_color_dict['Blue'])
        borrowed_blue = base_color_dict['Blue']
        if sample_size == 0:  # ---- If no blue color, borrow for blue.
            borrowed_blue = borrow_for_color_blue(base_color_dict, from_left, True)
            sample_size = len(borrowed_blue)
        elif sample_size > 1:
            sample_size //= 2
        potential_cyn_blu = numpy.array(borrowed_blue[:sample_size])

    # ---- Shift Hues.
    if len(potential_cyn_blu) != 0:
        blu_hue_column = potential_cyn_blu[:, 0] - 25
        blu_hue_column = [360 + x if x < 0 else x for x in blu_hue_column]
        potential_cyn_blu[:, 0] = blu_hue_column
    if len(potential_cyn_grn) != 0:
        grn_hue_column = potential_cyn_grn[:, 0] + 25
        grn_hue_column = [x % 360 for x in grn_hue_column]
        potential_cyn_grn[:, 0] = grn_hue_column

    # ---- If only one potential color has been borrowed, return it.
    if len(potential_cyn_blu) != 0 and len(potential_cyn_grn) == 0:
        return potential_cyn_blu
    elif len(potential_cyn_grn) != 0 and len(potential_cyn_blu) == 0:
        return potential_cyn_grn

    # ---- Calculate differences.
    blu_diff = abs(const.CYAN_HUE - potential_cyn_blu[0][0])  # Hue of first pixel [0] is closer to cyan.
    grn_diff = abs(const.CYAN_HUE - potential_cyn_grn[-1][0])  # Hue of last pixel [-1] is closer to cyan.

    # ---- Return the hue closest to cyan.
    if blu_diff < grn_diff:
        return potential_cyn_blu
    else:
        return potential_cyn_grn


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def borrow_for_color_blue(base_color_dict, from_left, from_right):
    """!
    @brief  Borrows colors for the base color blue.
    @param  base_color_dict Dictionary with arrays of all the base colors.
    @param  from_left   Boolean flag for recursive calls, if we came from the left.
    @param  from_right  Boolean flag for recursive calls, if we came from the right.
    @return A list/array sample of a potential color substitute.
    """
    potential_blu_mag, potential_blu_cyn = [], []

    if not from_left and not from_right:  # ---- Coming from origin, borrow from left and right.
        sample_size = len(base_color_dict['Magenta'])
        borrowed_magenta = base_color_dict['Magenta']
        if sample_size == 0:  # ---- If no magenta color, borrow for magenta.
            borrowed_magenta = borrow_for_color_magenta(base_color_dict, from_left, True)
            sample_size = len(borrowed_magenta)
        elif sample_size > 1:
            sample_size //= 2
        potential_blu_mag = numpy.array(borrowed_magenta[:sample_size])
        sample_size = len(base_color_dict['Cyan'])
        borrowed_cyan = base_color_dict['Cyan']
        if sample_size == 0:  # ---- If no cyan color, borrow for cyan.
            borrowed_cyan = borrow_for_color_cyan(base_color_dict, True, from_right)
            sample_size = len(borrowed_cyan)
        elif sample_size > 1:
            sample_size //= 2
        potential_blu_cyn = numpy.array(borrowed_cyan[-sample_size:])

    elif from_left:  # ---- Coming from left (magenta), borrow from right (cyan).
        sample_size = len(base_color_dict['Cyan'])
        borrowed_cyan = base_color_dict['Cyan']
        if sample_size == 0:  # ---- If no cyan color, borrow for cyan.
            borrowed_cyan = borrow_for_color_cyan(base_color_dict, True, from_right)
            sample_size = len(borrowed_cyan)
        elif sample_size > 1:
            sample_size //= 2
        potential_blu_cyn = numpy.array(borrowed_cyan[-sample_size:])

    elif from_right:  # ---- Coming from right (cyan), borrow from left (magenta).
        sample_size = len(base_color_dict['Magenta'])
        borrowed_magenta = base_color_dict['Magenta']
        if sample_size == 0:  # ---- If no magenta color, borrow for magenta.
            borrowed_magenta = borrow_for_color_magenta(base_color_dict, from_left, True)
            sample_size = len(borrowed_magenta)
        elif sample_size > 1:
            sample_size //= 2
        potential_blu_mag = numpy.array(borrowed_magenta[:sample_size])

    # ---- Shift Hues.
    if len(potential_blu_mag) != 0:
        mag_hue_column = potential_blu_mag[:, 0] - 25
        mag_hue_column = [360 + x if x < 0 else x for x in mag_hue_column]
        potential_blu_mag[:, 0] = mag_hue_column
    if len(potential_blu_cyn) != 0:
        cyn_hue_column = potential_blu_cyn[:, 0] + 25
        cyn_hue_column = [x % 360 for x in cyn_hue_column]
        potential_blu_cyn[:, 0] = cyn_hue_column

    # ---- If only one potential color has been borrowed, return it.
    if len(potential_blu_mag) != 0 and len(potential_blu_cyn) == 0:
        return potential_blu_mag
    elif len(potential_blu_cyn) != 0 and len(potential_blu_mag) == 0:
        return potential_blu_cyn

    # ---- Calculate differences.
    mag_diff = abs(const.BLUE_HUE - potential_blu_mag[0][0])    # Hue of first pixel [0] is closer to blue.
    cyn_diff = abs(const.BLUE_HUE - potential_blu_cyn[-1][0])   # Hue of last pixel [-1] is closer to blue.

    # ---- Return the hue closest to blue.
    if mag_diff < cyn_diff:
        return potential_blu_mag
    else:
        return potential_blu_cyn


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def borrow_for_color_magenta(base_color_dict, from_left, from_right):
    """!
    @brief  Borrows colors for the base color magenta.
    @param  base_color_dict Dictionary with arrays of all the base colors.
    @param  from_left   Boolean flag for recursive calls, if we came from the left.
    @param  from_right  Boolean flag for recursive calls, if we came from the right.
    @return A list/array sample of a potential color substitute.
    """
    potential_mag_red, potential_mag_blue = [], []

    if not from_left and not from_right:  # ---- Coming from origin, borrow from left and right.
        sample_size = len(base_color_dict['Red'])
        borrowed_red = base_color_dict['Red']
        if sample_size == 0:  # ---- If no red color, borrow for red.
            borrowed_red = borrow_for_color_red(base_color_dict, from_left, True)
            sample_size = len(borrowed_red)
        elif sample_size > 1:
            sample_size //= 2
        potential_mag_red = numpy.array(borrowed_red[:sample_size])
        sample_size = len(base_color_dict['Blue'])
        borrowed_blue = base_color_dict['Blue']
        if sample_size == 0:  # ---- If no blue color, borrow for blue.
            borrowed_blue = borrow_for_color_blue(base_color_dict, True, from_right)
            sample_size = len(borrowed_blue)
        elif sample_size > 1:
            sample_size //= 2
        potential_mag_blue = numpy.array(borrowed_blue[-sample_size:])

    elif from_left:  # ---- Coming from left (red), borrow from right (blue).
        sample_size = len(base_color_dict['Blue'])
        borrowed_blue = base_color_dict['Blue']
        if sample_size == 0:  # ---- If no blue color, borrow for blue.
            borrowed_blue = borrow_for_color_blue(base_color_dict, True, from_right)
            sample_size = len(borrowed_blue)
        elif sample_size > 1:
            sample_size //= 2
        potential_mag_blue = numpy.array(borrowed_blue[-sample_size:])

    elif from_right:  # ---- Coming from right (blue), borrow from left (red).
        sample_size = len(base_color_dict['Red'])
        borrowed_red = base_color_dict['Red']
        if sample_size == 0:  # ---- If no red color, borrow for red.
            borrowed_red = borrow_for_color_red(base_color_dict, from_left, True)
            sample_size = len(borrowed_red)
        elif sample_size > 1:
            sample_size //= 2
        potential_mag_red = numpy.array(borrowed_red[:sample_size])

    # ---- Shift Hues.
    if len(potential_mag_red) != 0:
        red_hue_column = potential_mag_red[:, 0] - 25
        red_hue_column = [360 + x if x < 0 else x for x in red_hue_column]
        potential_mag_red[:, 0] = red_hue_column
    if len(potential_mag_blue) != 0:
        blu_hue_column = potential_mag_blue[:, 0] + 25
        blu_hue_column = [x % 360 for x in blu_hue_column]
        potential_mag_blue[:, 0] = blu_hue_column

    # ---- If only one potential color has been borrowed, return it.
    if len(potential_mag_red) != 0 and len(potential_mag_blue) == 0:
        return potential_mag_red
    elif len(potential_mag_blue) != 0 and len(potential_mag_red) == 0:
        return potential_mag_blue

    # ---- Calculate differences.
    red_diff = abs(const.MAGENTA_HUE - potential_mag_red[0][0])     # Hue of first pixel [0] is closer to magenta.
    blue_diff = abs(const.MAGENTA_HUE - potential_mag_blue[-1][0])  # Hue of last pixel [-1] is closer to magenta.

    # ---- Return the hue closest to magenta.
    if red_diff < blue_diff:
        return potential_mag_red
    else:
        return potential_mag_blue


# ***********************************************************************
# ***********************************************************************

def extract_dominant_colors(base_color_dict):
    """!
    @brief  Extracts dominant light, normal, dark colors from each of the base colors.
    @param  base_color_dict Dictionary with arrays of all the base colors.
    @return Dictionary of light, normal, dark colors for each of the base colors.
    """
    dominant_red_colors = extract_colors(base_color_dict['Red'])
    dominant_yellow_colors = extract_colors(base_color_dict['Yellow'])
    dominant_green_colors = extract_colors(base_color_dict['Green'])
    dominant_cyan_colors = extract_colors(base_color_dict['Cyan'])
    dominant_blue_colors = extract_colors(base_color_dict['Blue'])
    dominant_magenta_colors = extract_colors(base_color_dict['Magenta'])

    light_red_hsl_color, norm_red_hsl_color, dark_red_hsl_color = dominant_red_colors
    light_yellow_hsl_color, norm_yellow_hsl_color, dark_yellow_hsl_color = dominant_yellow_colors
    light_green_hsl_color, norm_green_hsl_color, dark_green_hsl_color = dominant_green_colors
    light_cyan_hsl_color, norm_cyan_hsl_color, dark_cyan_hsl_color = dominant_cyan_colors
    light_blue_hsl_color, norm_blue_hsl_color, dark_blue_hsl_color = dominant_blue_colors
    light_magenta_hsl_color, norm_magenta_hsl_color, dark_magenta_hsl_color = dominant_magenta_colors

    dom_color_dict: dict[str, list] = {'Light Red': light_red_hsl_color, 'Light Yellow': light_yellow_hsl_color,
                                       'Light Green': light_green_hsl_color, 'Light Cyan': light_cyan_hsl_color,
                                       'Light Blue': light_blue_hsl_color, 'Light Magenta': light_magenta_hsl_color,
                                       'Normal Red': norm_red_hsl_color, 'Normal Yellow': norm_yellow_hsl_color,
                                       'Normal Green': norm_green_hsl_color, 'Normal Cyan': norm_cyan_hsl_color,
                                       'Normal Blue': norm_blue_hsl_color, 'Normal Magenta': norm_magenta_hsl_color,
                                       'Dark Red': dark_red_hsl_color, 'Dark Yellow': dark_yellow_hsl_color,
                                       'Dark Green': dark_green_hsl_color, 'Dark Cyan': dark_cyan_hsl_color,
                                       'Dark Blue': dark_blue_hsl_color, 'Dark Magenta': dark_magenta_hsl_color
                                       }
    return dom_color_dict


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def extract_colors(hsl_base_color_array):
    """!
    @brief  Extracts the dominant light, normal, dark colors from the color array.
    @param  hsl_base_color_array    2D Array of hsl colors from one of the base colors.
    @return List/Array of dominant light, normal, dark colors in hsl format.
    """
    light_colors, norm_colors, dark_colors = sort_by_light_value(hsl_base_color_array)
    light_color = extract_dominant_color(light_colors)
    norm_color = extract_dominant_color(norm_colors)
    dark_color = extract_dominant_color(dark_colors)

    check_sat_and_light(light_color)
    check_sat_and_light(norm_color)
    check_sat_and_light(dark_color)
    check_colors(light_color, norm_color, dark_color)
    check_sat_and_light(light_color)
    check_sat_and_light(norm_color)
    check_sat_and_light(dark_color)

    return [light_color, norm_color, dark_color]


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def sort_by_light_value(hsl_base_color_array):
    """!
    @brief  Sorts the colors array by the lightness value and returns three separate color arrays.
    @param  hsl_base_color_array    2D Array of hsl colors from one of the base colors.
    @return List/Array of light, normal, and dark colors from the array of hsl colors.
    """
    light_colors = []
    norm_colors = []
    dark_colors = []

    for pixel in hsl_base_color_array:
        lit = pixel[2]
        if lit >= const.WHITE_LIGHT_RANGE[0]:   # -------- If light color.
            light_colors.append(pixel)
        elif lit >= const.GRAY_LIGHT_RANGE[0]:  # -------- If normal color.
            norm_colors.append(pixel)
        else:                                   # -------- If dark color.
            dark_colors.append(pixel)

    return [numpy.asarray(light_colors), numpy.asarray(norm_colors), numpy.asarray(dark_colors)]


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def extract_dominant_color(hsl_colors):
    """!
    @brief  Extracts the dominant color from the hsl color array.
    @param  hsl_colors  2D Array of hsl colors from one of the base colors [Red, Green, Blue, etc.].
    @return A dominant color list/array in hsl format [h, s, l].
    """
    dom_colors = get_dom_hue_colors(hsl_colors) # Get colors with dominant hues from hsl_colors.
    dom_colors = dom_colors[dom_colors[:, 1].argsort(axis=0)]   # Sort by 2nd column (s).
    dom_colors = get_dom_sat_colors(dom_colors) # Get colors with dominant saturation from dom_colors.
    dom_colors = dom_colors[dom_colors[:, 2].argsort(axis=0)]   # Sort by 3rd column (l).
    dom_colors = get_dom_lit_colors(dom_colors) # Get colors with dominant lightness from dom_colors.
    dom_colors = dom_colors[dom_colors[:, 0].argsort(axis=0)]   # Sort by 1st column (h).

    if len(dom_colors) == 0:
        dom_color = numpy.array([-1.0, -1.0, -1.0])
    else:
        dom_color = dom_colors[numpy.random.choice(len(dom_colors))]

    return dom_color


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def get_dom_hue_colors(hsl_colors):
    """!
    @brief  Construct list/array of a base color with the dominant hue.
    @details    Example: From the hsl_colors array, there could be 10 hues that
                appear 4 times each, while the rest of the hues appear only once or
                twice. The hsl_colors with these 10 hues will be extracted and
                returned because they appear the most and are therefore the dominant hues.
    @param  hsl_colors  2D Array of hsl colors from one of the base colors [Red, Green, Blue, etc.].
    @return List/array of all hsl colors that had the dominant number of hue values.
    """
    hue_pixel_dict: dict[int, numpy.ndarray] = {}
    hue_dict: [int, int] = {}
    dom_hue_count = 0

    start_idx, end_idx = 0, 0
    while start_idx < (len(hsl_colors)):  # ---- Determine the count of the dominant hues.
        current_hue = hsl_colors[start_idx][0]
        while end_idx < len(hsl_colors) and hsl_colors[end_idx][0] == current_hue:
            end_idx += 1

        if end_idx >= len(hsl_colors):
            hue_pixel_dict[current_hue] = numpy.array(hsl_colors[start_idx:])
        else:
            hue_pixel_dict[current_hue] = numpy.array(hsl_colors[start_idx:end_idx])

        hue_dict[current_hue] = len(hue_pixel_dict[current_hue])
        if hue_dict[current_hue] > dom_hue_count:
            dom_hue_count = hue_dict[current_hue]

        start_idx = end_idx

    if not hue_pixel_dict:  # If there were no colors saved.
        return numpy.empty((0, 3), list)

    # Construct 2D hsl list/array of colors with dominant hues.
    dom_hue_colors = numpy.empty((0, 3), list)
    for key, value in hue_dict.items():
        if value == dom_hue_count:
            dom_hue_colors = numpy.append(dom_hue_colors, hue_pixel_dict[key], axis=0)

    return dom_hue_colors


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def get_dom_sat_colors(hsl_colors):
    """!
    @brief  Construct list/array of a base color with the dominant saturation.
    @details    Example: From the hsl_colors array, there could be 5 saturation values
                that appear 12 times each, while the rest of the saturation values
                appear only once or twice. The hsl_colors with these 5 saturation
                values will be extracted and returned because they appear the most
                and are therefore the dominant saturation values.
    @param  hsl_colors  2D Array of hsl colors from one of the base colors [Red, Green, Blue, etc.].
    @return List/array of all hsl colors that had the dominant number of saturation values.
    """
    sat_pixel_dict: dict[int, numpy.ndarray] = {}
    sat_dict: [int, int] = {}
    dom_sat_count = 0

    start_idx, end_idx = 0, 0
    while start_idx < (len(hsl_colors)):  # ---- Determine the count of the dominant saturations.
        current_sat = hsl_colors[start_idx][1]
        while end_idx < len(hsl_colors) and hsl_colors[end_idx][1] == current_sat:
            end_idx += 1

        if end_idx >= len(hsl_colors):
            sat_pixel_dict[current_sat] = numpy.array(hsl_colors[start_idx:])
        else:
            sat_pixel_dict[current_sat] = numpy.array(hsl_colors[start_idx:end_idx])

        sat_dict[current_sat] = len(sat_pixel_dict[current_sat])
        if sat_dict[current_sat] > dom_sat_count:
            dom_sat_count = sat_dict[current_sat]

        start_idx = end_idx

    if not sat_pixel_dict:  # If there were no colors saved.
        return numpy.empty((0, 3), list)

    # Construct 2D hsl list/array of colors with dominant saturations.
    dom_sat_colors = numpy.empty((0, 3), list)
    for key, value in sat_dict.items():
        if value == dom_sat_count:
            dom_sat_colors = numpy.append(dom_sat_colors, sat_pixel_dict[key], axis=0)

    return dom_sat_colors


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def get_dom_lit_colors(hsl_colors):
    """!
    @brief  Construct list/array of a base color with the dominant lightness.
    @details    Example: From the hsl_colors array, there could be 2 lightness values
                that appear 8 times each, while the rest of the lightness values
                appear only once or twice. The hsl_colors with these 2 lightness
                values will be extracted and returned because they appear the most
                and are therefore the dominant lightness values.
    @param  hsl_colors  2D Array of hsl colors from one of the base colors [Red, Green, Blue, etc.].
    @return List/array of all hsl colors that had the dominant number of lightness values.
    """
    lit_pixel_dict: dict[int, numpy.ndarray] = {}
    lit_dict: [int, int] = {}
    dom_lit_count = 0

    start_idx, end_idx = 0, 0
    while start_idx < (len(hsl_colors)):  # ---- Determine the count of the dominant lightness.
        current_lit = hsl_colors[start_idx][2]
        while end_idx < len(hsl_colors) and hsl_colors[end_idx][2] == current_lit:
            end_idx += 1

        if end_idx >= len(hsl_colors):
            lit_pixel_dict[current_lit] = numpy.array(hsl_colors[start_idx:])
        else:
            lit_pixel_dict[current_lit] = numpy.array(hsl_colors[start_idx:end_idx])

        lit_dict[current_lit] = len(lit_pixel_dict[current_lit])
        if lit_dict[current_lit] > dom_lit_count:
            dom_lit_count = lit_dict[current_lit]

        start_idx = end_idx

    if not lit_pixel_dict:  # If there were no colors saved.
        return numpy.empty((0, 3), list)

    # Construct 2D hsl list/array of colors with dominant lightness.
    dom_lit_colors = numpy.empty((0, 3), list)
    for key, value in lit_dict.items():
        if value == dom_lit_count:
            dom_lit_colors = numpy.append(dom_lit_colors, lit_pixel_dict[key], axis=0)

    return dom_lit_colors


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def check_colors(light_color, norm_color, dark_color):
    """!
    @brief  Checks to make sure all the color types have been properly set by <extract_colors()> function.
    @param  light_color Light hsl color.
    @param  norm_color  Normal hsl color.
    @param  dark_color  Dark hsl color.
    """
    has_light = light_color[0] != -1
    has_norm = norm_color[0] != -1
    has_dark = dark_color[0] != -1

    # Check and set dark color.
    if not has_dark:
        if has_light:
            dark_color[0] = light_color[0]
            sat_diff = light_color[1] / 2 if light_color[1] < 50 else (100 - light_color[1]) / 2
            sat_diff = round(sat_diff, 1)
            dark_color[1] = light_color[1] + sat_diff if light_color[1] < 50 else light_color[1] - sat_diff
            dark_color[2] = 100 - light_color[2] + round(random.uniform(-5.0, 5.0), 1)
        elif has_norm:
            dark_color[0] = norm_color[0]
            sat_diff = norm_color[1] / 2 if norm_color[1] < 50 else (100 - norm_color[1]) / 2
            sat_diff = round(sat_diff, 1)
            dark_color[1] = norm_color[1] + sat_diff if norm_color[1] < 50 else norm_color[1] - sat_diff
            # dark_color[1] = norm_color[1] - sat_diff
            light_diff = norm_color[2] / 2 if norm_color[2] < 50 else (100 - norm_color[2]) / 2
            light_diff = round(light_diff, 1)
            dark_color[2] = norm_color[2] - light_diff
        # check_sat_and_light(dark_color)

    # Check and set light color.
    if not has_light:
        if has_dark:
            light_color[0] = dark_color[0]
            sat_diff = dark_color[1] / 2 if dark_color[1] < 50 else (100 - dark_color[1]) / 2
            sat_diff = round(sat_diff, 1)
            light_color[1] = dark_color[1] + sat_diff if dark_color[1] < 50 else dark_color[1] - sat_diff
            light_color[2] = 100 - dark_color[2] + round(random.uniform(-5.0, 5.0), 1)
        elif has_norm:
            light_color[0] = norm_color[0]
            sat_diff = norm_color[1] / 2 if norm_color[1] < 50 else (100 - norm_color[1]) / 2
            sat_diff = round(sat_diff, 1)
            light_color[1] = norm_color[1] + sat_diff if norm_color[1] < 50 else norm_color[1] - sat_diff
            # light_color[1] = norm_color[1] + sat_diff
            light_diff = norm_color[2] / 2 if norm_color[2] < 50 else (100 - norm_color[2]) / 2
            light_diff = round(light_diff, 1)
            light_color[2] = norm_color[2] + light_diff
        # check_sat_and_light(light_color)

    # Check and set normal color
    if not has_norm:
        hue_diff = round(abs((light_color[0] - dark_color[0]) / 2))
        sat_diff = round(abs(light_color[1] - dark_color[1]) / 2, 1)
        light_diff = round((light_color[2] - dark_color[2]) / 2, 1)
        norm_color[0] = (dark_color[0] + hue_diff) if dark_color[0] < light_color[0] else (
                light_color[0] + hue_diff)
        norm_color[0] %= 360
        norm_color[1] = (dark_color[1] + sat_diff) if dark_color[1] < light_color[1] else (
                light_color[1] + sat_diff)
        norm_color[2] = dark_color[2] + light_diff
        # check_sat_and_light(norm_color)


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def check_sat_and_light(hsl_color):
    """!
    @brief  Normalize saturation and lightness so that saturation isn't
            completely 0% and that lightness isn't 0% or 100%.
    @param  hsl_color   An hsl color in list/array format [h, s, l].
    """
    # Edge case, don't do this for values of [-1, -1, -1]
    if hsl_color[0] == -1:
        return

    # Check and re-set saturation.
    if hsl_color[1] < 5:
        hsl_color[1] = round(random.uniform(5.0, 10.0), 1)

    # Check and re-set lightness.
    if hsl_color[2] > 95:
        hsl_color[2] = round(random.uniform(85.0, 95.0), 1)
    elif hsl_color[2] < 5:
        hsl_color[2] = round(random.uniform(5.0, 10.0), 1)


# ***********************************************************************
# ***********************************************************************

def generate_remaining_colors(dom_color_dict, ratios):
    """!
    @brief  Generate the remaining black and white, and background and foreground colors.
    @param  dom_color_dict  Dictionary of dominant light, normal, dark base colors.
    @param  ratios  Dictionary of ratios of the base colors in image.
    """
    # Get the most and least dominant colors.
    most_dom_color, least_dom_color = get_color_extremes(ratios)
    black_colors, white_colors = generate_black_and_white(dom_color_dict["Normal " + most_dom_color])
    light_theme, norm_theme, dark_theme = generate_background_and_foreground(
        dom_color_dict["Normal " + most_dom_color], dom_color_dict["Normal " + least_dom_color])

    light_black, norm_black, dark_black = black_colors
    light_white, norm_white, dark_white = white_colors
    light_background, light_foreground = light_theme
    norm_background, norm_foreground = norm_theme
    dark_background, dark_foreground = dark_theme

    dom_color_dict["Light Black"] = light_black
    dom_color_dict["Normal Black"] = norm_black
    dom_color_dict["Dark Black"] = dark_black
    dom_color_dict["Light White"] = light_white
    dom_color_dict["Normal White"] = norm_white
    dom_color_dict["Dark White"] = dark_white
    dom_color_dict["Light Background"] = light_background
    dom_color_dict["Light Foreground"] = light_foreground
    dom_color_dict["Normal Background"] = norm_background
    dom_color_dict["Normal Foreground"] = norm_foreground
    dom_color_dict["Dark Background"] = dark_background
    dom_color_dict["Dark Foreground"] = dark_foreground


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def get_color_extremes(ratios):
    """!
    @brief  Determines the most and least dominant color in the image.
    @param  ratios  Dictionary of ratios of the base colors in image.
    @return List/array of most and least dominant color as strings.
    """
    most_dom_color_percentage = 0.0
    least_dom_color_percentage = 100.0
    most_dom_color_array = []
    least_dom_color_array = []

    for key, value in ratios.items():
        if value == most_dom_color_percentage:
            most_dom_color_array.append(key)
        elif value > most_dom_color_percentage:
            most_dom_color_percentage = value
            most_dom_color_array.clear()
            most_dom_color_array.append(key)

        if value == least_dom_color_percentage:
            least_dom_color_array.append(key)
        elif value < least_dom_color_percentage:
            least_dom_color_percentage = value
            least_dom_color_array.clear()
            least_dom_color_array.append(key)

    # Set the most and least dominant colors.
    if len(most_dom_color_array) == 1:
        most_dom_color = most_dom_color_array[0]
    else:
        index = random.randrange(len(most_dom_color_array) - 1)
        most_dom_color = most_dom_color_array[index]
    if len(least_dom_color_array) == 1:
        least_dom_color = least_dom_color_array[0]
    else:
        index = random.randrange(len(least_dom_color_array) - 1)
        least_dom_color = least_dom_color_array[index]

    return [most_dom_color, least_dom_color]


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def generate_black_and_white(hsl_color):
    """!
    @brief  Generate a black and white color using the hsl_color.
    @param  hsl_color   The hsl color array from which to generate black and white.
    @return List/array of light, normal, dark black and white hsl colors.
    """
    black_color = numpy.zeros(3, dtype=float)
    white_color = numpy.zeros(3, dtype=float)

    black_color[0] = hsl_color[0]
    black_color[1] = 60.0
    black_color[2] = 10.0
    white_color[0] = hsl_color[0]
    white_color[1] = 10.0
    white_color[2] = 85.0

    light_black_color = numpy.array([-1.0, -1.0, -1.0])
    dark_black_color = numpy.array([-1.0, -1.0, -1.0])
    light_white_color = numpy.array([-1.0, -1.0, -1.0])
    dark_white_color = numpy.array([-1.0, -1.0, -1.0])

    check_colors(light_black_color, black_color, dark_black_color)
    check_colors(light_white_color, white_color, dark_white_color)

    return [[light_black_color, black_color, dark_black_color], [light_white_color, white_color, dark_white_color]]


# ---------------------------------------------------------------
# ---------------------------------------------------------------

def generate_background_and_foreground(most_dom_hsl_color, least_dom_hsl_color):
    """!
    @brief  Generates the background and foreground colors based on the most and least dominant colors.
    @param  most_dom_hsl_color  The hsl color array from which to generate background.
    @param  least_dom_hsl_color The hsl color array from which to generate foreground.
    @return List/array of background and foreground hsl colors.
    """
    light_background_color = numpy.zeros(3, dtype=float)
    light_foreground_color = numpy.zeros(3, dtype=float)
    norm_background_color = numpy.zeros(3, dtype=float)
    norm_foreground_color = numpy.zeros(3, dtype=float)
    dark_background_color = numpy.zeros(3, dtype=float)
    dark_foreground_color = numpy.zeros(3, dtype=float)

    light_background_color[0] = most_dom_hsl_color[0]
    light_background_color[1] = 15.0
    light_background_color[2] = 90.0
    light_foreground_color[0] = least_dom_hsl_color[0]
    light_foreground_color[1] = 10.0
    light_foreground_color[2] = 15.0

    norm_background_color[0] = most_dom_hsl_color[0]
    norm_background_color[1] = 10.0
    norm_background_color[2] = 60.0
    norm_foreground_color[0] = least_dom_hsl_color[0]
    norm_foreground_color[1] = 42.0
    norm_foreground_color[2] = 88.0

    dark_background_color[0] = most_dom_hsl_color[0]
    dark_background_color[1] = 10.0
    dark_background_color[2] = 15.0
    dark_foreground_color[0] = least_dom_hsl_color[0]
    dark_foreground_color[1] = 15.0
    dark_foreground_color[2] = 90.0

    return [[light_background_color, light_foreground_color], [norm_background_color, norm_foreground_color],
            [dark_background_color, dark_foreground_color]]

# ***********************************************************************
# ***********************************************************************
