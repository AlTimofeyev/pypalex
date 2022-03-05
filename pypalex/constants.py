"""!
#######################################################################
@author Al Timofeyev
@date   February 2, 2022
@brief  A collection of constants.
#######################################################################
"""

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
RED_HUE_MIN = 0
RED_HUE_MAX = 359
# YELLOW_HUE = 60 # Original hue for yellow.
YELLOW_HUE = 55 # Adjusted for brightness.
GREEN_HUE = 120
CYAN_HUE = 180
BLUE_HUE = 240
MAGENTA_HUE = 300
# -----------------------------------------------

# Lighting range [min, max] for grayscale/achromatic colors.
BLACK_LIGHT_RANGE = [0, 40]     # Range of lighting for where a color can be considered black.
GRAY_LIGHT_RANGE = [40, 60]     # Range of lighting for where a color can be considered gray.
WHITE_LIGHT_RANGE = [60, 100]   # Range of lighting for where a color can be considered white.
# -----------------------------------------------

# Hue range [min, max) for base colors.
RED_HUE_RANGE_MAX = [330, 360]
RED_HUE_RANGE_MIN = [0, 25]
YELLOW_HUE_RANGE = [25, 60]
GREEN_HUE_RANGE = [60, 170]
CYAN_HUE_RANGE = [170, 205]
BLUE_HUE_RANGE = [205, 260]
MAGENTA_HUE_RANGE = [260, 330]
# -----------------------------------------------
