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


# ---- IMPORTS ----
import sys
import os
import argparse
import filetype
from PIL import Image

from .settings import __version__, CONF_DIR
from .Extractor import Extractor
from . import image_utils as imutils
from . import arg_messages as argmsg

# ---- GLOBAL VARIABLES ----
## List of Extractor class objects for each individual image.
EXTRACTORS = []
## List of real/existing image file path(s).
PROPER_IMAGES = []
## List of image filenames.
FILENAMES = []
## List of output file path(s) for each image.
OUTPUT_FILEPATHS = []
## The path to the output directory where all JSON files will be saved.
OUTPUT_PATH = ''
## The tail to append to each output filepath.
OUTPUT_TAIL = "-color_palette.json"
## Flag to convert light color palette to pastel.
PASTEL_L = False
## Flag to convert normal color palette to pastel.
PASTEL_N = False
## Flag to convert dark color palette to pastel.
PASTEL_D = False
## Flag that gives preference to more saturated colors of the light color palette.
SAT_PREF_L = False
## Flag that gives preference to more saturated colors of the normal color palette.
SAT_PREF_N = False
## Flag that gives preference to more saturated colors of the dark color palette.
SAT_PREF_D = False


# **************************************************************************
# ****** CODE ORGANIZED HIGH-LEVEL to LOW-LEVEL WITH SECTION DIVIDERS ******
# **************************************************************************

##  Main script function.
def main():
    handle_args()
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    extract_color_palettes()

    # Save extracted palettes to file.
    for extractor in EXTRACTORS:
        imutils.save_palette_to_file(extractor.color_palette_dict, extractor.output_filepath)


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

    set_global_args(args)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Handles color extraction from image(s).
def extract_color_palettes():
    global EXTRACTORS

    for index, image_dir in enumerate(PROPER_IMAGES):
        print("Processing ", FILENAMES[index], " : ",  sep='', end='')
        image = Image.open(image_dir)
        hsv_img_matrix_2d = imutils.process_image(image)
        print("COMPLETED")
        print("Extracting Colors : ", sep='', end='')
        extractor = Extractor(hsv_img_matrix_2d, OUTPUT_FILEPATHS[index], PASTEL_L, PASTEL_N, PASTEL_D, SAT_PREF_L, SAT_PREF_N, SAT_PREF_D)
        extractor.run()
        EXTRACTORS.append(extractor)
        print("COMPLETED")


# **************************************************************************
# **************************************************************************

##  Sets up the argument parser for command line arguments.
#
#   @return A command line argument parsing object.
def setup_argument_parser():
    desc = "PyPalEx is a color palette extraction tool "
    desc += "for extracting light, normal and dark color "
    desc += "palettes from images into json files.\n"

    argument_parser = argparse.ArgumentParser(description=desc, usage="palex [options][arguments]")

    argument_parser.add_argument("-f", "--files", metavar="FILES", type=str, nargs="*",
                                 help="Specify the absolute file path(s). "
                                      "If used with -p --path option, you only need to specify the relative file path(s).")
    argument_parser.add_argument("-p", "--path", metavar="", type=str,
                                 help="Specify the path from where to use images. "
                                      "Absolute path is preferred, but relative path can also be used.")
    argument_parser.add_argument("-o", "--output", metavar="", type=str,
                                 help="Specify the output path where to store the JSON color palette.")
    argument_parser.add_argument("--pastel", action="store_true",
                                 help="Converts all color palettes into pastel.")
    argument_parser.add_argument("--pastel-light", action="store_true",
                                 help="Converts light color palette into pastel.")
    argument_parser.add_argument("--pastel-normal", action="store_true",
                                 help="Converts normal color palette into pastel.")
    argument_parser.add_argument("--pastel-dark", action="store_true",
                                 help="Converts dark color palette into pastel.")
    argument_parser.add_argument("--sat_pref", action="store_true",
                                 help="Gives preference to more saturated colors of all color palettes.")
    argument_parser.add_argument("--sat_pref-light", action="store_true",
                                 help="Gives preference to more saturated colors of the light color palette.")
    argument_parser.add_argument("--sat_pref-normal", action="store_true",
                                 help="Gives preference to more saturated colors of the normal color palette.")
    argument_parser.add_argument("--sat_pref-dark", action="store_true",
                                 help="Gives preference to more saturated colors of the dark color palette.")
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

##  Sets the global variables using the arguments.
#
#   @param  args    User-supplied arguments.
def set_global_args(args):
    global PASTEL_L
    global PASTEL_N
    global PASTEL_D
    global SAT_PREF_L
    global SAT_PREF_N
    global SAT_PREF_D
    global OUTPUT_PATH
    global OUTPUT_FILEPATHS
    global PROPER_IMAGES
    global FILENAMES

    PASTEL_L = args['pastel_light'] or args['pastel']
    PASTEL_N = args['pastel_normal'] or args['pastel']
    PASTEL_D = args['pastel_dark'] or args['pastel']
    SAT_PREF_L = args['sat_pref_light'] or args['sat_pref']
    SAT_PREF_N = args['sat_pref_normal'] or args['sat_pref']
    SAT_PREF_D = args['sat_pref_dark'] or args['sat_pref']

    OUTPUT_PATH = args['output'] if args['output'] is not None and args['output'] != '' else CONF_DIR
    args_path = args['path']

    for image_path in args['files']:
        filepath, filename = os.path.split(image_path)
        filename, extension = filename.split('.')
        if args_path is not None:
            if filepath == '':
                filepath = args_path
            else:
                filepath = os.path.join(args_path, filepath)
        FILENAMES.append(filename)
        PROPER_IMAGES.append(os.path.join(filepath, filename) + "." + extension)
        OUTPUT_FILEPATHS.append(os.path.join(OUTPUT_PATH, filename) + OUTPUT_TAIL)


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
