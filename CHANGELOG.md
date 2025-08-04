# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<br>

## Unreleased
- . . .

<br>

## [2.2.2] - 2025-08-03
- CHANGED: Changed the `organize_extracted_dictionary()` function in the **Extractor.py** file.
  - The `organize_extracted_dictionary()` function was missing the 6 newly added colors, causing an issue with palette generation (which wasn't detecting the new colors and throwing errors).

<br>

## [2.2.1] - 2025-08-03
- CHANGED: Indentation issue in the **__main__.py** file was resolved.
  - There was an `if...else` conditional statement int the `extract_color_palettes()` function that was indented one level deeper than it should have been, resulting in extracted color palettes not saving.

<br>

## [2.2.0] - 2024-12-15
- This update was delayed to August 2025.
- ADDED: Added 6 new colors to the **constants.py** file to be extracted along with the original 6.
    - Added orange, chartreuse, spring, azure, violet and rose.
    - Adjusted some existing color constants in the process.
- ADDED: Added more color format conversion functions to the **conversion_utils.py** file.
    - Added `hex_to_hsv()`, `hsv_to_ansi()`, `ansi_to_hsv()`, `hex_to_ansi()` and `ansi_to_hex()`.
- CHANGED: Changed he **constants.py** file.
    - Changed the `SATURATION_TOLERANCE_RANGE` constant value from `[10.0, 15.0]` to `[15.0, 20.0]`.
    - Changed the `PASTEL_SATURATION_RANGE` constant value from `[15.0, 75.0]` to `[20.0, 55.0]`.
- CHANGED: Changed the **print_utils.py** file.
  - Added `print_raw_colors()` function to allow for printing raw extracted colors to the Terminal.
    - This is for when the user wants to extract only the raw colors (not palettes) but also wants to print a preview.
  - Added `print_palette_preview()` function, a simplified version of the prior print palette function that uses already-made palettes.
  - Deprecated the following two functions in favor of `print_palette_preview()`:
    - `print_default_palette_preview()`
    - `print_template_palette_preview()`
    - These two functions will remain in this new version update, just in case there might be a use for them.
- CHANGED: Changed the **file_utils.py** file.
    - Changed the `generate_config_file()` function to include the new colors.
    - Refactored the `save_palettes()` function header and the beginning of the function.
      - Removed the pastel optional parameters from the header in favor of an optional dictionary that would contain the same values.
    - Added a `export_file_format` check at the beginning of all the functions in this file, except `generate_config_file()`, to make sure it's a supported format.
- CHANGED: Changed the **Extractor.py** file and class.
    - Added `math` and `stat` packages to this file.
    - Moved the image processing portion of the package into the `Extractor` class.
      - This class now contains a `load()` function to load the Extractor class with an image before using the `run()` function.
    - Added support for the 6 new colors.
    - Added `generate_mood_palettes()` and `generate_adaptive_palettes()` functions to generate mood and adaptive color palettes.
    - Changed the `set_color_format()` function to be able to modify the color format of both the extracted colors dictionary or any color palette dictionary that is passed to this function.
      - This function can now change the color format more than once, removing the limit from the last update.
    - Changed the `convert_pastel()` function so that the saturation is adjusted regardless if it was already set to a proper saturation.
- CHANGED: Changed the **extraction_utils.py** file.
    - Changed `check_missing_color_types()` function to use `new_bounds[0] +` for borrowing color types.
      - Previously, some of the color-type-checks used `new_bounds[1] -` instead, so I changed that for this update.
    - Changed the linear color ordering to be more intuitive.
      - From *(left side)*`['red', 'rose', 'magenta', 'violet', 'blue', 'azure', 'cyan', 'spring', 'green', 'chartreuse', 'yellow', 'orange']`*(right side)*
      - To *(left side)*`['red', 'orange', 'yellow', 'chartreuse', 'green', 'spring', 'cyan', 'azure', 'blue', 'violet', 'magenta', 'rose']`*(right side)*
      - This will work better for mental visualization in the long run as the latter variation is more intuitive.
    - Changed `get_left_and_right_colors()` and `borrow_color()` functions to accommodate the change in linear color ordering.
    - Added the 6 new base colors into the extraction process for some functions.
    - Changed the `extract_colors()` function by adding a `ratios` parameter to the function header.
    - Changed the saturation and brightness values for black and white colors in `generate_black_and_white()` function.
    - Added ration type processing to the `sort_by_sat_and_bright_value()` function.
      - This will record the percentage/ratios of each color type for each of the base colors.
    - Added `get_dominant_color_name()` function to get the name of the dominant base color.
    - Added `get_hue_shift_value()` function to calculate how much to shift a hue based on the hue's range and on the percentage provided.
    - Added `calculate_dist_between_2_colors()` function to calculate the distance between two HSV colors.
    - Changed `check_missing_colors()` function to be more concise.
    - Added `set_missing_color()` function to support the `check_missing_colors()` function as there was repeated code.
    - Changed `find_closest_to_centroid()` function to use the new `calculate_dist_between_2_colors()` function.
- CHANGED: Changed the **__main__.py** file.

<br>

## [2.1.1] - 2024-07-08
- CHANGED: Changed the hex functions in **conversion_utils.py** file to use a `#` character before the hex string.
    - Changed the `rgb_to_hex()` and `hex_to_rgb()` functions.

<br>

## [2.1.0] - 2024-07-08
- ADDED: Added PyYAML to the package requirements and the GitHub Actions Workflows.
- ADDED: Added default output locations for extracted color palettes.
    - Added `DEFAULT_EXTRACTED_DIR`, `PASTEL_EXTRACTED_DIR` and `RAW_EXTRACTED_DIR` constant variables into the **settings.py** file.
    - These directories will be located in the same folder as the configuration file for this tool.
- ADDED: Added more options and configuration file handling to the **__main__.py** file.
    - Added `-r, --raw-dump` option.
    - Added `-g, --gen-config` option.
    - Added `-w, --where` option.
- ADDED: Added ANSI conversion functions to the **conversion_utils.py** file.
    - Added `rgb_to_ansi()` and `ansi_to_rgb()` functions.
- CHANGED: Changed the naming convention for the color names in **Extractor.py** and **extraction_utils.py** files to be all lowercase.
    - Made all color names lowercase (e.g. `Red` to `red`, `Dark Red` to `dark red`, etc.).
- CHANGED: Changed `extract_color_palettes()` function name to `extract_colors()` in **extraction_utils.py** and **Extractor.py** files.
- CHANGED: Refactored the **Extractor.py** file and added some new functions.
    - Added `convert_to_pastel()` function to replace `check_pastel_conversion()` function.
    - Added `organize_extracted_dictionary()` function to replace `construct_palette_dictionary()` function.
    - Added `set_color_format()`, `generate_palettes()` and `generate_default_palettes()` functions.
    - Removed unnecessary parameters from the _Extractor_ class constructor.
- CHANGED: Refactored the **arg_messages.py** file.
    - Corrected a misspelling of PyPalEx CLI call from `pypalex` to `palex`.
- CHANGED: Completely refactored the **print_utils.py** file to accommodate printing with palette templates.
    - Improved the readability of the code in this file. 
    - Removed all the previous functions from this file.
- CHANGED: Completely refactored the **file_utils.py** file.
    - Made `generate_config_file()` function for generating a configuration file.
    - Made `raw_dump()` function for saving the raw extracted colors to a file.
    - Made `save_palettes()` function for saving organized palettes to files.
    - Removed all the previous functions from this file.

<br>

## [2.0.0] - 2024-06-10
- ADDED: Updated **setup.py** to include project links on the official PyPI Package Homepage.
- FIXED: Fixed a bug where the `--pastel, /light/normal/dark` options were broken because they were still reliant on the old `SATURATION_RANGE` and `BRIGHTNESS_RANGE` constants in the **constants.py** file.
    - Changed the `convert_pastel()` function in **Extractor.py** file to use the new constant values that were introduced in version 1.3.5.
- CHANGED: A color palette's saturation value is only converted to pastel if it is outside the pastel saturation range that is defined in the **constants.py** file.
- CHANGED: The `PASTEL_BRIGHTNESS_RANGE` is now set to be between 65.0 and 95.0 instead of 50.0 to 100.0 in the **constants.py** file.
- REMOVED: Removed the saturation preference options from package.
    - Removed any mention of saturation preference from **\_\_main\_\_.py** file.
    - Removed `sat_pref_light/norm/dark` and `sat_pref_list` variables from **Extractor.py** file.
    - Removed any use or mention of`sat_pref_list` from **extraction_utils.py** file:
        - Removed it from `extract_color_palettes()`, `extract_color_types()`, `extract_dominant_color()` and `find_closest_to_centroid()`.

<br>

## [1.3.5] - 2024-05-31
- ADDED: Added a black and dark brightness range as well as a saturation tolerance range to the **constants.py** file.
  - This was added to isolate black or indistinguishable colors from dark colors and achromatic/grayscale colors from saturated colors.
- CHANGED: Changed the name of `sort_by_bright_value()` to `sort_by_sat_and_bright_value()` as it now sorts by the saturation tolerance range as well.
- CHANGED: Changed `extract_color_types()`, `sort_by_sat_and_bright_value()` and `check_missing_color_types()` to account for the added black color range and saturation tolerance range from the **constants.py** file.
- REMOVED: Removed the `check_sat_and_bright()` function.
  - Everything this function did is now being done by the `check_missing_color_types()` function and the new constant variables in **constants.py**.
- REMOVED: Removed the `SATURATION_RANGE` and `BRIGHTNESS_RANGE` from the **constants.py** file.

<br>

## [1.3.4] - 2024-05-16
- CHANGED: The image rescale function in **image_utils.py**.
    - Images are now rescaled according to a proper mathematical formula and maintain their aspect ratio instead of hard-rescaling images to 480p with a 16:9 or 9:16 aspect ratio.
    - The math behind rescaling the image came from: https://math.stackexchange.com/a/3078131
    - If an image is smaller than the required sampling size of 480p, it is not rescaled.

<br>

## [1.3.3] - 2023-04-07
- ADDED: Added a `--save-check` option to ask if the user wants to save the extracted color palettes.
- ADDED: Added a `--preview` option to show a preview of extracted color palette.
- ADDED: Added a `--preview-check` option to show preview AND ask if the user wants to save extracted the color palette.
- ADDED: Added a `hex_to_rgb()` function to the **conversion_utils.py** file.
- ADDED: Added a **print_utils.py** file to handle printing previews to the screen and a **file_utils.py** file to handle different file saving options..
    - This is a potential point for contributors to add different printing and file saving options.
    - **NOTE**: The terminal needs to be able to display ANSI colors and ASCII characters to properly use the default preview option (this issue could be avoided by showing preview in separate GUI).
- CHANGED: Tested package against Python 3.6.15 and confirmed everything works as it should, added compatibility for Python 3.6 to **setup.py** file.
- CHANGED: `Extractor` class no longer organizes the extracted color palettes into color schemes, that will be done by the saving options in **file_utils.py**.
    - The `Extractor` class x will organize the color palettes into a dictionary of default format that looks like this: {light background, light foreground, dark background, dark foreground, light palette, normal palette, dark palette}
- CHANGED: Changed the light background brightness from 94% to 95%.
- CHANGED: Changed the light foreground saturation and brightness from (4%, 92%) to (3%, 95%).
- REMOVED: Removed file saving function from **image_utils.py** file.
    - This function was moved to the **file_utils.py** file.

<br>

## [1.3.2] - 2023-03-26
- FIXED: Fixed bug where `extractor.color_palette_dict` was not renamed to `extractor.color_schemes_dict` in the **\_\_main\_\_.py** file when changes were made in PyPalEx 1.3.1.

<br>

## [1.3.1] - 2023-03-23
- Added saturation preference options to PyPalEx for those that prefer more saturated colors.
- Added `--sat_pref` option to extract more saturated colors of all color palettes.
- Added `--sat_pref-light` option to extract more saturated colors of the light color palette.
- Added `--sat_pref-normal` option to extract more saturated colors of the normal color palette.
- Added `--sat_pref-dark` option to extract more saturated colors of the dark color palette.

<br>

## [1.3.0] - 2023-03-11

- Refactored codebase.
- Added multiprocessing to extraction process in **palex.extraction\_utils.py**.
    - Optimized color extraction for single image files with multiprocessing.
    - Removed multiprocessing for multiple image files (refer to `extract_color_palettes()` function of **palex.\_\_main\_\_.py** _v1.2.0_).
        - PyPalEx will continue to maintain the functionality to process multiple image files, but multiprocessing will only be applied to the color extraction process of individual images.
- Added `hsv_to_hex()` function to **palex.conversion\_utils.py**.
- Added enforcement of RGB color space in `process_image()` function of **palex.image\_utils.py**.
- Added constants for Pastel color range to **palex.constants.py**.
- Added CI/CD automation with GitHub Actions to automatically build and publish new release versions of PyPalEx to PyPI and TestPyPI.
- Changed color space that is used in the extraction process from HSL to HSV.
- Changed `-d --directory` option to `-p --path` option.
- Changed `-p --pastel` option to `--pastel`.
- Removed normal palette scheme.

## [1.2.0] - 2022-04-21

- Added `-p --pastel` option to convert all extracted color palettes to pastel.
- Added `--pastel-light` option to convert only the light color palette to pastel.
- Added `--pastel-normal` option to convert only the normal color palette to pastel.
- Added `--pastel-dark` option to convert only the dark color palette to pastel.
- Changed the order of the colors in JSON file.
    - Changed from [black, red, yellow, green, cyan, blue, magenta, white] to  
    [black, red, green, yellow, blue, magenta, cyan white].


## [1.1.0] - 2022-04-10

- Added `-v --version` option to print the PyPalEx version.
- Changed lighting adjustment threshold:
    - Some colors were still too bright or too dark to distinguish in the previous version.
    - Lightness threshold for bright colors decreased from 95% to 90%
        - Random range changed from [85.0, 95.0] to [80.0, 90.0].
    - Lightness threshold for dark colors increased from 5% to 15%
        - Random range changed from [5.0, 10.0] to [15.0, 25.0].
- Changed black color's normal saturation and lightness.
    - Saturation was decreased from 60% to 50%.
    - Lightness was increased from 10% to 15%.
- Changed Normal palette's foreground lightness.
    - Foreground lightness decreased from 88% to 85%.


## [1.0.6] - 2022-03-08

- **FIRST INITIAL RELEASE OF PyPalEx.**
- Contains the following options:
    - `-f --files`
    - `-d --directory`
    - `-o --output`
- Saves all three extracted color palettes (light/normal/dark) to a single file.
    - [filenam]-color_palette.json


[2.2.2]: https://github.com/AlTimofeyev/pypalex/compare/2.2.1...2.2.2
[2.2.1]: https://github.com/AlTimofeyev/pypalex/compare/2.2.0...2.2.1
[2.2.0]: https://github.com/AlTimofeyev/pypalex/compare/2.1.1...2.2.0
[2.1.1]: https://github.com/AlTimofeyev/pypalex/compare/2.1.0...2.1.1
[2.1.0]: https://github.com/AlTimofeyev/pypalex/compare/2.0.0...2.1.0
[2.0.0]: https://github.com/AlTimofeyev/pypalex/compare/1.3.5...2.0.0
[1.3.5]: https://github.com/AlTimofeyev/pypalex/compare/1.3.4...1.3.5
[1.3.4]: https://github.com/AlTimofeyev/pypalex/compare/1.3.3...1.3.4
[1.3.3]: https://github.com/AlTimofeyev/pypalex/compare/1.3.2...1.3.3
[1.3.2]: https://github.com/AlTimofeyev/pypalex/compare/1.3.1...1.3.2
[1.3.1]: https://github.com/AlTimofeyev/pypalex/compare/1.3.0...1.3.1
[1.3.0]: https://github.com/AlTimofeyev/pypalex/compare/1.2.0...1.3.0
[1.2.0]: https://github.com/AlTimofeyev/pypalex/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/AlTimofeyev/pypalex/compare/1.0.6...1.1.0
[1.0.6]: https://github.com/AlTimofeyev/pypalex/releases/tag/1.0.6