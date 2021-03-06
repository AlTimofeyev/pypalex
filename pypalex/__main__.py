"""!
#######################################################################
@author Al Timofeyev
@date   February 2, 2022
@brief  Main script for PyPalEx.
@details    This tool is for extracting color palettes from images.
#######################################################################
"""

# ---- IMPORTS ----
import sys
import os
import argparse
import filetype
from PIL import Image
import multiprocessing

from .settings import __version__, CONF_DIR
from .Extractor import Extractor
from . import image_utils as imutils
from . import arg_messages as argmsg

# ---- GLOBAL VARIABLES ----
EXTRACTORS = []
PROPER_IMAGES = []
OUTPUT_DIRS = []
OUTPUT_DIR = ''
OUTPUT_TAIL = "-color_palette.json"
PASTEL = False
PASTEL_L = False
PASTEL_N = False
PASTEL_D = False


def thread_helper(extractor):
    """!
    @brief  Supports multiprocess color extraction operations.
    @param  extractor   The Extractor object for which to run extraction process.
    @return The Extractor object.
    """
    extractor.run()
    return extractor

# ---------------------------------------------------------------
# ---------------------------------------------------------------


def extract_color_palettes():
    """! Handles multiprocess color extraction from image(s). """
    global EXTRACTORS

    # Prepare Extractor object(s).
    for index, image_dir in enumerate(PROPER_IMAGES):
        image = Image.open(image_dir)
        full_hsl_img_array = imutils.process_image(image)
        extractor = Extractor(full_hsl_img_array, OUTPUT_DIRS[index], PASTEL, PASTEL_L, PASTEL_N, PASTEL_D)
        EXTRACTORS.append(extractor)

    # Begin multiprocess extraction operations.
    pool = multiprocessing.Pool()
    EXTRACTORS = pool.map(thread_helper, EXTRACTORS)
    pool.close()
    pool.join()

# ***********************************************************************
# ***********************************************************************


def set_global_args(args):
    """!
    @brief  Sets the global variables using the arguments.
    @param  args    User-supplied arguments.
    """
    global PASTEL
    global PASTEL_L
    global PASTEL_N
    global PASTEL_D
    global OUTPUT_DIR
    global OUTPUT_DIRS
    global PROPER_IMAGES

    PASTEL = args['pastel']
    PASTEL_L = args['pastel_light']
    PASTEL_N = args ['pastel_normal']
    PASTEL_D = args['pastel_dark']

    OUTPUT_DIR = args['output'] if args['output'] is not None and args['output'] != '' else CONF_DIR
    args_directory = args['directory']

    for image_path in args['files']:
        directory, filename = os.path.split(image_path)
        filename, extension = filename.split('.')
        if args_directory is not None:
            if directory == '':
                directory = args_directory
            else:
                directory = os.path.join(args_directory, directory)
        PROPER_IMAGES.append(os.path.join(directory, filename) + "." + extension)
        OUTPUT_DIRS.append(os.path.join(OUTPUT_DIR, filename) + OUTPUT_TAIL)

# ***********************************************************************
# ***********************************************************************


def check_source(image_path):
    """!
    @brief  Checks to make sure the path is either a file or directory
    @param  image_path  Path to image with filename and file extension (.jpg, .png, etc.).
    @return Boolean flag: True if file exists, False otherwise.
    """
    return os.path.exists(image_path) and os.path.isfile(image_path)

# ---------------------------------------------------------------
# ---------------------------------------------------------------


def check_sources(image_paths, directory=None):
    """!
    @brief  Checks each of the sources provided.
    @param  image_paths Array of image paths.
    @param  directory   A directory path to the images, if it is provided.
    @return Boolean flag: True if all/some sources are good, False if all sources are bad.
    """
    bad_image_paths = []
    for img_name in image_paths:
        full_image_path = img_name
        if directory is not None:
            full_image_path = os.path.join(directory, img_name)
        if not check_source(full_image_path):
            bad_image_paths.append(img_name)

    # Remove all the 'bad images' from image_paths.
    for bad_image in bad_image_paths:
        image_paths.remove(bad_image)

    if len(image_paths) == 0:
        return False

    bad_image_paths.clear()

    # Check to make sure the remaining files are images.
    for img_name in image_paths:
        full_image_path = img_name
        if directory is not None:
            full_image_path = os.path.join(directory, img_name)
        if not filetype.is_image(full_image_path):
            bad_image_paths.append(img_name)
        else:
            try:
                Image.open(full_image_path)
            except IOError:
                bad_image_paths.append(img_name)

    # Remove all the 'bad images' from image_paths.
    for bad_image in bad_image_paths:
        image_paths.remove(bad_image)

    # Return true if there are proper images that can be used.
    return len(image_paths) != 0

# ***********************************************************************
# ***********************************************************************


def check_path(full_path):
    """!
    @brief  Check the full path to make sure the directory exists.
    @param  full_path   The full path to directory.
    @return Boolean flag: True if directory exists and is not a file, False otherwise.
    """
    return os.path.exists(full_path) and not os.path.isfile(full_path)

# ***********************************************************************
# ***********************************************************************


def setup_argument_parser():
    """!
    @brief  Sets up the argument parser for command line arguments.
    @return A command line argument parsing object.
    """
    desc = "PyPalEx is a color palette extraction tool "
    desc += "for extracting light, normal and dark color "
    desc += "palettes from images into json files.\n"

    argument_parser = argparse.ArgumentParser(description=desc, usage="palex [options][arguments]")

    argument_parser.add_argument("-f", "--files", metavar="FILES", type=str, nargs="*",
                                 help="Specify the file path(s). (e.g. -f /path/to/images/image.png) "
                                      "If used with '-d' directory option, you only need to list the filename(s). "
                                      "(e.g. -f image1.png image2.jpeg -d /path/to/images/)")
    argument_parser.add_argument("-d", "--directory", metavar="", type=str,
                                 help="Specify the directory from where to use images. "
                                      "(e.g. -d /path/to/images/)")
    argument_parser.add_argument("-o", "--output", metavar="", type=str,
                                 help="Specify the output directory where to store the JSON color palette. "
                                      "(e.g. -o /path/to/output/)")
    argument_parser.add_argument("-p", "--pastel", action="store_true",
                                 help="Converts all palettes to pastel.")
    argument_parser.add_argument("--pastel-light", action="store_true",
                                 help="Converts light palette to pastel.")
    argument_parser.add_argument("--pastel-normal", action="store_true",
                                 help="Converts normal palette to pastel.")
    argument_parser.add_argument("--pastel-dark", action="store_true",
                                 help="Converts dark palette to pastel.")
    argument_parser.add_argument("-v", "--version", action="store_true",
                                 help="Prints the PyPalEx version.")

    return argument_parser

# ***********************************************************************
# ***********************************************************************


def handle_args():
    """! Handles the arguments passed to PyPalEx. """
    # Converts arguments into a dictionary:
    # {'files': None, 'directory': None, 'output': None}
    argument_parser = setup_argument_parser()
    args = vars(argument_parser.parse_args())

    # Check if pypalex version was requested.
    if args['version']:
        print("pypalex ", __version__, sep="")
        sys.exit()

    # Exit if no files/directories were provided.
    if (args['files'] is None or args['files'] == []) and args['directory'] is None:
        sys.exit(argmsg.no_args_help_message())

    # Check either the file(s) or the file(s) in directory to make sure
    # there are valid images to work with.
    if args['files']:
        if not check_sources(args['files'], args['directory']):
            sys.exit(argmsg.bad_source_message())
    elif args['directory'] is not None:
        if not check_path(args['directory']):
            sys.exit(argmsg.bad_directory_message())
        args['files'] = os.listdir(args['directory'])
        if not check_sources(args['files'], args['directory']):
            sys.exit(argmsg.bad_source_message())

    set_global_args(args)


# --------------------------------------------------------------------------
# ---------------------------------- MAIN ----------------------------------
# --------------------------------------------------------------------------
def main():
    """! Main script function. """
    handle_args()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    extract_color_palettes()

    # Save extracted palettes to file.
    for extractor in EXTRACTORS:
        imutils.save_palette_to_file(extractor.color_palette_dict, extractor.output_path)


if __name__ == '__main__':
    main()
