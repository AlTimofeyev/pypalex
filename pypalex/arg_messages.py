"""!
#######################################################################
@author Al Timofeyev
@date   March 3, 2022
@brief  Archive of messages to display for arguments supplied by user.
#######################################################################
"""


def bad_source_message():
    """!
    @brief  Returns an error message if the sources provided were not images.
    @return The "bad sources" message.
    """
    message = "**** Execution Terminated ****\n"
    message += "The image sources provided contained no valid images\n"
    message += "for PyPalEx to work with.\n"
    return message


def bad_directory_message():
    """!
    @brief  Returns an error message if the directory provided is not a valid directory.
    @return The "bad directory" message.
    """
    message = "**** Execution Terminated ****\n"
    message += "The directory provided is not a valid directory\n"
    message += "for PyPalEx to work with.\n"
    return message


def no_args_help_message():
    """!
    @brief  Returns a help message if no arguments were presented.
    @return The "no arguments" help message.
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
