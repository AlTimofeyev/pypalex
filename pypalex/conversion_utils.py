##  @file   conversion_utils.py
#   @brief  Utilities for converting between RGB, HSV, HEX.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on February 2, 2022.
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 6, 2023.
#   - Modified by Al Timofeyev on April 5, 2023.
#   - Modified by Al Timofeyev on July 8, 2024.
#   - Modified by Al Timofeyev on October 12, 2024.


##  Convert HSV array [h,s,v] to HEX string '#ffffff'.
#   @details    HSV where h is in the set [0, 359] and s, v are in the set [0.0, 100.0].
#               HEX string is in the set ["#000000", "#ffffff"].
#
#   @param  hsv_array   HSV array [h,s,v].
#
#   @return A HEX string.
def hsv_to_hex(hsv_array):
    rgb_array = hsv_to_rgb(hsv_array)
    return rgb_to_hex(rgb_array)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Convert HEX string '#ffffff' to HSV array [h,s,v].
#   @details    HEX string is in the set ["#000000", "#ffffff"].
#               HSV where h is in the set [0, 359] and s, v are in the set [0.0, 100.0].
#
#   @param  hex_str HEX string '#ffffff'.
#
#   @return HSV array [h,s,v].
def hex_to_hsv(hex_str):
    rgb_array = hex_to_rgb(hex_str)
    return rgb_to_hsv(rgb_array)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Convert HSV array [h,s,v] to an ANSI color escape code string.
#   @details    HSV where h is in the set [0, 359] and s, v are in the set [0.0, 100.0].
#               ANSI where \033[38;2;r;g;bm is for the foreground color
#               and \033[48;2;r;g;bm is for the background color.
#
#   @param  hsv_array   HSV array [h,s,v].
#   @param  background  Flag for if the HSV color is for a background or not.
#
#   @return ANSI escape code string.
def hsv_to_ansi(hsv_array, background=False):
    rgb_array = hsv_to_rgb(hsv_array)
    return rgb_to_ansi(rgb_array, background=background)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Converts ANSI color escape code string tp HSV array [h,s,v].
#   @details    ANSI where \033[38;2;r;g;bm is for the foreground color
#               and \033[48;2;r;g;bm is for the background color.
#               HSV where h is in the set [0, 359] and s, v are in the set [0.0, 100.0].
#
#   @param  ansi_string ANSI color escape code string.
#
#   @return HSV array [h,s,v].
def ansi_to_hsv(ansi_string):
    rgb_array = ansi_to_rgb(ansi_string)
    return rgb_to_hsv(rgb_array)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Convert HEX string '#ffffff' to an ANSI color escape code string.
#   @details    HEX string is in the set ["#000000", "#ffffff"].
#               ANSI where \033[38;2;r;g;bm is for the foreground color
#               and \033[48;2;r;g;bm is for the background color.
#
#   @param  hex_str     HEX string '#ffffff'.
#   @param  background  Flag for if the HEX string is for a background or not.
#
#   @return ANSI escape code string.
def hex_to_ansi(hex_str, background=False):
    rgb_array = hex_to_rgb(hex_str)
    return rgb_to_ansi(rgb_array, background=background)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Converts ANSI color escape code string to HEX string '#ffffff'.
#   @details    ANSI where \033[38;2;r;g;bm is for the foreground color
#               and \033[48;2;r;g;bm is for the background color.
#               HEX string is in the set ["#000000", "#ffffff"].
#
#   @param  ansi_string ANSI color escape code string.
#
#   @return A HEX string.
def ansi_to_hex(ansi_string):
    rgb_array = ansi_to_rgb(ansi_string)
    return rgb_to_hex(rgb_array)


# **************************************************************************
# **************************************************************************

##  Converts RGB array [r,g,b] to HSV array [h,s,v].
#   @details    RGB where [r,g,b] are in the set [0, 255].
#               HSV where h is in the set [0, 359] and s, v are in the set [0.0, 100.0].
#               Formula adapted from https://www.rapidtables.com/convert/color/rgb-to-hsv.html
#
#   @param  rgb_array   RGB array [r,g,b].
#
#   @return HSV array [h,s,v].
def rgb_to_hsv(rgb_array):
    r, g, b = rgb_array
    r, g, b = (r/255), (g/255), (b/255)

    min_color, max_color = min(r, g, b), max(r, g, b)
    change_in_color = max_color - min_color
    h, s, v = None, None, max_color

    # Set saturation
    if max_color == 0:
        s = 0
    else:
        s = change_in_color / max_color

    # Set hue
    if change_in_color == 0:
        h = 0
    elif max_color == r:
        h = ((g - b) / change_in_color) % 6
    elif max_color == g:
        h = ((b - r) / change_in_color) + 2
    else:
        h = ((r - g) / change_in_color) + 4

    h = round(h*60)     # Degrees
    s = s*100           # Percentage [0% - 100%]
    v = v*100           # Percentage [0% - 100%]

    return [h, s, v]


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Convert HSV array [h,s,v] to RGB array [r,g,b].
#   @details    HSV where h is in the set [0, 359] and s, v are in the set [0.0, 100.0].
#               RGB where [r,g,b] are in the set [0, 255].
#               Formula adapted from https://www.rapidtables.com/convert/color/hsv-to-rgb.html
#
#   @param  hsv_array   HSV array [h,s,v].
#
#   @return RGB array [r,g,b].
def hsv_to_rgb(hsv_array):
    # Normalize 0 <= s <= 1 AND 0 <= v <= 1
    h, s, v = hsv_array
    s, v = s/100, v/100

    r, g, b = 0, 0, 0

    color_range = v * s
    x = color_range * (1 - abs(((h / 60) % 2) - 1))
    m = v - color_range

    if 0 <= h < 60:
        r, g, b = color_range, x, 0
    elif 60 <= h < 120:
        r, g, b = x, color_range, 0
    elif 120 <= h < 180:
        r, g, b = 0, color_range, x
    elif 180 <= h < 240:
        r, g, b = 0, x, color_range
    elif 240 <= h < 300:
        r, g, b = x, 0, color_range
    elif 300 <= h < 360:
        r, g, b = color_range, 0, x

    r, g, b = (r+m), (g+m), (b+m)

    r, g, b = round(r*255), round(g*255), round(b*255)

    return [r, g, b]


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Convert RGB array [r,g,b] to HEX string '#ffffff'.
#   @details    RGB where [r,g,b] are in the set [0, 255].
#               HEX string is in the set ["#000000", "#ffffff"].
#
#   @param  rgb_array   RGB array [r,g,b].
#
#   @return A HEX string.
def rgb_to_hex(rgb_array):
    r, g, b = rgb_array
    hex_string = '#%02x%02x%02x' % (r, g, b)

    return hex_string


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Convert HEX string '#ffffff' to RGB array [r,g,b].
#   @details    HEX string is in the set ["#000000", "#ffffff"].
#               RGB where [r,g,b] are in the set [0, 255].
#
#   @param  hex_str HEX string '#ffffff'.
#
#   @return RGB array [r,g,b].
def hex_to_rgb(hex_str):
    rgb_array = []
    for hex_digit1, hex_digit2 in zip(hex_str[1::2], hex_str[2::2]):    # Hex strings now contain a hashtag '#'.
        rgb_array.append(int(hex_digit1+hex_digit2, 16))

    return rgb_array


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Convert RGB array [r,g,b] to an ANSI color escape code string.
#   @details    An RGB [r,g,b] array is used to generate an ANSI
#               escape code of the RGB color for use in the
#               terminal CLI. The basic format for these codes depends
#               on if it will be used for foreground or background color.
#               Use \033[38;2;r;g;bm for the foreground color.
#               Use \033[48;2;r;g;bm for the background color.
#
#   @note   For more information about these ANSI escape codes,
#           here are some sources:
#           https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
#           https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences/33206814#33206814
#           https://stackoverflow.com/questions/45782766/color-python-output-given-rrggbb-hex-value/45782972#45782972
#
#   @param  rgb_array   RGB array [r,g,b].
#   @param  background  Flag for if the RGB color is for a background or not.
#
#   @return ANSI escape code string of the RGB color.
def rgb_to_ansi(rgb_array, background=False):
    r, g, b = rgb_array
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Converts ANSI color escape code string to an RGB array.
#
#   @note   This function is dependent on the ANSI string to
#           be formatted like '\033[{};2;{};{};{}m' or
#           '\u001b[{};2;{};{};{}m' or something similar. For more
#           information about these ANSI escape codes, here are
#           some sources:
#           https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
#           https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences/33206814#33206814
#           https://stackoverflow.com/questions/45782766/color-python-output-given-rrggbb-hex-value/45782972#45782972
#
#   @param  ansi_string ANSI color escape code string.
#
#   @return RGB array [r,g,b].
def ansi_to_rgb(ansi_string):
    split_ansi = ansi_string.split(';')
    r, g, b = int(split_ansi[-3]), int(split_ansi[-2]), int(split_ansi[-1][:-1])
    return [r, g, b]
