##  @file   arg_messages.py
#   @brief  Archive of messages to display for arguments supplied by user.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on March 3, 2022.
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 6, 2023.
#   - Modified by Al Timofeyev on July 8, 2024.


##  Generates an error message if the sources provided were not images.
#
#   @return The "bad sources" message.
def bad_source_message():
    message = "------------------------------------------\n"
    message += "********** EXECUTION TERMINATED **********\n"
    message += "------------------------------------------\n"
    message += "The image sources provided contained no\n"
    message += "valid images for PyPalEx to work with.\n"
    return message


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Generates an error message if the directory provided is not a valid directory.
#
#   @return The "bad directory" message.
def bad_path_message():
    message = "------------------------------------------\n"
    message += "********** EXECUTION TERMINATED **********\n"
    message += "------------------------------------------\n"
    message += "The path provided is not a valid path\n"
    message += "for PyPalEx to work with.\n"
    return message


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Generates a help message if no arguments were presented.
#
#   @return The "no arguments" help message.
def no_args_help_message():
    message = "------------------------------------------\n"
    message += "********** EXECUTION TERMINATED **********\n"
    message += "------------------------------------------\n"
    message += "No Options were provided. Please use Options with PyPalEx.\n"
    message += "Examples:\n"
    message += "palex -f /path/to/images/image_name.png\n"
    message += "palex -f image_name.png -p /path/to/images/\n"
    message += "palex -f image_name1.jpg image_name2.png -p /path/to/images\n"
    message += "palex -f image_name.png -p /path/to/images/ -o /path/to/output/\n"
    message += "palex -p /path/to/images/\n"
    message += "palex -p /path/to/images/ -o /path/to/output/\n\n"
    message += "Or any combination of -f, -p, -o, but you MUST have at least\n"
    message += "either a -f or a -p argument set for PyPalEx to work.\n"
    message += "Option -f accepts multiple arguments while Options -p and -o\n"
    message += "accept only one argument.\n\n"
    message += "For a full description of the available arguments, please use\n"
    message += "the -h or --help Option. (e.g. palex -h)\n"
    return message
