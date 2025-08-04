<h1 align=center>PyPalEx</h1>

<h3 align=center>Python Palette Extractor</h3>

<p align=center>
  <a href="https://github.com/AlTimofeyev/pypalex/releases"><img src="https://img.shields.io/github/v/release/AlTimofeyev/pypalex.svg?colorA=151515&colorB=8C977D&style=for-the-badge"></a>
  <a href="https://github.com/AlTimofeyev/pypalex/stargazers"><img src="https://img.shields.io/github/stars/AlTimofeyev/pypalex?colorA=151515&colorB=D9BC8C&style=for-the-badge"></a>
  <a href="https://github.com/AlTimofeyev/pypalex/network/members"><img src="https://img.shields.io/github/forks/AlTimofeyev/pypalex?colorA=151515&colorB=8DA3B9&style=for-the-badge"></a>
  <a href="https://github.com/AlTimofeyev/pypalex/blob/main/LICENSE"><img src="https://img.shields.io/static/v1?label=license&message=MIT&color=B66467&labelColor=151515&style=for-the-badge"></a>
</p>

<img src="https://github.com/AlTimofeyev/pypalex/blob/main/Assets/README_EXAMPLE-tsujin_bohboh-Holiday.PNG" alt="Package Example with Background Image by tsujin_bohboh on Twitter" title="Package Example with Background Image by tsujin_bohboh on Twitter" align="center">

<p align="justify">
PyPalEx is a tool for extracting color palettes from images and storing them in JSON / YAML formated files. This tool is intended to be OS independent, for use by the tech community for developing their own custom theme managers or by artists who want to extract color palettes for their art from images, pictures or wallpapers they adore.
</p>

<br>
<br>

<h2 align=center>TABLE OF CONTENTS</h2>

- [**PyPalEx Archives**](#pypalex-archives)
  - [Wiki Homepage](#wiki-homepage)
  - [Palette Examples Archive](#wiki-palette-examples-archive)
  - [Code Documentation](#code-documentation)
  - [Configuration File](#configuration-file)
- [**Dependencies**](#dependencies)
  - [Environment Variables](#environment-variables)
- [**Installation**](#installation)
  - [PIP Install](#pip-install)
  - [Manual/Git Install](#manualgit-install)
- [**User Guide**](#user-guide)
  - [Disclosure](#disclosure)
  - [Options List](#options-list)
  - [Notes](#notes)
  - [Option Usage Examples](#option-usage-examples)
  - [Shell Usage](#shell-usage)
- [**Feedback**](#feedback)

<br>
<br>

<h2 align=center id="pypalex-archives">PYPALEX ARCHIVES</h2>

<h3 align=center>
  [<a href="https://github.com/AlTimofeyev/pypalex/wiki" id="wiki-homepage">Wiki Homepage</a>]
  [<a href="https://github.com/AlTimofeyev/pypalex/wiki/Archive-of-Palette-Examples" id="wiki-palette-examples-archive">Palette Examples Archive</a>]
  [<a href="https://github.com/AlTimofeyev/pypalex/blob/main/pypalex_code_documentation.pdf" id="code-documentation">Codebase Documentation</a>]
  [<a href="https://github.com/AlTimofeyev/pypalex/wiki/Configuration-File" id="configuration-file">Configuration File</a>]
</h3>

<br>

<h2 align=center id="dependencies">DEPENDENCIES</h2>

Aside from Python, the rest are Python packages that are installable with pip.
- `Python 3.6+`
- `Pillow (PIL) 9.0+`
    - For performing operations on images.
- `NumPy 1.21+`
    - To manage large amounts of image data.
- `filetype 1.0+`
    - To confirm filetypes are images file types.
- `PyYAML 5.4.1+`
    - To manage YAML file types.

### ENVIRONMENT VARIABLES
There are two optional environment variables that can be set by the user:
- `PYPALEX_CACHE_DIR`
- `PYPALEX_CONFIG_DIR`

By default, PyPalEx will try to store extracted color palettes into one of three locations:
- `PYPALEX_CONFIG_DIR` 
- `XDG_CONFIG_HOME/palex` 
- `$HOME/.config/palex`

By default, PyPalEx will first try to save extracted color palettes wherever `PYPALEX_CONFIG_DIR` points to in the user's system. If the user does not set the `PYPALEX_CONFIG_DIR` environment variable, then PyPalEx will default to saving extracted color palettes wherever `XDG_CONFIG_HOME/palex` points to in the user's system. And if the `XDG_CONFIG_HOME` environment variable is not set, then PyPalEx will default to saving extracted color palettes into `$HOME/.config/palex`.  
_This default output location is, of course, overriden if PyPalEx is used with the `-o --output` option._

<br>

<h2 align=center id="installation">INSTALLATION</h2>

### PIP INSTALL
#### **System-wide install (*`sudo`*)**
```sh
pip3 install pypalex
```

#### **User install (*No `sudo`*)**
```sh
pip3 install --user pypalex

# Add local 'pip' to PATH:
# (In your .bashrc, .zshrc etc)
export PATH="${PATH}:${HOME}/.local/bin/"
```

### MANUAL/GIT INSTALL
```sh
git clone https://github.com/AlTimofeyev/pypalex
cd pypalex
pip3 install --user .

# Add local 'pip' to PATH:
# (In your .bashrc, .zshrc etc)
export PATH="${PATH}:${HOME}/.local/bin/"
```

<br>

<h2 align=center id="user-guide">USER GUIDE</h2> 

### DISCLOSURE
- PyPalEx can only work on images that are in the RBG color space, so any images that you supply to PyPalEx that are not already in RGB will automatically be converted into RGB color space before the extraction process begins.
- PyPalEx takes about ~5 seconds on average to process an image and extract color palettes.
- When using PyPalEx on a directory of images, you can calculate the time it takes to process all the images by multiplying the number of images by 5 seconds.
  - Example: You have a directory of 20 images. So the time it will take to process all the images is  
  20 x 5 = ~100 seconds

<p align=justify>
Some images may take 2-3 seconds to be processed while other images may take 4-5 seconds to be processed. But the average wait time for an image to be processed and for color palettes to be extracted is about ~5 seconds.
</p>

### OPTIONS LIST
- `-f --files`
  - Specify the absolute file path(s).
  - If used with `-p --path` option, you only need to specify the relative file path(s).
- `-p --path`
  - Specify the path from where to use images.
  - Absolute path is preferred, but relative path can also be used.
- `-o --output`
  - Specify the output path where to store the JSON color palette.
- `--save-check`
  - Asks if the user wants to save the extracted color palettes.
- `--preview`
  - Shows a preview of the extracted color palettes before saving.
- `--preview-check`
  - Shows a preview of, and asks if the user wants to save, the extracted color palettes.
- `--pastel`
  - Converts all color types into pastel.
- `--pastel-light`
  - Converts light color type into pastel.
- `--pastel-normal`
  - Converts normal color type into pastel.
- `--pastel-dark`
  - Converts dark color type into pastel.
- `-r --raw-dump`
  - Saves the raw extracted colors without organizing them into color palettes.
- `-g --gen-config`
  - Generates a default configuration file.
- `-w --where`
  - Prints where the default output locations of the configuration file and extracted color palattes are located.
  - This option will also let you know if these locations exist or not, as they are optional.
- `-v --version`
  -  Prints the PyPalEx version.

### NOTES
- When using PyPalEx, the use of either `-f --files` and/or `-p --path` is a **MUST**. Without either, or both of, these two options being specified, PyPalEx will not work.
- PyPalEx will skip over any files that are not images.
- Please note that all the `--pastel` and `--sat_pref` options only affect the 6 base colors (red, green, yellow, blue, magenta, cyan) and do **NOT** affect the background, foreground, black, and white colors.
- Please note that the user can individually select which palette to convert to pastel (do not mistake palette for "color scheme/color theme"). For more details, please refer to the PyPalEx wiki homepage to identify which "color scheme/color theme" contains the palette you wish to convert to pastel.

### OPTION USAGE EXAMPLES
For usage examples of each of the options provided, please read the Wiki Homepage :  
[https://github.com/AlTimofeyev/pypalex/wiki#option-usage-examples](https://github.com/AlTimofeyev/pypalex/wiki#option-usage-examples)

### SHELL USAGE
Here's an example of how to use the Extractor class from a python environment running in a terminal / shell (CLI):

``` python
>>> from pypalex.Extractor import Extractor
>>> from pypalex.print_utils import print_palette_preview
>>> from pypalex.file_utils import save_palettes
>>>
>>> extractor = Extractor()
>>>
>>> extractor.load("$HOME/aboslute/path/to/image.jpg")
>>> extractor.run()
>>>
>>> # The colors are extracted in HSV format, and the generated palettes are also in HSV format.
>>> adaptive_palettes_HSV = extractor.generate_adaptive_palettes(light_palette_name="binga", dark_palette_name="bongo")
>>>
>>> # You can change the color format of the colors that are in the Extractor before generating palettes.
>>> extractor.set_color_format("hex")
>>> mood_palettes_HEX = extractor.generate_mood_palettes(light_palette_name="happy", dark_palette_name="gloomy")
>>>
>>> # Print the palettes before saving them, but don't forget to specify their color types.
>>> print_palette_preview(adaptive_palettes_HSV, "hsv")
>>> print_palette_preview(mood_palettes_HEX, "hex")
>>>
>>> # If you're happy with the palettes from the image, you can save them.
>>> save_palettes(adaptive_palettes_HSV, image_name="forest", output_path="$HOME/absolute/path/to/output/folder", export_file_format="json", export_color_format="hsv")
>>> save_palettes(mood_palettes_HEX, image_name="melody", output_path="$HOME/absolute/path/to/output/folder", export_file_format="yaml", export_color_format="hex")
>>>
>>> # OR you can load another image into the Extractor and repeat the process.
>>> extractor.load("$HOME/aboslute/path/to/another/image.jpg")
>>> extractor.run()
>>>
>>> # Please look through the code documentation file, or the codebase, to 
>>> # get a better understanding of how to use each funciton and class 
>>> # separately. You can also import the funcitons and classes in this 
>>> # package into your own projects.
```

<br>

<h2 align=center id="feedback">FEEDBACK</h2>

<p align=justify>
Any and all feedback is greatly appreciated and welcomed! On the PyPalEx GitHub repository, there is a <b><a href="https://github.com/AlTimofeyev/pypalex/discussions">Discussion</a></b> post that is available for each Release version of PyPalEx and open to everyone for any comments or feedback on the version of PyPalEx you are using.
</p>

[//]: # (Include Contributions Section Later)
