"""
#######################################################################
Author:   Al Timofeyev
Date:     February 2, 2022
Desc:     This project is for color palette extraction from an image.
#######################################################################
"""

# ---- IMPORTS ----
from .settings import CONF_DIR
import sys
import os
import argparse # for CLI arguments.
import filetype # for checking for image files only
from PIL import Image
import multiprocessing
from Extractor import Extractor
import image_utils as imutils

# ---- GLOBAL VARIABLES ----
EXTRACTORS = []
PROPER_IMAGES = []
OUTPUT_DIRS = []
OUTPUT_DIR = ''
OUTPUT_TAIL = "-color_palette.json"
ARGUMENT_PARSER = None


def check_sources(image_paths, directory=None):
    """

    :param image_paths:
    :param directory:
    :return:
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


def check_source(image_path):
    """
    Checks to make sure the path is either a file or directory
    :param image_path:
    :return:
    """
    return os.path.exists(image_path) and os.path.isfile(image_path)


def check_path(full_path):
    """
    Check the full path to make sure the directory exists.
    :param full_path:
    :return:
    """
    return os.path.exists(full_path) and not os.path.isfile(full_path)


def set_global_args(args):
    """
    Sets the global variables using the arguments.
    :param args:    User-supplied arguments.
    """
    global OUTPUT_DIR
    global OUTPUT_DIRS
    global PROPER_IMAGES

    OUTPUT_DIR = args['Output'] if args['Output'] is not None and args['Output'] != '' else CONF_DIR
    args_directory = args['Directory']

    for image_path in args['Files']:
        directory, filename = os.path.split(image_path)
        filename, extension = filename.split('.')
        if args_directory is not None:
            if directory == '':
                directory = args_directory
            else:
                directory = os.path.join(args_directory, directory)
        PROPER_IMAGES.append(os.path.join(directory, filename) + "." + extension)
        OUTPUT_DIRS.append(os.path.join(OUTPUT_DIR, filename) + OUTPUT_TAIL)


def setup_argument_parser():
    """ Sets up the argument parser for command line arguments. """
    global ARGUMENT_PARSER

    description = "PyPalEx is a color palette extraction tool "
    description += "for extracting light, normal and dark color "
    description += "palettes from images into json files."

    ARGUMENT_PARSER = argparse.ArgumentParser(description)

    ARGUMENT_PARSER.add_argument("-f", "--Files", metavar="FILES", nargs="*",
                                 help="Specify the file path(s). (e.g. -f /path/to/images/image.png) "
                                      "If used with '-d' directory option, you only need to list the filename(s). "
                                      "(e.g. -f image1.png image2.jpeg -d /path/to/images/)")
    ARGUMENT_PARSER.add_argument("-d", "--Directory", metavar="",
                                 help="Specify the directory from where to convert images. "
                                      "(e.g. -d /path/to/images/)")
    ARGUMENT_PARSER.add_argument("-o", "--Output", metavar="",
                                 help="Specify the output directory where to store the JSON color palette. "
                                      "(e.g. -o /path/to/output/)")


def handle_args():
    """ Handles the arguments passed to PyPalEx. """
    # Converts arguments into a dictionary:
    # {'File': None, 'Directory': None, 'Output': None}
    args = vars(ARGUMENT_PARSER.parse_args())

    # Exit if no files/directories were provided.
    if (args['Files'] is None or args['Files'] == []) and args['Directory'] is None:
        sys.exit(no_args_help_message())

    # Check either the file(s) or the file(s) in directory to make sure
    # there are valid images to work with.
    if args['Files']:
        if not check_sources(args['Files'], args['Directory']):
            sys.exit(bad_source_message())
    elif args['Directory'] is not None:
        if not check_path(args['Directory']):
            sys.exit(bad_directory_message())
        args['Files'] = os.listdir(args['Directory'])
        if not check_sources(args['Files'], args['Directory']):
            sys.exit(bad_source_message())

    set_global_args(args)


def bad_source_message():
    """
    Returns an error message if the sources provided were not images.
    :return: The "bad sources" message.
    """
    message = "**** Execution Terminated ****\n"
    message += "The image sources provided contained no valid images\n"
    message += "for PyPalEx to work with.\n"
    return message


def bad_directory_message():
    """
    Returns an error message if the directory provided is not a
    valid directory.
    :return: The "bad directory" message.
    """
    message = "**** Execution Terminated ****\n"
    message += "The directory provided is not a valid directory\n"
    message += "for PyPalEx to work with.\n"
    return message


def no_args_help_message():
    """
    Returns a help message if no arguments were presented.
    :return: The "no arguments" help message.
    """
    message = "**** Execution Terminated ****\n"
    message += "No Options were provided. Please use Options with PyPalEx.\n"
    message += "Examples:\n"
    message += "pypalex -f /path/to/images/image_name.png\n"
    message += "pypalex -f image_name.png -d /path/to/images/\n"
    message += "pypalex -f image_name1.jpg image_name2.png -d /path/to/images\n"
    message += "pypalex -f image_name.png -d /path/to/images/ -o /path/to/output/\n"
    message += "pypalex -d /path/to/images/\n"
    message += "pypalex -d /path/to/images/ -o /path/to/output/\n\n"
    message += "Or any combination of -f, -d, -o, but you MUST have at least\n"
    message += "either a -f or a -d argument set for PyPalEx to work.\n"
    message += "Option -f accepts multiple arguments while Options -d and -o\n"
    message += "accept only one argument.\n\n"
    message += "For a full description of the available arguments, please use\n"
    message += "the -h or --help Option. (e.g. pypalex -h)\n"
    return message


def thread_helper(extractor):
    """
    Supports multiprocess color extraction operations.
    :param extractor:   The Extractor object for which to run extraction process.
    :return:    The Extractor object.
    """
    extractor.run()
    return extractor


def extract_color_palettes():
    """ Handles multiprocess color extraction from image(s). """
    global EXTRACTORS

    # Prepare Extractor object(s).
    for index, image_dir in enumerate(PROPER_IMAGES):
        image = Image.open(image_dir)
        full_hsl_img_array = imutils.process_image(image)
        extractor = Extractor(full_hsl_img_array, OUTPUT_DIRS[index])
        EXTRACTORS.append(extractor)

    # Begin multiprocess extraction operations.
    pool = multiprocessing.Pool()
    EXTRACTORS = pool.map(thread_helper, EXTRACTORS)
    pool.close()
    pool.join()


# --------------------------------------------------------------------------
# ---------------------------------- MAIN ----------------------------------
# --------------------------------------------------------------------------
def main():
    """ Main script function. """
    handle_args()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    extract_color_palettes()

    # Save extracted palettes to file.
    for index, extractor in enumerate(EXTRACTORS):
        imutils.save_palette_to_file(extractor.color_palette_dict, extractor.output_path)


if __name__ == '__main__':
    setup_argument_parser()
    main()
