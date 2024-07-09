##  @package pypalex
#   @brief      Python Palette Extractor: extracts color palettes from images
#   @details    PyPalEx is a tool for extracting color palettes from images
#               and generating a JSON format file with light and dark color
#               themes. This tool is intended to be OS independent, for use
#               by the tech community for developing their own custom theme
#               managers or by artists who want to extract color palettes for
#               their art from images, pictures or wallpapers they adore.

##  @mainpage PyPalEx: The Python Palette Extractor
#
#   @section description_main Description
#   PyPalEx is a tool for extracting color palettes from images and generating
#   a JSON format file with light and dark color themes. This tool is intended
#   to be OS independent, for use by the tech community for developing their own
#   custom theme managers or by artists who want to extract color palettes for
#   their art from images, pictures or wallpapers they adore.

##  @file   __main__.py
#   @brief  Main script for PyPalEx.
#   @details    Used to run from the Command Line.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on February 2, 2022.
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 6, 2023.
#   - Modified by Al Timofeyev on March 22, 2023.
#   - Modified by Al Timofeyev on March 26, 2023.
#   - Modified by Al Timofeyev on April 7, 2023.
#   - Modified by Al Timofeyev on June 10, 2024.
#   - Modified by Al Timofeyev on July 8, 2024.


# ---- IMPORTS ----
import sys
import os
import yaml
import argparse
import filetype
from PIL import Image

from .settings import __version__, CONF_DIR, DEFAULT_EXTRACTED_DIR, PASTEL_EXTRACTED_DIR, RAW_EXTRACTED_DIR
from .Extractor import Extractor
from . import image_utils as imutils
from . import arg_messages as argmsg
from . import file_utils as futils
from . import print_utils as prn

# ---- GLOBAL VARIABLES ----
## Filename of the configuration file.
CONFIG_FILENAME = 'palex-config.yaml'
## List of real/existing image file path(s).
PROPER_IMAGES = []
## List of image filenames (contain file extensions).
FILENAMES = []
## List of image names.
IMAGE_NAMES = []
## The path to the output directory where all exported files will be saved.
OUTPUT_PATH = ''
## The format of the files to be exported (e.g. 'json', 'yaml').
EXPORT_FILE_FORMAT = 'json'
## The format in which the extracted colors will be exported (e.g. 'hsv', 'rgb', 'hex', 'ansi').
EXPORT_COLOR_FORMAT = 'hex'
## Dictionary of palette templates that can be used to organize extracted colors into palettes to export.
EXPORT_PALETTE_TEMPLATES = {}
## Flag to check if user wants to save extracted color palettes.
SAVE_CHECK = False
## Flag to show a preview of extracted palettes.
SHOW_PREVIEW = False
## Flag to save raw extracted colors.
SAVE_RAW = False
## Flag to convert light color type to pastel.
PASTEL_L = False
## Flag to convert normal color type to pastel.
PASTEL_N = False
## Flag to convert dark color type to pastel.
PASTEL_D = False
## A set of valid color names used to check user-defined color palettes from the configuration file.
VALID_COLOR_SET = {'red', 'light red', 'dark red', 'yellow', 'light yellow', 'dark yellow',
                   'green', 'light green', 'dark green', 'cyan', 'light cyan', 'dark cyan',
                   'blue', 'light blue', 'dark blue', 'magenta', 'light magenta', 'dark magenta'}


# **************************************************************************
# ****** CODE ORGANIZED HIGH-LEVEL to LOW-LEVEL WITH SECTION DIVIDERS ******
# **************************************************************************

##  Main script function.
def main():
    handle_args()
    extract_color_palettes()


# **************************************************************************
# **************************************************************************

##  Handles the arguments passed to PyPalEx.
def handle_args():
    # Converts arguments into a dictionary: {'files': None, 'path': None, 'output': None}
    argument_parser = setup_argument_parser()
    args = vars(argument_parser.parse_args())

    # Check if pypalex version was requested.
    if args['version']:
        print("pypalex ", __version__, sep="")
        sys.exit()

    # Check if pypalex default output locations were requested.
    if args['where']:
        config_filepath = os.path.join(CONF_DIR, CONFIG_FILENAME)
        config_home = "Config Home : " + CONF_DIR
        config_file = "Config File : " + config_filepath
        primary_dir = "Primary     : " + DEFAULT_EXTRACTED_DIR
        pastel_dir = "Pastel      : " + PASTEL_EXTRACTED_DIR
        raw_dir = "Raw         : " + RAW_EXTRACTED_DIR

        if not os.path.exists(CONF_DIR) or os.path.isfile(CONF_DIR):
            config_home += "                    ->  [DOES NOT EXIST]"
        if not os.path.exists(config_filepath) or not os.path.isfile(config_filepath):
            config_file += "  ->  [DOES NOT EXIST]"
        if not os.path.exists(DEFAULT_EXTRACTED_DIR) or os.path.isfile(DEFAULT_EXTRACTED_DIR):
            primary_dir += "            ->  [DOES NOT EXIST]"
        if not os.path.exists(PASTEL_EXTRACTED_DIR) or os.path.isfile(PASTEL_EXTRACTED_DIR):
            pastel_dir += "             ->  [DOES NOT EXIST]"
        if not os.path.exists(RAW_EXTRACTED_DIR) or os.path.isfile(RAW_EXTRACTED_DIR):
            raw_dir += "                ->  [DOES NOT EXIST]"

        print(config_home, config_file, primary_dir, pastel_dir, raw_dir, sep='\n')
        sys.exit()

    # Check if pypalex configuration file was requested to be generated.
    if args['gen_config']:
        config_filepath = os.path.join(CONF_DIR, CONFIG_FILENAME)

        if os.path.exists(config_filepath) and os.path.isfile(config_filepath):
            print("A config file already exists : ", config_filepath, sep='')
            overwrite_message = "Would you like to overwrite the existing config file? [y/n]: "
            while True:
                user_choice = input(overwrite_message)
                user_choice = user_choice.lower()

                if user_choice in ('y', 'yes'):
                    break
                elif user_choice in ('n', 'no'):
                    sys.exit()

        futils.generate_config_file(CONFIG_FILENAME)
        sys.exit()

    # Exit if no files/paths were provided.
    if (args['files'] is None or args['files'] == []) and args['path'] is None:
        sys.exit(argmsg.no_args_help_message())

    # Check either the file(s) or the file(s) in the path
    # to make sure there are valid images to work with.
    if args['files']:
        if not check_sources(args['files'], args['path']):
            sys.exit(argmsg.bad_source_message())
    elif args['path'] is not None:
        if not check_path(args['path']):
            sys.exit(argmsg.bad_path_message())
        args['files'] = os.listdir(args['path'])
        if not check_sources(args['files'], args['path']):
            sys.exit(argmsg.bad_source_message())

    handle_config()     # Handle the configuration file before processing any CLI options.
    set_global_args(args)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Handles color extraction from image(s).
def extract_color_palettes():
    for index, image_dir in enumerate(PROPER_IMAGES):
        print("Processing ", FILENAMES[index], " : ",  sep='', end='')
        image = Image.open(image_dir)
        hsv_img_matrix_2d = imutils.process_image(image)
        print("COMPLETED")
        print("Extracting Colors : ", sep='', end='')
        extractor = Extractor(hsv_img_matrix_2d, IMAGE_NAMES[index])
        extractor.run()
        print("COMPLETED")

        if PASTEL_L or PASTEL_N or PASTEL_D:
            print("Converting Selected Pastel Options : ", sep='', end='')
            extractor.convert_to_pastel(pastel_light=PASTEL_L, pastel_normal=PASTEL_N, pastel_dark=PASTEL_D)
            print("COMPLETED")

        if SHOW_PREVIEW:
            prn.print_template_palette_preview(extractor.extracted_colors_dict, EXPORT_PALETTE_TEMPLATES, 'hsv')

        save_file = True
        if SAVE_CHECK:
            save_message = "Do you want to save this palette? [y/n]: "
            while True:
                user_choice = input(save_message)
                user_choice = user_choice.lower()

                if user_choice in ('y', 'yes'):
                    break
                elif user_choice in ('n', 'no'):
                    save_file = False
                    break

        if save_file:
            extractor.set_color_format(EXPORT_COLOR_FORMAT)

            if SAVE_RAW:
                futils.raw_dump(extractor.extracted_colors_dict, IMAGE_NAMES[index], OUTPUT_PATH, EXPORT_FILE_FORMAT, EXPORT_COLOR_FORMAT)
            else:
                palettes = extractor.generate_palettes(EXPORT_PALETTE_TEMPLATES)
                futils.save_palettes(palettes, EXPORT_PALETTE_TEMPLATES, IMAGE_NAMES[index], OUTPUT_PATH, EXPORT_FILE_FORMAT, EXPORT_COLOR_FORMAT, pastel_light=PASTEL_L, pastel_normal=PASTEL_N, pastel_dark=PASTEL_D)

        if index < len(PROPER_IMAGES)-1:    # Print blank line separator if there are more images.
            print()


# **************************************************************************
# **************************************************************************

##  Sets up the argument parser for command line arguments.
#
#   @return A command line argument parsing object.
def setup_argument_parser():
    desc = "PyPalEx is a color palette extraction tool "
    desc += "for extracting color palettes from images "
    desc += "into json / yaml files.\n"

    argument_parser = argparse.ArgumentParser(description=desc, usage="palex [options][arguments]")

    argument_parser.add_argument("-f", "--files", metavar="FILES", type=str, nargs="*",
                                 help="Specify the absolute file path(s). "
                                      "If used with -p --path option, you only need to specify the relative file path(s).")
    argument_parser.add_argument("-p", "--path", metavar="", type=str,
                                 help="Specify the path from where to use images. "
                                      "Absolute path is preferred, but relative path can also be used.")
    argument_parser.add_argument("-o", "--output", metavar="", type=str,
                                 help="Specify the output path where to store the JSON color palette.")
    argument_parser.add_argument("--save-check", action="store_true",
                                 help="Asks if the user wants to save the extracted color palettes.")
    argument_parser.add_argument("--preview", action="store_true",
                                 help="Shows a preview of the extracted color palettes before saving.")
    argument_parser.add_argument("--preview-check", action="store_true",
                                 help="Shows a preview of, and asks if the user wants to save, the extracted color palettes.")
    argument_parser.add_argument("--pastel", action="store_true",
                                 help="Converts all color types into pastel.")
    argument_parser.add_argument("--pastel-light", action="store_true",
                                 help="Converts light color type into pastel.")
    argument_parser.add_argument("--pastel-normal", action="store_true",
                                 help="Converts normal color type into pastel.")
    argument_parser.add_argument("--pastel-dark", action="store_true",
                                 help="Converts dark color type into pastel.")
    argument_parser.add_argument("-r", "--raw-dump", action="store_true",
                                 help="Saves the raw extracted colors without organizing them into color palettes.")
    argument_parser.add_argument("-g", "--gen-config", action="store_true",
                                 help="Generates a default configuration file.")
    argument_parser.add_argument("-w", "--where", action="store_true",
                                 help="Prints where the default output locations of the configuration file and extracted color palattes are located.")
    argument_parser.add_argument("-v", "--version", action="store_true",
                                 help="Prints the PyPalEx version.")

    return argument_parser


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Checks each of the sources provided and removes any bad sources.
#   @details    Any filepaths or source files that are not images or
#               do not exist get removed.
#
#   @param  filepaths   List of file paths.
#   @param  path        A path to the images, if it is provided.
#
#   @return True if all/some sources are good, False if all sources are bad.
def check_sources(filepaths, path=None):
    bad_source_paths = []
    for filepath in filepaths:
        source_filepath = filepath
        if path is not None:
            source_filepath = os.path.join(path, filepath)
        if not check_source(source_filepath):
            bad_source_paths.append(filepath)

    # Remove all the bad source paths from filepaths.
    for bad_source in bad_source_paths:
        filepaths.remove(bad_source)

    if len(filepaths) == 0:
        return False

    bad_source_paths.clear()

    # Check to make sure the remaining files are images.
    for filepath in filepaths:
        image_filepath = filepath
        if path is not None:
            image_filepath = os.path.join(path, filepath)
        if not filetype.is_image(image_filepath):
            bad_source_paths.append(filepath)
        else:
            try:
                Image.open(image_filepath)
            except IOError:
                bad_source_paths.append(filepath)

    # Remove all the bad images from filepaths.
    for bad_source in bad_source_paths:
        filepaths.remove(bad_source)

    # Return true if there are proper images that can be used.
    return len(filepaths) != 0


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Check the path to make sure it exists.
#
#   @param  path    The path to a directory.
#
#   @return True if the path exists and is not a file, False otherwise.
def check_path(path):
    return os.path.exists(path) and not os.path.isfile(path)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Handle the PyPalEx configuration file settings.
def handle_config():
    config_filepath = os.path.join(CONF_DIR, CONFIG_FILENAME)

    # If the configuration file doesn't exist, do nothing.
    if not os.path.exists(config_filepath) or not os.path.isfile(config_filepath):
        return

    global SAVE_CHECK
    global SHOW_PREVIEW
    global EXPORT_FILE_FORMAT
    global EXPORT_COLOR_FORMAT
    global EXPORT_PALETTE_TEMPLATES

    with open(config_filepath, 'r') as config_file:
        config_data = yaml.load(config_file, Loader=yaml.SafeLoader)

    for key, value in config_data.items():
        if key == 'save-check' and isinstance(value, bool):
            SAVE_CHECK = value
        elif key == 'show-preview' and isinstance(value, bool):
            SHOW_PREVIEW = value
        elif key == 'export-file-format' and value.lower() in ['json', 'yaml', 'yml']:
            EXPORT_FILE_FORMAT = value.lower()
        elif key == 'export-color-format' and value.lower() in ['hex', 'rgb', 'hsv', 'ansi']:
            EXPORT_COLOR_FORMAT = value.lower()
        elif key == 'exported-palettes' and isinstance(value, dict):
            EXPORT_PALETTE_TEMPLATES = value


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Sets the global variables using the arguments.
#
#   @param  args    User-supplied arguments.
def set_global_args(args):
    global EXPORT_PALETTE_TEMPLATES
    global SAVE_CHECK
    global SHOW_PREVIEW
    global SAVE_RAW
    global PASTEL_L
    global PASTEL_N
    global PASTEL_D
    global OUTPUT_PATH
    global PROPER_IMAGES
    global FILENAMES
    global IMAGE_NAMES

    if args['save_check'] or args['preview_check']:
        SAVE_CHECK = True
    if args['preview'] or args['preview_check']:
        SHOW_PREVIEW = True
    SAVE_RAW = args['raw_dump']
    PASTEL_L = args['pastel_light'] or args['pastel']
    PASTEL_N = args['pastel_normal'] or args['pastel']
    PASTEL_D = args['pastel_dark'] or args['pastel']

    OUTPUT_PATH = args['output'] if args['output'] is not None else ''
    args_path = args['path']

    for image_path in args['files']:
        filepath, filename = os.path.split(image_path)
        image_name, extension = filename.split('.')
        if args_path is not None:
            if filepath == '':
                filepath = args_path
            else:
                filepath = os.path.join(args_path, filepath)
        FILENAMES.append(filename)
        IMAGE_NAMES.append(image_name)
        PROPER_IMAGES.append(os.path.join(filepath, filename))

    # Check to make sure there are at least some default themes to export.
    if not EXPORT_PALETTE_TEMPLATES:
        default_light_theme = {'palette-type': 'light', 'color1': 'red', 'color2': 'green', 'color3': 'yellow',
                               'color4': 'blue', 'color5': 'magenta', 'color6': 'cyan', 'color9': 'dark red',
                               'color10': 'dark green', 'color11': 'dark yellow', 'color12': 'dark blue',
                               'color13': 'dark magenta', 'color14': 'dark cyan',
                               'contains-light': False, 'contains-normal': True, 'contains-dark': True}
        default_dark_theme = {'palette-type': 'dark', 'color1': 'red', 'color2': 'green', 'color3': 'yellow',
                              'color4': 'blue', 'color5': 'magenta', 'color6': 'cyan', 'color9': 'light red',
                              'color10': 'light green', 'color11': 'light yellow', 'color12': 'light blue',
                              'color13': 'light magenta', 'color14': 'light cyan',
                              'contains-light': True, 'contains-normal': True, 'contains-dark': False}
        EXPORT_PALETTE_TEMPLATES = {'light-theme': default_light_theme, 'dark-theme': default_dark_theme}
    else:
        for palette_name, colors_dict in EXPORT_PALETTE_TEMPLATES.items():
            # This will be used to identify individual pastel palettes during saving process.
            contains_light = False
            contains_normal = False
            contains_dark = False

            for key, color_name in colors_dict.items():
                # Remove case sensitivity from the color names.
                colors_dict[key] = color_name.lower()
                color_name = color_name.lower()

                if key == 'palette-type':
                    continue

                # A failsafe color if an incorrect color name was used in config file.
                if color_name not in VALID_COLOR_SET:
                    colors_dict[key] = 'black'
                    continue

                if color_name in {'light red', 'light yellow', 'light green', 'light cyan', 'light blue', 'light magenta'}:
                    contains_light = True
                elif color_name in {'red', 'yellow', 'green', 'cyan', 'blue', 'magenta'}:
                    contains_normal = True
                elif color_name in {'dark red', 'dark yellow', 'dark green', 'dark cyan', 'dark blue', 'dark magenta'}:
                    contains_dark = True

            EXPORT_PALETTE_TEMPLATES[palette_name]['contains-light'] = contains_light
            EXPORT_PALETTE_TEMPLATES[palette_name]['contains-normal'] = contains_normal
            EXPORT_PALETTE_TEMPLATES[palette_name]['contains-dark'] = contains_dark


# **************************************************************************
# **************************************************************************

##  Checks to make sure the path leads to a file.
#
#   @param  filepath    Path to file with filename and file extension.
#
#   @return True if file exists, False otherwise.
def check_source(filepath):
    return os.path.exists(filepath) and os.path.isfile(filepath)


# **************************************************************************
# ************** MAIN ************** MAIN ************** MAIN **************
# **************************************************************************
if __name__ == '__main__':
    main()
