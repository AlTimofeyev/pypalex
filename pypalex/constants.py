##  @file   constants.py
#   @brief  A collection of constants for PyPalEx.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on February 2, 2022.
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 6, 2023.
#   - Modified by Al Timofeyev on May 31, 2024.
#   - Modified by Al Timofeyev on June 10, 2024.


# RGB values for base colors.
BLACK_RGB = [0, 0, 0]
WHITE_RGB = [255, 255, 255]
RED_RGB = [255, 0, 0]
# YELLOW_RGB = [255, 255, 0]  # Original hex for yellow.
YELLOW_RGB = [255, 234, 0]  # Adjusted for brightness.
GREEN_RGB = [0, 255, 0]
CYAN_RGB = [0, 255, 255]
BLUE_RGB = [0, 0, 255]
MAGENTA_RGB = [255, 0, 255]
# -----------------------------------------------

# HEX values for base colors.
BLACK_HEX = 0x000000
WHITE_HEX = 0xFFFFFF
RED_HEX = 0xFF0000
# YELLOW_HEX = 0xFFFF00   # Original hex for yellow.
YELLOW_HEX = 0xFFEA00   # Adjusted for brightness.
GREEN_HEX = 0x00FF00
CYAN_HEX = 0x00FFFF
BLUE_HEX = 0x0000FF
MAGENTA_HEX = 0xFF00FF
# -----------------------------------------------

# Hue values for base colors.
RED_HUE = 0
# YELLOW_HUE = 60 # Original hue for yellow.
YELLOW_HUE = 55 # Adjusted for brightness.
GREEN_HUE = 120
CYAN_HUE = 180
BLUE_HUE = 240
MAGENTA_HUE = 300
# -----------------------------------------------

# Hue range [min, max) for base colors.
RED_HUE_RANGE_MAX = [330, 360]
RED_HUE_RANGE_MIN = [0, 25]
YELLOW_HUE_RANGE = [25, 64]
GREEN_HUE_RANGE = [64, 170]
CYAN_HUE_RANGE = [170, 210]
BLUE_HUE_RANGE = [210, 260]
MAGENTA_HUE_RANGE = [260, 330]
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
SATURATION_TOLERANCE_RANGE = [10.0, 15.0]
# -----------------------------------------------

# Pastel Saturation and Brightness Value ranges [min, max]
PASTEL_SATURATION_RANGE = [15.0, 75.0]
PASTEL_BRIGHTNESS_RANGE = [65.0, 95.0]
# -----------------------------------------------
