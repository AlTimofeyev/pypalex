##  @file   settings.py
#   @brief  The settings for PyPalEx.
#   @details    Used to set up the version numbers and
#               default output locations.
#
#   @note   This code has been borrowed from Dylan Araps
#           PyWal on github: https://github.com/dylanaraps/pywal/blob/master/pywal/settings.py
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on March 2, 2022
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 11, 2023.
#   - Modified by Al Timofeyev on March 22, 2023.
#   - Modified by Al Timofeyev on March 26, 2023.
#   - Modified by Al Timofeyev on April 7, 2023.
#   - Modified by Al Timofeyev on May 16, 2024.
#   - Modified by Al Timofeyev on May 31, 2024.
#   - Modified by Al Timofeyev on June 10, 2024.
#   - Modified by Al Timofeyev on July 8, 2024.


import os
import platform

__version__ = "2.1.1"
__cache_version__ = "1.0.0"

HOME = os.getenv("HOME", os.getenv("USERPROFILE"))
XDG_CACHE_DIR = os.getenv("XDG_CACHE_HOME", os.path.join(HOME, ".cache"))
XDG_CONF_DIR = os.getenv("XDG_CONFIG_HOME", os.path.join(HOME, ".config"))

# NOTE: CONF_DIR will just be the place where PyPalEx saves color palettes
# by default! No settings are actually stored. That's why the user of this
# tool can set their own default location with PYPALEX_CONFIG_DIR
# global shell environment variable.
CACHE_DIR = os.getenv("PYPALEX_CACHE_DIR", os.path.join(XDG_CACHE_DIR, "palex"))
CONF_DIR = os.getenv("PYPALEX_CONFIG_DIR", os.path.join(XDG_CONF_DIR, "palex"))
DEFAULT_EXTRACTED_DIR = os.path.join(CONF_DIR, "primary")
PASTEL_EXTRACTED_DIR = os.path.join(CONF_DIR, "pastel")
RAW_EXTRACTED_DIR = os.path.join(CONF_DIR, "raw")
MODULE_DIR = os.path.dirname(__file__)

OS = platform.uname()[0]
