##  @file   image_utils.py
#   @brief  Utilities for processing image and file handling.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on February 27, 2022.
#   - Modified by Al Timofeyev on April 21, 2022.
#   - Modified by Al Timofeyev on March 6, 2023.
#   - Modified by Al Timofeyev on April 5, 2023.
#   - Modified by Al Timofeyev on May 16, 2024.


# ---- IMPORTS ----
import numpy
import multiprocessing
from PIL import Image
from . import conversion_utils as convert


##  Processes PIL Image object.
#   @details    Multiprocessing example from: https://stackoverflow.com/a/45555516
#
#   @param  image   PIL Image object.
#
#   @return 2D numpy array of [h,s,v] arrays (pixels) from image.
def process_image(image):
    # Make sure image is in [r,g,b] format.
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Rescale image to reduce data sample.
    new_size = rescale_image(image)
    resized_img = image.resize(new_size, Image.LANCZOS)
    img_matrix_3d = numpy.array(resized_img)

    # Flatten image matrix into 2D.
    rgb_img_matrix_2d = img_matrix_3d.reshape(-1, 3)

    # Split image array into multiple arrays and remove empty arrays.
    split_rgb_img_arrays = numpy.array_split(rgb_img_matrix_2d, multiprocessing.cpu_count())
    split_rgb_img_arrays = [x for x in split_rgb_img_arrays if x.size > 0]

    # Multi-thread the conversion process from [r,g,b] to [h,s,v].
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    async_result = pool.map_async(process_helper, split_rgb_img_arrays)
    pool.close()
    pool.join()

    converted_hsv_results = []
    for value in async_result.get():
        converted_hsv_results.append(value)

    # Combine and sort all the individual [h,s,v] arrays by 3rd(v), 2nd(s), and then 1st(h) column.
    hsv_matrix_2d = numpy.concatenate(converted_hsv_results)
    hsv_matrix_2d = hsv_matrix_2d[numpy.lexsort((hsv_matrix_2d[:, 2], hsv_matrix_2d[:, 1], hsv_matrix_2d[:, 0]))]

    return hsv_matrix_2d


# **************************************************************************
# **************************************************************************

##  Rescales image to a smaller sampling size while maintaining aspect ration.
#
#   @note   The math behind rescaling the image came
#           from: https://math.stackexchange.com/a/3078131
#
#   @param  image   PIL Image object.
#
#   @return Tuple of the new width and height of image.
def rescale_image(image):
    width, height = image.size
    default_480p = [854, 480]   # 480p SD resolution with 16:9 ratio.
    default_360p = [640, 360]   # 360p SD resolution with 16:9 ratio.

    # Try scaling images down to 480p.
    # new_width = (width/height) * new_height
    # new_height = (height/width) * new_width
    if height < width:  # ---- Landscape.
        new_width = default_480p[0]
        new_height = round((height / width) * new_width)

        if new_height > default_480p[1]:
            new_height = default_480p[1]
            new_width = round((width / height) * new_height)
    elif width < height:  # ---- Portrait.
        new_height = default_480p[0]
        new_width = round((width / height) * new_height)

        if new_width > default_480p[1]:
            new_width = default_480p[1]
            new_height = round((height / width) * new_width)
    else:  # ---- Square, 1:1 ratio.
        new_width = default_360p[0]
        new_height = round((width / height) * new_width)

    return round(new_width), round(new_height)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

##  Helper function for multiprocessing conversion operations.
#   @details    Helps convert from [r,g,b] to [h,s,v].
#
#   @param  rgb_matrix_2d   A 2D matrix of rgb values.
#
#   @return A numpy array/2D matrix of converted [h,s,v] values.
def process_helper(rgb_matrix_2d):
    return numpy.apply_along_axis(convert.rgb_to_hsv, 1, rgb_matrix_2d)
