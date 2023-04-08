##  @file   print_utils.py
#   @brief  Utilities for printing preview to the screen.
#
#   @note   Potential point for contributors to add
#           different printing options, maybe even a
#           printing option that displays in a GUI.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on April 5, 2023.


# ---- IMPORTS ----
from . import conversion_utils as convert


##  Prints the default color schemes to the terminal.
#   @details    Prints a preview of the extracted color palettes
#               to the user's terminal screen using ANSI escape
#               codes.
#
#   @note   The terminal needs to be able to display ASCII
#           characters and ANSI colors for this to work.
#
#   @param  hex_color_palette   A dictionary of light, normal, and dark color palettes in hex format.
def print_default_scheme_preview(hex_color_palette):
    rgb_color_palette = get_rgb_palette(hex_color_palette)
    ansi_color_codes = get_ansi_color_codes(rgb_color_palette)

    reset_color = '\033[0m'  # Reset ANSI color escape code.

    light_background_ansi_color = ansi_color_codes['light background']
    dark_background_ansi_color = ansi_color_codes['dark background']
    ansi_colors1 = [ansi_color_codes['normal black'], ansi_color_codes['normal red'],
                    ansi_color_codes['normal green'], ansi_color_codes['normal yellow'],
                    ansi_color_codes['normal blue'], ansi_color_codes['normal magenta'],
                    ansi_color_codes['normal cyan'], ansi_color_codes['normal white']]

    ansi_colors2 = [ansi_color_codes['light black'], ansi_color_codes['light red'],
                    ansi_color_codes['light green'], ansi_color_codes['light yellow'],
                    ansi_color_codes['light blue'], ansi_color_codes['light magenta'],
                    ansi_color_codes['light cyan'], ansi_color_codes['light white']]

    ansi_colors3 = [ansi_color_codes['dark black'], ansi_color_codes['dark red'],
                    ansi_color_codes['dark green'], ansi_color_codes['dark yellow'],
                    ansi_color_codes['dark blue'], ansi_color_codes['dark magenta'],
                    ansi_color_codes['dark cyan'], ansi_color_codes['dark white']]

    light_scheme_panes = generate_panes(light_background_ansi_color, ansi_colors1, ansi_colors3)
    dark_scheme_panes = generate_panes(dark_background_ansi_color, ansi_colors1, ansi_colors2)

    # ASCII characters.
    # Full Block : █ = $'\u2588'
    full_block = '\u2588'
    lower_right_tri = '\u25e2'
    lower_left_tri = '\u25e3'
    upper_right_tri = '\u25e5'
    upper_left_tri = '\u25e4'

    top_border = \
        lower_right_tri + ' ' + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + \
        ' ' + lower_left_tri
    bottom_border = \
        upper_right_tri + ' ' + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + \
        ' ' + upper_left_tri
    foreground_row = \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block + full_block + \
        full_block + full_block + full_block

    # ****************************************** LIGHT SCHEME
    # ---- Top border
    print(get_color_escape(rgb_color_palette['light background']) + top_border + reset_color)

    # ---- Blank row for spacing between border and panes
    print(get_color_escape(rgb_color_palette['light background']) + full_block + full_block + reset_color, end='')
    print(light_background_ansi_color + '                                           ' + reset_color, end='')
    print(get_color_escape(rgb_color_palette['light background']) + full_block + full_block + reset_color)

    # ---- Rows of panes
    for scheme_pane in light_scheme_panes:
        print(get_color_escape(rgb_color_palette['light background']) + full_block + full_block + reset_color, end='')
        print(light_background_ansi_color + '  ' + scheme_pane
              + light_background_ansi_color + '  ' + reset_color, end='')
        print(get_color_escape(rgb_color_palette['light background']) + full_block + full_block + reset_color)

    # ---- Blank row for spacing between panes and foreground
    print(get_color_escape(rgb_color_palette['light background']) + full_block + full_block + reset_color, end='')
    print(light_background_ansi_color + '                                           ' + reset_color, end='')
    print(get_color_escape(rgb_color_palette['light background']) + full_block + full_block + reset_color)

    # ---- Foreground row
    print(get_color_escape(rgb_color_palette['light background']) + full_block + full_block + reset_color, end='')
    print(ansi_color_codes['dark foreground'] + light_background_ansi_color
          + '      ' + foreground_row + '      '
          + reset_color, end='')
    print(get_color_escape(rgb_color_palette['light background']) + full_block + full_block + reset_color)

    # ---- Bottom border
    print(get_color_escape(rgb_color_palette['light background']) + bottom_border + reset_color)

    # ****************************************** DARK SCHEME
    # ---- Top border
    print(get_color_escape(rgb_color_palette['dark background']) + top_border + reset_color)

    # ---- Blank row for spacing between border and panes
    print(get_color_escape(rgb_color_palette['dark background']) + full_block + full_block + reset_color, end='')
    print(dark_background_ansi_color + '                                           ' + reset_color, end='')
    print(get_color_escape(rgb_color_palette['dark background']) + full_block + full_block + reset_color)

    # ---- Rows of panes
    for scheme_pane in dark_scheme_panes:
        print(get_color_escape(rgb_color_palette['dark background']) + full_block + full_block + reset_color, end='')
        print(dark_background_ansi_color + '  ' + scheme_pane
              + dark_background_ansi_color + '  ' + reset_color, end='')
        print(get_color_escape(rgb_color_palette['dark background']) + full_block + full_block + reset_color)

    # ---- Blank row for spacing between panes and foreground
    print(get_color_escape(rgb_color_palette['dark background']) + full_block + full_block + reset_color, end='')
    print(dark_background_ansi_color + '                                           ' + reset_color, end='')
    print(get_color_escape(rgb_color_palette['dark background']) + full_block + full_block + reset_color)

    # ---- Foreground row
    print(get_color_escape(rgb_color_palette['dark background']) + full_block + full_block + reset_color, end='')
    print(ansi_color_codes['light foreground'] + dark_background_ansi_color
          + '      ' + foreground_row + '      '
          + reset_color, end='')
    print(get_color_escape(rgb_color_palette['dark background']) + full_block + full_block + reset_color)

    # ---- Bottom border
    print(get_color_escape(rgb_color_palette['dark background']) + bottom_border + reset_color)


# **************************************************************************
# **************************************************************************

##  Constructs ANSI color escape code based on an RGB list.
#   @details    An RGB [r,g,b] list is used to generate an ANSI
#               escape code of the RGB color for use in the
#               terminal CLI. The basic format for these codes depends
#               on if it will be used for foreground or background color.
#               Use \033[38;2;r;g;bm for the foreground color.
#               Use \033[48;2;r;g;bm for the background color.
#
#   @note   For more information about these ANSI escape codes,
#           here are some sources:
#           https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences/33206814#33206814
#           https://stackoverflow.com/questions/45782766/color-python-output-given-rrggbb-hex-value/45782972#45782972
#
#   @param  rgb_array   RGB array [r,g,b].
#   @param  background  Flag for if the RGB color is for a background or not.
#
#   @return ANSI escape code of the RGB color.
def get_color_escape(rgb_array, background=False):
    r, g, b = rgb_array
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Constructs an RGB [r,g,b] palette dictionary using a hex palette dictionary.
#
#   @param  hex_color_palette   A dictionary of color palettes in hex format.
#
#   @return A dictionary of colors in RGB [r,g,b] format.
def get_rgb_palette(hex_color_palette):
    rgb_color_palette = {}

    for key, value in hex_color_palette.items():
        rgb_color_palette[key] = convert.hex_to_rgb(value)

    return rgb_color_palette


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Constructs a ANSI escape code dictionary using a RGB [r,g,b] palette dictionary.
#
#   @param  rgb_color_palette   A dictionary of light, normal and dark color palettes in RGB [r,g,b] format.
#
#   @return A dictionary of ANSI color escape codes.
def get_ansi_color_codes(rgb_color_palette):
    ansi_color_codes = {}

    for key, value in rgb_color_palette.items():
        if key == 'light background' or key == 'dark background':
            ansi_color_codes[key] = get_color_escape(value, True)
        else:
            ansi_color_codes[key] = get_color_escape(value)

    return ansi_color_codes


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Generates panes based on two sets of ANSI color escape codes.
#
#   @note   The terminal needs to be able to display ASCII
#           characters and ANSI colors for this to be useful.
#
#   @param  background_ansi_color   The background ANSI color escape code.
#   @param  ansi_colors1            List of ANSI color escape codes.
#   @param  ansi_colors2            List of ANSI color escape codes.
#
#   @return List of strings of panes with ASCII and ANSI escape codes.
def generate_panes(background_ansi_color, ansi_colors1, ansi_colors2):
    if len(ansi_colors1) != len(ansi_colors2):  # The ansi color lists need to be the same length.
        return ['', '', '', '']

    reset_color = '\033[0m'  # Reset ANSI color escape code.

    # ASCII characters.
    # Full Block : █ = $'\u2588'
    # Upper half Block : ▀ = $'\u2580'
    # Lower Half Block : ▄ = $'\u2584'
    full_block = '\u2588'
    upper_block = '\u2580'
    lower_block = '\u2584'

    # Pane building blocks.
    front_top_pane = full_block + full_block + full_block
    front_mid_pane1 = full_block + full_block + full_block
    front_mid_pane2 = full_block + full_block + full_block
    front_bottom_pane = ' '
    back_top_pane = lower_block
    back_mid_pane1 = full_block
    back_mid_pane2 = full_block
    back_bottom_pane = upper_block + upper_block + upper_block

    # 4 Rows of panes.
    top_panes = ''
    mid_panes1 = ''
    mid_panes2 = ''
    bottom_panes = ''

    panes = [top_panes, mid_panes1, mid_panes2, bottom_panes]
    front_panes = [front_top_pane, front_mid_pane1, front_mid_pane2, front_bottom_pane]
    back_panes = [back_top_pane, back_mid_pane1, back_mid_pane2, back_bottom_pane]

    for idx, (pane, front_pane, back_pane) in enumerate(zip(panes, front_panes, back_panes)):  # For every row of panes.
        not_first_pane = False
        for ansi_color1, ansi_color2 in zip(ansi_colors1, ansi_colors2):  # For every color.
            if not_first_pane:
                pane += background_ansi_color + ' '
            pane += ansi_color1 + background_ansi_color + front_pane
            pane += ansi_color2 + background_ansi_color + back_pane
            not_first_pane = True
        pane += reset_color
        panes[idx] = pane

    return panes
