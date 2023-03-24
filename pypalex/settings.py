##  @file   settings.py
#   @brief  The settings for PyPalEx.
#   @details    Used to set up the version numbers and
#               default output locations.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on March 2, 2022
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 11, 2023.
#   - Modified by Al Timofeyev on March 22, 2023.
#
#   @note   This code has been borrowed from Dylan Araps
#           PyWal on github: https://github.com/dylanaraps/pywal/blob/master/pywal/settings.py


import os
import platform

__version__ = "1.3.1"
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
MODULE_DIR = os.path.dirname(__file__)

OS = platform.uname()[0]
