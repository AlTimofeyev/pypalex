# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<br>

## [1.3.2] - 2023-03-26
- Changed `__main__.py`:
    - Fixed bug where `extractor.color_palette_dict` was not renamed to `extractor.color_schemes_dict` when changes were made in PyPalEx 1.3.1.

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


[1.3.2]: https://github.com/AlTimofeyev/pypalex/compare/1.3.1...1.3.2
[1.3.1]: https://github.com/AlTimofeyev/pypalex/compare/1.3.0...1.3.1
[1.3.0]: https://github.com/AlTimofeyev/pypalex/compare/1.2.0...1.3.0
[1.2.0]: https://github.com/AlTimofeyev/pypalex/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/AlTimofeyev/pypalex/compare/1.0.6...1.1.0
[1.0.6]: https://github.com/AlTimofeyev/pypalex/releases/tag/1.0.6