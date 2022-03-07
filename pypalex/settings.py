"""!
#######################################################################
@author Al Timofeyev
@date   March 2, 2022
@brief  Settings for PyPalEx.

NOTE:
This code has been borrowed from Dylan Araps PyWal
on github: https://github.com/dylanaraps/pywal/blob/master/pywal/settings.py
#######################################################################
"""

import os
import platform

__version__ = "1.0.4"
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
