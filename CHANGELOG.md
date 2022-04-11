# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<br>

## [1.1.0] - 2022-04-10

- Added `-v --version` to print the PyPalEx version.
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


[1.1.0]: https://github.com/AlTimofeyev/pypalex/compare/1.0.6...1.1.0
[1.0.6]: https://github.com/AlTimofeyev/pypalex/releases/tag/1.0.6