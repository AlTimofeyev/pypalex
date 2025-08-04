##  @file   constants.py
#   @brief  A collection of constants for PyPalEx.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on February 2, 2022.
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 6, 2023.
#   - Modified by Al Timofeyev on May 31, 2024.
#   - Modified by Al Timofeyev on June 10, 2024.
#   - Modified by Al Timofeyev on October 12, 2024.


# RGB values for base colors.
BLACK_RGB = [0, 0, 0]
WHITE_RGB = [255, 255, 255]
RED_RGB = [255, 0, 0]
ORANGE_RGB = [255, 153, 0]
YELLOW_RGB = [255, 213, 0]
CHARTREUSE_RGB = [191, 255, 0]
GREEN_RGB = [0, 255, 0]
SPRING_RGB = [0, 255, 149]
CYAN_RGB = [0, 255, 255]
AZURE_RGB = [0, 128, 255]
BLUE_RGB = [0, 0, 255]
VIOLET_RGB = [140, 0, 255]
MAGENTA_RGB = [255, 0, 255]
ROSE_RGB = [255, 0, 93]
# -----------------------------------------------

# HEX values for base colors.
BLACK_HEX = 0x000000
WHITE_HEX = 0xFFFFFF
RED_HEX = 0xFF0000
ORANGE_HEX = 0xFF9900
YELLOW_HEX = 0xFFD500
CHARTREUSE_HEX = 0xBFFF00
GREEN_HEX = 0x00FF00
SPRING_HEX = 0x00FF95
CYAN_HEX = 0x00FFFF
AZURE_HEX = 0x0080FF
BLUE_HEX = 0x0000FF
VIOLET_HEX = 0x8C00FF
MAGENTA_HEX = 0xFF00FF
ROSE_HEX = 0xFF005D
# -----------------------------------------------

# Hue values for base colors.
RED_HUE = 0
ORANGE_HUE = 36
YELLOW_HUE = 50
CHARTREUSE_HUE = 75
GREEN_HUE = 120
SPRING_HUE = 155
CYAN_HUE = 180
AZURE_HUE = 210
BLUE_HUE = 240
VIOLET_HUE = 273
MAGENTA_HUE = 300
ROSE_HUE = 338
# -----------------------------------------------

# Hue range [min, max) for base colors.
RED_HUE_RANGE_MIN = [0, 20]         # Range = 30    Hue = 0
ORANGE_HUE_RANGE = [20, 43]         # Range = 23    Hue = 36
YELLOW_HUE_RANGE = [43, 64]         # Range = 21    Hue = 55 -> 50
CHARTREUSE_HUE_RANGE = [64, 90]     # Range = 26    Hue = 67 -> 75
GREEN_HUE_RANGE = [90, 145]         # Range = 55    Hue = 120
SPRING_HUE_RANGE = [145, 170]       # Range = 25    Hue = 155
CYAN_HUE_RANGE = [170, 195]         # Range = 25    Hue = 180
AZURE_HUE_RANGE = [195, 220]        # Range = 25    Hue = 210
BLUE_HUE_RANGE = [220, 255]         # Range = 35    Hue = 240
VIOLET_HUE_RANGE = [255, 290]       # Range = 35    Hue = 273
MAGENTA_HUE_RANGE = [290, 325]      # Range = 35    Hue = 300
ROSE_HUE_RANGE = [325, 350]         # Range = 25    Hue = 338
RED_HUE_RANGE_MAX = [350, 360]
# -----------------------------------------------

# Brightness Value range [min, max] for grayscale/achromatic colors.
BLACK_BRIGHTNESS_RANGE = [0.0, 35.0]    # Range of brightness for where a color can be considered black or indistinguishable.
DARK_BRIGHTNESS_RANGE = [35.0, 55.0]    # Range of brightness for where a color can be considered dark.
NORM_BRIGHTNESS_RANGE = [55.0, 80.0]    # Range of brightness for where a color can be considered normal.
LIGHT_BRIGHTNESS_RANGE = [80.0, 100.0]  # Range of brightness for where a color can be considered light.
# -----------------------------------------------

# The tolerance range [min, max] for grayscale/achromatic colors.
# If a color is less saturated than the min value in this range then it's considered grayscale/achromatic.
# If a grayscale/achromatic color is borrowed from, then it's first normalized to be within this range
SATURATION_TOLERANCE_RANGE = [15.0, 20.0]
# -----------------------------------------------

# Pastel Saturation and Brightness Value ranges [min, max]
PASTEL_SATURATION_RANGE = [20.0, 55.0]
PASTEL_BRIGHTNESS_RANGE = [65.0, 95.0]
# -----------------------------------------------
