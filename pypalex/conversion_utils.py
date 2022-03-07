"""!
#######################################################################
@author Al Timofeyev
@date   February 2, 2022
@brief  Utilities for converting between RGB, HSL, HEX.
#######################################################################
"""


def rgb_to_hsl(rgb_array):
    """!
    @brief  Convert rgb array [r, g, b] to hsl array [h, s, l].
    @details    RGB where r, g, b are in the set [0, 255].
                HSL where h in the set [0, 359] and s, l in the set [0.0, 100.0].
                Formula adapted from https://www.rapidtables.com/convert/color/rgb-to-hsl.html
    @param  rgb_array   RGB array [r, g, b].
    @return HSL array [h, s, l].
    """
    r, g, b = rgb_array
    r, g, b = (r/255), (g/255), (b/255)

    min_color, max_color = min(r, g, b), max(r, g, b)
    h, s, l = None, None, ((max_color+min_color) / 2)

    if min_color == max_color:
        h = s = 0   # Color is grayscale/achromatic.
    else:
        color_range = max_color - min_color
        s = color_range / (1 - abs(2 * l - 1))
        if max_color == r:
            h = ((g - b) / color_range) % 6
        elif max_color == g:
            h = (b - r) / color_range + 2
        else:
            h = (r - g) / color_range + 4

    h = round(h*60)     # Degrees.
    s = round(s*100, 1) # Percentage [0% - 100%] whole numbers.
    l = round(l*100, 1) # Percentage [0% - 100%] whole numbers.

    return [h, s, l]


def hsl_to_rgb(hsl_array):
    """!
    @brief  Convert hsl array [h, s, l] to rgb array [r, g, b].
    @details    HSL where h is in the set [0, 359] and s, l are in the set [0.0, 100.0].
                RGB where r, g, b in the set [0, 255].
                Formula adapted from https://www.rapidtables.com/convert/color/hsl-to-rgb.html
    @param  hsl_array   HSL array [h, s, l].
    @return RGB array [r, g, b].
    """
    # Normalize 0 <= s <= 1 AND 0 <= l <= 1
    h, s, l = hsl_array
    s, l = s/100, l/100

    r, g, b = None, None, None

    if s == 0:
        r = g = b = l   # Color is grayscale/achromatic.
    else:
        color_range = s * (1 - abs(2 * l - 1))
        x = color_range * (1 - abs(((h / 60) % 2) - 1))
        m = l - (color_range / 2)

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


def rgb_to_hex(rgb_array):
    """!
    @brief  Convert rgb array [r, g, b] to hex string 'ffffff'.
    @details    RGB where r, g, b are in the set [0, 255].
                Hex string in set ["000000", "ffffff"].
    @param  rgb_array   RGB array [r, g, b].
    @return Hex string 'ffffff'
    """
    r, g, b = rgb_array
    hex_string = '%02x%02x%02x' % (r, g, b)

    return hex_string
