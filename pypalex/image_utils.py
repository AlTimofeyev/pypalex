"""!
#######################################################################
@author Al Timofeyev
@date   February 27, 2022
@brief  Utilities for processing image and file handling.
#######################################################################
"""

# ---- IMPORTS ----
from PIL import Image
import numpy
import multiprocessing
import json
from . import conversion_utils as convert


def process_image(image):
    """!
    @brief  Processes PIL Image object.
    @details    Multiprocessing example from: https://stackoverflow.com/a/45555516
    @param  image   PIL Image object.
    @return List of full hsl arrays (pixels) of image.
    """
    # Rescale image to reduce data sample.
    new_size = rescale_image(image)
    resized_img = image.resize(new_size, Image.LANCZOS)
    img_array = numpy.array(resized_img)

    # Flatten image array and remove duplicate pixel values.
    flat_img_array = img_array.reshape(-1, 3)

    # Split image array into multiple arrays and remove empty arrays.
    split_rgb_img_arrays = numpy.array_split(flat_img_array, multiprocessing.cpu_count())
    split_rgb_img_arrays = [x for x in split_rgb_img_arrays if x.size > 0]

    # Multi-thread the conversion process from [r,g,b] to [h,s,l].
    pool = multiprocessing.Pool()
    converted_results = pool.map(thread_helper, split_rgb_img_arrays)
    pool.close()
    pool.join()

    # Combine and sort all the individual arrays.
    # Sort each of the hsl arrays by 3rd(l), 2nd(s), and then 1st(h) column.
    full_hsl_img_array = numpy.concatenate(converted_results)
    full_hsl_img_array = full_hsl_img_array[numpy.lexsort((full_hsl_img_array[:, 2], full_hsl_img_array[:, 1], full_hsl_img_array[:, 0]))]

    return full_hsl_img_array

# ---------------------------------------------------------------
# ---------------------------------------------------------------


def rescale_image(img):
    """!
    @brief  Rescales image to a smaller sampling size.
    @param  img The PIL.Image object.
    @return Tuple of the new width and height of image.
    """
    width, height = img.size
    default_480p = [854, 480]   # 480p SD resolution with 16:9 ratio.
    default_360p = [640, 360]   # 360p SD resolution with 16:9 ratio.

    # Try scaling images down to 480p with 16:9 ratio.
    if height < width:      # ---- Landscape, 16:9 ratio.
        percent_change_width = default_480p[0] / width
        percent_change_height = default_480p[1] / height
    elif width < height:    # ---- Portrait, 9:16 ratio.
        percent_change_width = default_480p[1] / width
        percent_change_height = default_480p[0] / height
    else:                   # ---- Square, 1:1 ratio.
        percent_change_width = default_360p[0] / width
        percent_change_height = default_360p[0] / height

    width *= percent_change_width
    height *= percent_change_height

    return round(width), round(height)

# ---------------------------------------------------------------
# ---------------------------------------------------------------


def thread_helper(flat_img_array):
    """!
    @brief  Helper function for multiprocessing conversion operations.
    @details    Helps convert from [r, g, b] to [h, s, l].
    @param  flat_img_array  A flattened rgb portion of the original image array.
    @return A numpy array of converted hsl values.
    """
    return numpy.apply_along_axis(convert.rgb_to_hsl, 1, flat_img_array)

# ***********************************************************************
# ***********************************************************************


def save_palette_to_file(color_palette, output_file):
    """!
    @brief  Saves color palette to json file.
    @details    If a file with the same name already exists, it is overwritten.
    @param  color_palette   Dictionary of light, normal, and dark color palettes.
    @param  output_file The output path/directory with filename at the end.
    """
    with open(output_file, 'w') as outfile:
        json.dump(color_palette, outfile, indent=4)
