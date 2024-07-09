##  @file   file_utils.py
#   @brief  Utilities for file handling.
#
#   @note   Potential point for contributors to add
#           different output saving options.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on April 5, 2023.
#   - Modified by Al Timofeyev on July 8, 2024.


# ---- IMPORTS ----
import os
import json
import yaml

from .settings import CONF_DIR, DEFAULT_EXTRACTED_DIR, PASTEL_EXTRACTED_DIR, RAW_EXTRACTED_DIR


##  Generates a configuration file.
#   @details    Generates a configuration file and saves
#               it in the default Configuration Directory
#               for PyPalEx.
#
#   @note    If a file with the same name already exists, it can be overwritten.
#
#   @param  config_filename A string that represents the filename of the configuration file (e.g. 'palex-config.yaml').
def generate_config_file(config_filename):
    os.makedirs(CONF_DIR, exist_ok=True)
    config_filepath = os.path.join(CONF_DIR, config_filename)

    default_light_theme = {'palette-type': 'light', 'color1': 'red', 'color2': 'green', 'color3': 'yellow',
                           'color4': 'blue', 'color5': 'magenta', 'color6': 'cyan', 'color9': 'dark red',
                           'color10': 'dark green', 'color11': 'dark yellow', 'color12': 'dark blue',
                           'color13': 'dark magenta', 'color14': 'dark cyan'}
    default_dark_theme = {'palette-type': 'dark', 'color1': 'red', 'color2': 'green', 'color3': 'yellow',
                          'color4': 'blue', 'color5': 'magenta', 'color6': 'cyan', 'color9': 'light red',
                          'color10': 'light green', 'color11': 'light yellow', 'color12': 'light blue',
                          'color13': 'light magenta', 'color14': 'light cyan'}
    # mixed_light_theme = {'palette-type': 'light', 'color1': 'red', 'color2': 'green', 'color3': 'yellow',
    #                      'color4': 'blue', 'color5': 'magenta', 'color6': 'cyan', 'color9': 'rose',
    #                      'color10': 'chartreuse', 'color11': 'orange', 'color12': 'azure',
    #                      'color13': 'violet', 'color14': 'spring'}
    # mixed_dark_theme = {'palette-type': 'dark', 'color1': 'rose', 'color2': 'chartreuse', 'color3': 'orange',
    #                     'color4': 'azure', 'color5': 'violet', 'color6': 'spring', 'color9': 'red',
    #                     'color10': 'green', 'color11': 'yellow', 'color12': 'blue',
    #                     'color13': 'magenta', 'color14': 'cyan'}

    # config = {
    #     'save-check': True,
    #     'show-preview': True,
    #     'export-file-format': 'json',
    #     'export-color-format': 'hex',
    #     'exported-palettes': {'light-theme': default_light_theme, 'dark-theme': default_dark_theme,
    #                         'mixed-light-theme': mixed_light_theme, 'mixed-dark-theme': mixed_dark_theme}
    # }
    config = {
        'save-check': True,
        'show-preview': True,
        'export-file-format': 'json',
        'export-color-format': 'hex',
        'exported-palettes': {'light-theme': default_light_theme, 'dark-theme': default_dark_theme}
    }

    config_comments = "# ******************************************** CONFIG NOTES ********************************************\n"
    config_comments += "# ------------------------------------------------------------------------------------------------------\n"
    config_comments += "# For a full explanation about the configuration file for this tool please visit the\n"
    config_comments += "# PyPalEx Wiki page at : https://github.com/AlTimofeyev/pypalex/wiki/Configuration-File \n"
    config_comments += "# \n"
    config_comments += "# save-check          : Ask the user if they want to save the extracted palette - [True / False]\n"
    config_comments += "# show-preview        : Show preview of extracted palette(s) before saving - [True / False]\n"
    config_comments += "# export-file-format  : Export file format options - ['json', 'yaml']\n"
    config_comments += "# export-color-format : Export color format options - ['hex', 'rgb', 'hsv', 'ansi']\n"
    config_comments += "# exported-palettes   : Dictionary of palette templates to organize after extraction.\n"
    config_comments += "# \n"
    config_comments += "# Each palette MUST have a name (e.g. 'light-theme', 'dark-theme', 'mixed-light-theme', etc.).\n"
    config_comments += "# Each palette MUST specify what 'palette-type' it is : ('light' or 'dark').\n"
    config_comments += "# Each palette MUST specify Standard ANSI colors 1 through 6.\n"
    config_comments += "# Each palette MUST specify High-Intensity ANSI colors 9 through 14.\n"
    config_comments += "# More about ANSI colors at : https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit\n"
    config_comments += "# \n"
    config_comments += "# ************************************ COLORS AVAILABLE FOR PALETTES ***********************************\n"
    config_comments += "# ------------------------------------------------------------------------------------------------------\n"
    config_comments += "# 1.  red,        light red,        dark red\n"
    # config_comments += "# 2.  orange,     light orange,     dark orange\n"
    config_comments += "# 3.  yellow,     light yellow,     dark yellow\n"
    # config_comments += "# 4.  chartreuse, light chartreuse, dark chartreuse\n"
    config_comments += "# 5.  green,      light green,      dark green\n"
    # config_comments += "# 6.  spring,     light spring,     dark spring\n"
    config_comments += "# 7.  cyan,       light cyan,       dark cyan\n"
    # config_comments += "# 8.  azure,      light azure,      dark azure\n"
    config_comments += "# 9.  blue,       light blue,       dark blue\n"
    # config_comments += "# 10. violet,     light violet,     dark violet\n"
    config_comments += "# 11. magenta,    light magenta,    dark magenta\n"
    # config_comments += "# 12. rose,       light rose,       dark rose\n"
    config_comments += "# \n"
    config_comments += "# NOTES ABOUT PALETTES :\n"
    config_comments += "# - Palette Templates is just another way of saying Color Theme or Color Scheme Templates.\n"
    config_comments += "# - Color Codes color0, color7, color8 and color15, as well as the background and foreground,\n"
    config_comments += "#   have been excluded as they are hard-coded and dependent on the dominant color in the image.\n"
    config_comments += "# - If you mistype one of the color names or Color Codes PyPalEx will automatically default\n"
    config_comments += "#   to using black for that Color Code to avoid running into errors.\n"
    config_comments += "# ******************************************************************************************************\n\n"

    with open(config_filepath, 'w') as config_file:
        config_file.write(config_comments)
        yaml.dump(config, config_file, indent=4, sort_keys=False)

    print("GENERATED CONFIG :", config_filepath)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Saves the raw extracted colors into a file.
#
#   @note    If a file with the same name already exists, it can be overwritten.
#
#   @param  extracted_colors_dict   A dictionary of colors.
#   @param  image_name              A string that represents the name of the image from where the colors were extracted (e.g. 'forest_wallpaper', 'bubblegum', etc).
#   @param  output_path             A string that specifies the directory where to save the file (can be a blank string).
#   @param  export_file_format      A string that specifies the format of the file that will be exported (e.g. 'json', 'yaml').
#   @param  export_color_format     A string that specifies the format of the colors that will be exported (e.g. 'hsv', 'rgb', 'hex', 'ansi').
def raw_dump(extracted_colors_dict, image_name, output_path, export_file_format, export_color_format):
    if output_path == '':
        output_path = RAW_EXTRACTED_DIR
        filename = image_name + '-raw_colors.' + export_file_format
    else:
        output_path = os.path.join(output_path, image_name)
        filename = 'raw_colors.' + export_file_format

    os.makedirs(output_path, exist_ok=True)
    output_filepath = os.path.join(output_path, filename)

    if os.path.exists(output_filepath) and os.path.isfile(output_filepath):
        print("The following files already exist and will be overwritten if you proceed : ", sep='')
        print("   - ", output_filepath, sep='')
        print()  # Extra Spacing.
        overwrite_message = "Would you like to overwrite these files? [y/n]: "
        while True:
            user_choice = input(overwrite_message)
            user_choice = user_choice.lower()

            if user_choice in ('y', 'yes'):
                break
            elif user_choice in ('n', 'no'):
                return

    with open(output_filepath, 'w') as output_file:
        if export_file_format == 'json':
            json.dump(extracted_colors_dict, output_file, indent=4, sort_keys=False)
        elif export_file_format == 'yaml' or export_file_format == 'yml':
            if export_color_format == 'hsv' or export_color_format == 'rgb':
                yaml.dump(extracted_colors_dict, output_file, indent=4, sort_keys=False, default_flow_style=None)
            else:
                yaml.dump(extracted_colors_dict, output_file, indent=4, sort_keys=False)

    print("SAVED : ", output_filepath, sep='')


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Saves the color palettes of extracted colors.
#   @details    Each palette is saved to its own individual file.
#
#   @note    If files with the same name already exist, they can be overwritten.
#
#   @param  palettes            A dictionary of palettes that were organized based on the palette templates.
#   @param  palette_templates   A dictionary of palette templates.
#   @param  image_name          A string that represents the name of the image from where the colors were extracted (e.g. 'forest_wallpaper', 'bubblegum', etc).
#   @param  output_path         A string that specifies the directory where to save the file (can be a blank string).
#   @param  export_file_format  A string that specifies the format of the file that will be exported (e.g. 'json', 'yaml').
#   @param  export_color_format A string that specifies the format of the colors that will be exported (e.g. 'hsv', 'rgb', 'hex', 'ansi').
#   @param  pastel_light        A Flag that specifies if the light colors have been converted to pastel.
#   @param  pastel_normal       A Flag that specifies if the normal colors have been converted to pastel.
#   @param  pastel_dark         A Flag that specifies if the dark colors have been converted to pastel.
def save_palettes(palettes, palette_templates, image_name, output_path, export_file_format, export_color_format, pastel_light=False, pastel_normal=False, pastel_dark=False):
    output_filepaths = []
    make_output_path, make_default_primary_path, make_default_pastel_path = False, False, False

    for palette_name, palette in palettes.items():
        filename = palette_name + '.' + export_file_format

        if output_path == '':
            if ( (pastel_light and palette_templates[palette_name]['contains-light']) or
                    (pastel_normal and palette_templates[palette_name]['contains-normal']) or
                    (pastel_dark and palette_templates[palette_name]['contains-dark']) ):
                make_default_pastel_path = True
                output_filepaths.append(os.path.join(os.path.join(PASTEL_EXTRACTED_DIR, image_name), filename))
            else:
                make_default_primary_path = True
                output_filepaths.append(os.path.join(os.path.join(DEFAULT_EXTRACTED_DIR, image_name), filename))
        else:
            make_output_path = True
            output_filepaths.append(os.path.join(os.path.join(output_path, image_name), filename))

    if make_output_path:
        os.makedirs(os.path.join(output_path, image_name), exist_ok=True)
    else:
        if make_default_primary_path:
            os.makedirs(os.path.join(DEFAULT_EXTRACTED_DIR, image_name), exist_ok=True)
        if make_default_pastel_path:
            os.makedirs(os.path.join(PASTEL_EXTRACTED_DIR, image_name), exist_ok=True)

    overwrite_files = ""
    for output_filepath in output_filepaths:
        if os.path.exists(output_filepath) and os.path.isfile(output_filepath):
            overwrite_files += "   - " + output_filepath + "\n"

    if overwrite_files != "":
        print("The following files already exist and will be overwritten if you proceed : ", sep='')
        print(overwrite_files, end='')
        print()  # Extra Spacing.
        overwrite_message = "Would you like to overwrite these files? [y/n]: "
        while True:
            user_choice = input(overwrite_message)
            user_choice = user_choice.lower()

            if user_choice in ('y', 'yes'):
                break
            elif user_choice in ('n', 'no'):
                return

    for palette, output_filepath in zip(palettes.values(), output_filepaths):
        with open(output_filepath, 'w') as output_file:
            if export_file_format == 'json':
                json.dump(palette, output_file, indent=4, sort_keys=False)
            elif export_file_format == 'yaml' or export_file_format == 'yml':
                if export_color_format == 'hsv' or export_color_format == 'rgb':
                    yaml.dump(palette, output_file, indent=4, sort_keys=False, default_flow_style=None)
                else:
                    yaml.dump(palette, output_file, indent=4, sort_keys=False)

        print("SAVED : ", output_filepath, sep='')
