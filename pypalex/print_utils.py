##  @file   print_utils.py
#   @brief  Utilities for printing preview to the screen.
#
#   @note   Potential point for contributors to add
#           different printing options, maybe even a
#           printing option that displays in a GUI.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on April 5, 2023.
#   - Modified by Al Timofeyev on July 8, 2024.
#   - Modified by Al Timofeyev on October 12, 2024.


# ---- IMPORTS ----
import os
from . import conversion_utils as convert


##  Prints raw extracted colors to the Terminal.
#
#   @param  extracted_colors_dict   A dictionary of colors.
#   @param  color_format            A string that specifies the format of each color in the extracted colors dictionary (e.g. 'hsv', 'rgb', 'hex', 'ansi').
#   @param  pair_colors             A Flag to specify whether to print colors by pairing them by color type or not.
def print_raw_colors(extracted_colors_dict, color_format, pair_colors=False):
    rgb_colors_dict = get_rgb_colors(extracted_colors_dict, color_format)
    ansi_color_codes = extracted_colors_dict if color_format == 'ansi' else get_ansi_color_codes(rgb_colors_dict)

    columns, rows = os.get_terminal_size()
    # columns = os.get_terminal_size().columns

    reset_color = '\033[0m'  # Reset ANSI color escape code.

    name_spacing = '<20'
    color_spacing_1 = '^25'
    color_spacing_2 = '^25'
    partial_color_spacing_1 = '^9'
    partial_color_spacing_2 = '^10'
    color_spacing_symbol = ''
    symbol_spacing = '^0'
    end = ''

    # Make sure that the colors are printed in a decent format.
    # If the screen size gets too small, this part will break.
    if columns <= 85:
        name_spacing = '^16'
        color_spacing_1 = '^16'
        color_spacing_2 = '^25'
        partial_color_spacing_1 = '^5'
        partial_color_spacing_2 = '^5'
        color_spacing_symbol = ' '
        symbol_spacing = '^5'
        end = '\n'
    elif columns < 100:
        name_spacing = '<16'
        color_spacing_1 = '^20'
        color_spacing_2 = '^20'
        partial_color_spacing_1 = '^7'
        partial_color_spacing_2 = '^7'

    # ****************************************** BACKGROUND COLORS
    print(f"{'LIGHT BACKGROUND' : {name_spacing}}{':' : ^5}{repr(extracted_colors_dict['light background']) : ^25}", end=end)
    print(f"{reset_color}{' ' : {partial_color_spacing_1}}{reset_color}"
          f"{reset_color}{ansi_color_codes['light background']}{' ' : ^6}{reset_color}"
          f"{reset_color}{' ' : {partial_color_spacing_2}}{reset_color}"
          f"{color_spacing_symbol : {symbol_spacing}}"
          f"{reset_color}{ansi_color_codes['light background']}{ansi_color_codes['dark foreground']}{'chroma' : {color_spacing_2}}{reset_color}")

    print(f"{'DARK BACKGROUND' : {name_spacing}}{':' : ^5}{repr(extracted_colors_dict['dark background']) : ^25}", end=end)
    print(f"{reset_color}{' ' : {partial_color_spacing_1}}{reset_color}"
          f"{reset_color}{ansi_color_codes['dark background']}{' ' : ^6}{reset_color}"
          f"{reset_color}{' ' : {partial_color_spacing_2}}{reset_color}"
          f"{color_spacing_symbol : {symbol_spacing}}"
          f"{reset_color}{ansi_color_codes['dark background']}{ansi_color_codes['light foreground']}{'chroma' : {color_spacing_2}}{reset_color}")

    # ****************************************** FOREGROUND COLORS
    print(f"{'LIGHT FOREGROUND' : {name_spacing}}{':' : ^5}{repr(extracted_colors_dict['light foreground']) : ^25}", end=end)
    print(f"{reset_color}{ansi_color_codes['light foreground']}{'chroma' : {color_spacing_1}}{reset_color}"
          f"{color_spacing_symbol : {symbol_spacing}}"
          f"{reset_color}{convert.rgb_to_ansi(rgb_colors_dict['light foreground'], background=True)}{ansi_color_codes['dark foreground']}{'chroma' : {color_spacing_2}}{reset_color}")

    print(f"{'DARK FOREGROUND' : {name_spacing}}{':' : ^5}{repr(extracted_colors_dict['dark foreground']) : ^25}", end=end)
    print(f"{reset_color}{ansi_color_codes['dark foreground']}{'chroma' : {color_spacing_1}}{reset_color}"
          f"{color_spacing_symbol : {symbol_spacing}}"
          f"{reset_color}{convert.rgb_to_ansi(rgb_colors_dict['dark foreground'], background=True)}{ansi_color_codes['light foreground']}{'chroma' : {color_spacing_2}}{reset_color}")
    print()

    # ****************************************** ALL OTHER COLORS
    for color_name, color in extracted_colors_dict.items():
        if color_name in {'foreground', 'light foreground', 'dark foreground', 'background', 'light background', 'dark background'}:
            continue

        if pair_colors:
            # If printing colors by pairing them by color
            # type, then we only search for the base colors.
            if color_name not in {'black', 'red', 'orange', 'yellow', 'chartreuse', 'green', 'spring',
                                  'cyan', 'azure', 'blue', 'violet', 'magenta', 'rose', 'white'}:
                continue

            light_color_name, dark_color_name = 'light ' + color_name, 'dark ' + color_name

            ext_light_color, ext_dark_color = extracted_colors_dict[light_color_name], extracted_colors_dict[dark_color_name]
            rgb_light_color, rgb_dark_color = rgb_colors_dict[light_color_name], rgb_colors_dict[dark_color_name]
            ansi_light_color, ansi_dark_color = ansi_color_codes[light_color_name], ansi_color_codes[dark_color_name]

            print_raw_color(light_color_name, ext_light_color, rgb_light_color, ansi_light_color)
            print_raw_color(color_name, color, rgb_colors_dict[color_name], ansi_color_codes[color_name])
            print_raw_color(dark_color_name, ext_dark_color, rgb_dark_color, ansi_dark_color)
        else:
            print_raw_color(color_name, color, rgb_colors_dict[color_name], ansi_color_codes[color_name])


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Prints the extracted colors, organized into color palettes, to the Terminal.
#   @details    Prints a preview of the extracted colors to
#               the user's CLI / Terminal screen, organized
#               into palettes and using ANSI escape codes
#               and ASCII characters.
#
#   @note   The CLI / Terminal needs to be able to display ASCII
#           characters and ANSI colors for this to work.
#
#   @param  palettes        A dictionary of color palettes, where each item (palette) is a dictionary of colors.
#   @param  color_format    A string that specifies the format of each color in the extracted colors dictionary (e.g. 'hsv', 'rgb', 'hex', 'ansi').
def print_palette_preview(palettes, color_format):
    for palette_name, colors_dict in palettes.items():
        rgb_colors_dict = get_rgb_colors(colors_dict, color_format)
        ansi_color_codes = colors_dict if color_format == 'ansi' else get_ansi_color_codes(rgb_colors_dict)

        background_rgb_color = rgb_colors_dict['background']
        foreground_rgb_color = rgb_colors_dict['foreground']
        background_ansi_color = ansi_color_codes['background']

        standard_ansi_colors = [ansi_color_codes['color0'], ansi_color_codes['color1'], ansi_color_codes['color2'],
                                ansi_color_codes['color3'],ansi_color_codes['color4'], ansi_color_codes['color5'],
                                ansi_color_codes['color6'], ansi_color_codes['color7']]
        intense_ansi_colors = [ansi_color_codes['color8'], ansi_color_codes['color9'], ansi_color_codes['color10'],
                               ansi_color_codes['color11'],ansi_color_codes['color12'], ansi_color_codes['color13'],
                               ansi_color_codes['color14'], ansi_color_codes['color15']]

        # ---- Top border
        print(make_default_row(background_rgb_color, blank_row=False, border_type='top'))

        # ---- Blank row for spacing between border and panes
        print(make_default_row(background_rgb_color, blank_row=True))

        # ---- Rows of panes
        print(make_panes(background_ansi_color, standard_ansi_colors, intense_ansi_colors))

        # ---- Blank row for spacing between panes and foreground
        print(make_default_row(background_rgb_color, blank_row=True))

        # ---- Foreground row
        print(make_foreground_row(foreground_rgb_color, background_rgb_color))

        # ---- Bottom border
        print(make_default_row(background_rgb_color, blank_row=False, border_type='bottom'))


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Prints the extracted colors, organized into default color palettes, to the Terminal.
#   @details    Prints a preview of the extracted colors to
#               the user's CLI / Terminal screen, organized
#               into default palettes and using ANSI escape
#               codes and ASCII characters.
#
#   @note   The CLI / Terminal needs to be able to display ASCII
#           characters and ANSI colors for this to work.
#   @note   DEPRECATED function, in favor of print_palette_preview().
#
#   @param  extracted_colors_dict   A dictionary of colors.
#   @param  color_format            A string that specifies the format of each color in the extracted colors dictionary (e.g. 'hsv', 'rgb', 'hex', 'ansi').
def print_default_palette_preview(extracted_colors_dict, color_format):
    rgb_colors_dict = get_rgb_colors(extracted_colors_dict, color_format)

    ansi_color_codes = extracted_colors_dict if color_format == 'ansi' else get_ansi_color_codes(rgb_colors_dict)

    light_background_ansi_color = ansi_color_codes['light background']
    dark_background_ansi_color = ansi_color_codes['dark background']
    ansi_colors1 = [ansi_color_codes['black'], ansi_color_codes['red'],
                    ansi_color_codes['green'], ansi_color_codes['yellow'],
                    ansi_color_codes['blue'], ansi_color_codes['magenta'],
                    ansi_color_codes['cyan'], ansi_color_codes['white']]

    ansi_colors2 = [ansi_color_codes['light black'], ansi_color_codes['light red'],
                    ansi_color_codes['light green'], ansi_color_codes['light yellow'],
                    ansi_color_codes['light blue'], ansi_color_codes['light magenta'],
                    ansi_color_codes['light cyan'], ansi_color_codes['light white']]

    ansi_colors3 = [ansi_color_codes['dark black'], ansi_color_codes['dark red'],
                    ansi_color_codes['dark green'], ansi_color_codes['dark yellow'],
                    ansi_color_codes['dark blue'], ansi_color_codes['dark magenta'],
                    ansi_color_codes['dark cyan'], ansi_color_codes['dark white']]

    # ****************************************** LIGHT PALETTE
    # ---- Top border
    print(make_default_row(rgb_colors_dict['light background'], blank_row=False, border_type='top'))

    # ---- Blank row for spacing between border and panes
    print(make_default_row(rgb_colors_dict['light background'], blank_row=True))

    # ---- Rows of panes
    print(make_panes(light_background_ansi_color, ansi_colors1, ansi_colors3))

    # ---- Blank row for spacing between panes and foreground
    print(make_default_row(rgb_colors_dict['light background'], blank_row=True))

    # ---- Foreground row
    print(make_foreground_row(rgb_colors_dict['dark foreground'], rgb_colors_dict['light background']))

    # ---- Bottom border
    print(make_default_row(rgb_colors_dict['light background'], blank_row=False, border_type='bottom'))

    # ****************************************** DARK PALETTE
    # ---- Top border
    print(make_default_row(rgb_colors_dict['dark background'], blank_row=False, border_type='top'))

    # ---- Blank row for spacing between border and panes
    print(make_default_row(rgb_colors_dict['dark background'], blank_row=True))

    # ---- Rows of panes
    print(make_panes(dark_background_ansi_color, ansi_colors1, ansi_colors2))

    # ---- Blank row for spacing between panes and foreground
    print(make_default_row(rgb_colors_dict['dark background'], blank_row=True))

    # ---- Foreground row
    print(make_foreground_row(rgb_colors_dict['light foreground'], rgb_colors_dict['dark background']))

    # ---- Bottom border
    print(make_default_row(rgb_colors_dict['dark background'], blank_row=False, border_type='bottom'))


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Prints the extracted colors, organized with palette templates, to the Terminal.
#   @details    Prints a preview of the extracted colors to
#               the user's CLI / Terminal screen, organized
#               with palette templates and using ANSI escape
#               codes and ASCII characters.
#
#   @note   The CLI / Terminal needs to be able to display ASCII
#           characters and ANSI colors for this to work.
#   @note   DEPRECATED function, in favor of print_palette_preview().
#
#   @param  extracted_colors_dict   A dictionary of colors.
#   @param  palette_templates       A dictionary of palette templates.
#   @param  color_format            A string that specifies the format of each color in the extracted colors dictionary (e.g. 'hsv', 'rgb', 'hex', 'ansi').
def print_template_palette_preview(extracted_colors_dict, palette_templates, color_format):
    rgb_colors_dict = get_rgb_colors(extracted_colors_dict, color_format)

    ansi_color_codes = extracted_colors_dict if color_format == 'ansi' else get_ansi_color_codes(rgb_colors_dict)

    failsafe_color = ansi_color_codes['black']

    for palette_name, palette_template in palette_templates.items():
        background_rgb_color = rgb_colors_dict['dark background']
        foreground_rgb_color = rgb_colors_dict['light foreground']
        background_ansi_color = ansi_color_codes['dark background']

        standard_ansi_colors = [ansi_color_codes['black'], failsafe_color, failsafe_color, failsafe_color,
                                failsafe_color, failsafe_color, failsafe_color, ansi_color_codes['white']]
        intense_ansi_colors = [ansi_color_codes['light black'], failsafe_color, failsafe_color, failsafe_color,
                               failsafe_color, failsafe_color, failsafe_color, ansi_color_codes['light white']]

        for key, color_name in palette_template.items():
            if key == 'palette-type':
                # The dark palette type is assigned by default, so we only test for light.
                if color_name == 'light':
                    background_rgb_color = rgb_colors_dict['light background']
                    foreground_rgb_color = rgb_colors_dict['dark foreground']

                    background_ansi_color = ansi_color_codes['light background']
                    intense_ansi_colors[0] = ansi_color_codes['dark black']
                    intense_ansi_colors[7] = ansi_color_codes['dark white']
            elif color_name not in ansi_color_codes:
                continue
            elif key == 'color1':
                standard_ansi_colors[1] = ansi_color_codes[color_name]
            elif key == 'color2':
                standard_ansi_colors[2] = ansi_color_codes[color_name]
            elif key == 'color3':
                standard_ansi_colors[3] = ansi_color_codes[color_name]
            elif key == 'color4':
                standard_ansi_colors[4] = ansi_color_codes[color_name]
            elif key == 'color5':
                standard_ansi_colors[5] = ansi_color_codes[color_name]
            elif key == 'color6':
                standard_ansi_colors[6] = ansi_color_codes[color_name]
            elif key == 'color9':
                intense_ansi_colors[1] = ansi_color_codes[color_name]
            elif key == 'color10':
                intense_ansi_colors[2] = ansi_color_codes[color_name]
            elif key == 'color11':
                intense_ansi_colors[3] = ansi_color_codes[color_name]
            elif key == 'color12':
                intense_ansi_colors[4] = ansi_color_codes[color_name]
            elif key == 'color13':
                intense_ansi_colors[5] = ansi_color_codes[color_name]
            elif key == 'color14':
                intense_ansi_colors[6] = ansi_color_codes[color_name]

        # ---- Top border
        print(make_default_row(background_rgb_color, blank_row=False, border_type='top'))

        # ---- Blank row for spacing between border and panes
        print(make_default_row(background_rgb_color, blank_row=True))

        # ---- Rows of panes
        print(make_panes(background_ansi_color, standard_ansi_colors, intense_ansi_colors))

        # ---- Blank row for spacing between panes and foreground
        print(make_default_row(background_rgb_color, blank_row=True))

        # ---- Foreground row
        print(make_foreground_row(foreground_rgb_color, background_rgb_color))

        # ---- Bottom border
        print(make_default_row(background_rgb_color, blank_row=False, border_type='bottom'))


# **************************************************************************
# **************************************************************************

##  Prints a raw color to the Terminal screen.
#
#   @param  color_name      A string name of the color to be printed (i.e. red, yellow, blue, etc.).
#   @param  extracted_color The extracted color in any color format.
#   @param  rgb_color       The extracted color in RGB color format.
#   @param  ansi_color      The extracted color in ANSI color format.
def print_raw_color(color_name, extracted_color, rgb_color, ansi_color):
    columns, rows = os.get_terminal_size()
    # columns = os.get_terminal_size().columns

    reset_color = '\033[0m'  # Reset ANSI color escape code.

    name_spacing = '<20'
    color_spacing_1 = '^25'
    color_spacing_2 = '^25'
    color_spacing_symbol = ''
    symbol_spacing = '^0'
    end = ''

    # Make sure that the colors are printed in a decent format.
    # If the screen size gets too small, this part will break.
    if columns <= 85:
        name_spacing = '^16'
        color_spacing_1 = '^16'
        color_spacing_2 = '^25'
        color_spacing_symbol = ' '
        symbol_spacing = '^5'
        end = '\n'
    elif columns < 100:
        name_spacing = '<16'
        color_spacing_1 = '^20'
        color_spacing_2 = '^20'

    print(f"{color_name.upper() : {name_spacing}}{':' : ^5}{repr(extracted_color) : ^25}", end=end)
    print(f"{reset_color}{ansi_color}{'chroma' : {color_spacing_1}}{reset_color}"
          f"{color_spacing_symbol : {symbol_spacing}}"
          f"{reset_color}{convert.rgb_to_ansi(rgb_color, background=True)}{'chroma' : {color_spacing_2}}{reset_color}")


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Constructs a dictionary of colors in RGB [r,g,b] format.
#
#   @param  extracted_colors_dict   A dictionary of colors.
#   @param  color_format            A string that specifies the format of each color in the extracted colors dictionary (e.g. 'hsv', 'rgb', 'hex', 'ansi').
#
#   @return A dictionary of RGB colors.
def get_rgb_colors(extracted_colors_dict, color_format):
    rgb_colors_dict = {}

    for color_name, color in extracted_colors_dict.items():
        rgb_color = [0,0,0]     # Edge case.
        if color_format == 'rgb':
            rgb_color = color
        elif color_format == 'hsv':
            rgb_color = convert.hsv_to_rgb(color)
        elif color_format == 'hex':
            rgb_color = convert.hex_to_rgb(color)
        elif color_format == 'ansi':
            rgb_color = convert.ansi_to_rgb(color)

        rgb_colors_dict[color_name] = rgb_color

    return rgb_colors_dict


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Constructs an ANSI escape code dictionary using a dictionary of colors in RGB [r,g,b] format.
#
#   @param  rgb_colors_dict A dictionary of colors in RGB [r,g,b] format.
#
#   @return A dictionary of ANSI color escape codes.
def get_ansi_color_codes(rgb_colors_dict):
    ansi_color_codes = {}

    for color_name, rgb_color in rgb_colors_dict.items():
        if color_name == 'background' or color_name == 'light background' or color_name == 'dark background':
            ansi_color_codes[color_name] = convert.rgb_to_ansi(rgb_color, background=True)
        else:
            ansi_color_codes[color_name] = convert.rgb_to_ansi(rgb_color)

    return ansi_color_codes


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Creates a string that represents a default row when printing palette previews.
#   @details    The default row can be either a blank
#               row or a row with a specific border.
#
#   @param  rgb_row_color   The color of the row in RGB [r,g,b] format.
#   @param  blank_row       Flag that determines if this is a blank row or a border row.
#   @param  border_type     A string that specifies if this row needs a border (e.g. 'top', 'bottom').
#
#   @return A string that represents a default row that can be printed.
def make_default_row(rgb_row_color, blank_row, border_type=None):
    lower_right_tri = '\u25e2'
    lower_left_tri = '\u25e3'
    upper_right_tri = '\u25e5'
    upper_left_tri = '\u25e4'

    reset_color = '\033[0m'  # Reset ANSI color escape code.

    row = ''

    if blank_row:
        row += reset_color + convert.rgb_to_ansi(rgb_row_color, background=True)
        row += '                                               ' + reset_color
    else:
        left_corner, right_corner = '*', '*'
        if border_type == 'top':
            left_corner, right_corner = lower_right_tri, lower_left_tri
        elif border_type == 'bottom':
            left_corner, right_corner = upper_right_tri, upper_left_tri

        row += reset_color + convert.rgb_to_ansi(rgb_row_color) + left_corner + ' ' + reset_color
        row += convert.rgb_to_ansi(rgb_row_color, background=True)
        row += '                                           ' + reset_color
        row += convert.rgb_to_ansi(rgb_row_color) + ' ' + right_corner + reset_color

    return row


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Creates a string that represents the foreground row when printing palette previews.
#
#   @param  rbg_foreground_color    The foreground color of the row in RGB [r,g,b] format.
#   @param  rbg_background_color    The background color of the row in RGB [r,g,b] format.
#
#   @return A string that represents a foreground row that can be printed.
def make_foreground_row(rbg_foreground_color, rbg_background_color):
    reset_color = '\033[0m'  # Reset ANSI color escape code.

    ansi_foreground_color = convert.rgb_to_ansi(rbg_foreground_color, background=True)
    ansi_background_color = convert.rgb_to_ansi(rbg_background_color, background=True)

    row = reset_color
    row += ansi_background_color + '        ' + reset_color
    row += ansi_foreground_color + '                               ' + reset_color
    row += ansi_background_color + '        ' + reset_color

    return row


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Creates a string that represents the 4 rows of panes when printing palette previews.
#
#   @param  background_ansi_color   An ANSI escape code string of the background color.
#   @param  standard_ansi_colors    A list of ANSI escape code strings for standard colors.
#   @param  intense_ansi_colors     A list of ANSI escape code strings for intense colors.
#
#   @return A string that represents the 4 rows of panes that can be printed.
def make_panes(background_ansi_color, standard_ansi_colors, intense_ansi_colors):
    top_row = make_panes_row(background_ansi_color, standard_ansi_colors, intense_ansi_colors, panes_section='top')
    middle_row = make_panes_row(background_ansi_color, standard_ansi_colors, intense_ansi_colors, panes_section='middle')
    bottom_row = make_panes_row(background_ansi_color, standard_ansi_colors, intense_ansi_colors, panes_section='bottom')

    reset_color = '\033[0m'  # Reset ANSI color escape code.

    pane_rows = reset_color + ''

    # Row 1 - Top row of panes.
    pane_rows += background_ansi_color + '    ' + reset_color
    pane_rows += top_row + reset_color
    pane_rows += background_ansi_color + '    ' + reset_color + "\n"

    # Row 2 - Middle row of panes.
    pane_rows += background_ansi_color + '    ' + reset_color
    pane_rows += middle_row + reset_color
    pane_rows += background_ansi_color + '    ' + reset_color + "\n"

    # Row 3 - Middle row of panes.
    pane_rows += background_ansi_color + '    ' + reset_color
    pane_rows += middle_row + reset_color
    pane_rows += background_ansi_color + '    ' + reset_color + "\n"

    # Row 4 - Bottom row of panes.
    pane_rows += background_ansi_color + '    ' + reset_color
    pane_rows += bottom_row + reset_color
    pane_rows += background_ansi_color + '    ' + reset_color

    return pane_rows


# **************************************************************************
# **************************************************************************

##  Creates a string that represents a row of panes for printing palette previews.
#
#   @param  background_ansi_color   An ANSI escape code string of the background color.
#   @param  standard_ansi_colors    A list of ANSI escape code strings for standard colors.
#   @param  intense_ansi_colors     A list of ANSI escape code strings for intense colors.
#   @param  panes_section           A string that specifies which section of the panes to make (e.g. 'top', 'middle', 'bottom').
#
#   @return A string that represents a row of panes that can be printed.
def make_panes_row(background_ansi_color, standard_ansi_colors, intense_ansi_colors, panes_section):
    reset_color = '\033[0m'     # Reset ANSI color escape code.

    # ASCII characters.
    # Full Block : █ = $'\u2588'
    # Upper half Block : ▀ = $'\u2580'
    # Lower Half Block : ▄ = $'\u2584'
    full_block = '\u2588'
    upper_block = '\u2580'
    lower_block = '\u2584'

    # Pane building blocks.
    front_top_pane = full_block + full_block + full_block
    front_mid_pane = full_block + full_block + full_block
    front_bottom_pane = ' '
    back_top_pane = lower_block
    back_mid_pane = full_block
    back_bottom_pane = upper_block + upper_block + upper_block

    front_pane = '##'
    back_pane = "**"
    if panes_section == 'top':
        front_pane = front_top_pane
        back_pane = back_top_pane
    elif panes_section == 'middle':
        front_pane = front_mid_pane
        back_pane = back_mid_pane
    elif panes_section == 'bottom':
        front_pane = front_bottom_pane
        back_pane = back_bottom_pane

    row = reset_color + background_ansi_color + ''

    # For every color.
    for idx, (standard_color, intense_color) in enumerate(zip(standard_ansi_colors, intense_ansi_colors)):
        row += standard_color + front_pane
        row += intense_color + back_pane
        if idx < (len(standard_ansi_colors) - 1):
            row += ' '

    row += reset_color

    return row
