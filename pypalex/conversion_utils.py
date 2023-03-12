##  @file   conversion_utils.py
#   @brief  Utilities for converting between RGB, HSV, HEX.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on February 2, 2022.
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 6, 2023.


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

##  Convert HSV array [h,s,v] to HEX string 'ffffff'.
#   @details    HSV where h is in the set [0, 359] and s, v are in the set [0.0, 100.0].
#               HEX string is in the set ["000000", "ffffff"].
#   @param  hsv_array   HSV array [h,s,v].
#
#   @return A HEX string.
def hsv_to_hex(hsv_array):
    rgb_array = hsv_to_rgb(hsv_array)
    return rgb_to_hex(rgb_array)


# **************************************************************************
# **************************************************************************

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

##  Convert RGB array [r,g,b] to HEX string 'ffffff'.
#   @details    RGB where [r,g,b] are in the set [0, 255].
#               HEX string is in the set ["000000", "ffffff"].
#
#   @param  rgb_array   RGB array [r,g,b].
#
#   @return A HEX string.
def rgb_to_hex(rgb_array):
    r, g, b = rgb_array
    hex_string = '%02x%02x%02x' % (r, g, b)

    return hex_string
