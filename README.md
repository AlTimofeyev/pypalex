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
PyPalEx is a tool for extracting color palettes from images and generating a JSON format file with light and dark color themes. This tool is intended to be OS independent, for use by the tech community for developing their own custom theme managers or by artists who want to extract color palettes for their art from images, pictures or wallpapers they adore.
</p>

<br>
<br>

<h2 align=center>TABLE OF CONTENTS</h2>

- [**PyPalEx Archives**](#pypalex-archives)
  - [Wiki Homepage](#wiki-homepage)
  - [Palette Examples Archive](#wiki-palette-examples-archive)
  - [Code Documentation](#code-documentation)
- [**Dependencies**](#dependencies)
  - [Environment Variables](#environment-variables)
- [**Installation**](#installation)
  - [PIP Install](#pip-install)
  - [Manual/Git Install](#manualgit-install)
- [**User Guide**](#user-guide)
  - [Disclosure](#disclosure)
  - [Options List](#options-list)
  - [Notes](#notes)
  - [Example Usage](#example-usage)
- [**Feedback**](#feedback)

<br>
<br>

<h2 align=center id="pypalex-archives">PYPALEX ARCHIVES</h2>

<h3 align=center>
  [<a href="https://github.com/AlTimofeyev/pypalex/wiki">Wiki Homepage</a>]
  [<a href="https://github.com/AlTimofeyev/pypalex/wiki/Archive-of-Palette-Examples">Palette Examples Archive</a>]
  [<a href="https://github.com/AlTimofeyev/pypalex/blob/main/pypalex_code_documentation.pdf">Codebase Documentation</a>]
</h3>

<br>

<h2 align=center id="dependencies">DEPENDENCIES</h2>

Aside from Python, the rest are Python packages that are installable with pip.
- `Python 3.7+`
- `Pillow (PIL) 9.0+`
    - For performing operations on images.
- `NumPy 1.21+`
    - To manage large amounts of image data.
- `filetype 1.0+`
    - To confirm filetypes are images file types.

### ENVIRONMENT VARIABLES
There are two optional environement variables that can be set by the user:
- `PYPALEX_CACHE_DIR`
- `PYPALEX_CONFIG_DIR`

By default, PyPalEx will try to store extracted color palettes into one of three locations:
- `PYPALEX_CONFIG_DIR` 
- `XDG_CONFIG_HOME/palex` 
- `$HOME/.config/palex`

By default, PyPalEx will try to save extracted color palettes wherever `PYPALEX_CONFIG_DIR` points to in the user's system. If the user does not set the `PYPALEX_CONFIG_DIR` environment variable, then PyPalEx will default to saving extracted color palettes wherever `XDG_CONFIG_HOME/palex` points to in the user's system. And if the `XDG_CONFIG_HOME` environment variable is not set, then PyPalEx will default to saving extracted color palettes into `$HOME/.config/palex`.  
_This default output location is, of course, overriden if PyPalEx is used with the `-o --output` option._

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
- `--pastel`
  - Converts all color palettes into pastel.
- `--pastel-light`
  - Converts light color palette into pastel.
- `--pastel-normal`
  - Converts normal color palette into pastel.
- `--pastel-dark`
  - Converts dark color palette into pastel.
- `--sat_pref`
  - Gives preference to more saturated colors of all color palettes.
- `--sat_pref-light`
  - Gives preference to more saturated colors of the light color palette.
- `--sat_pref-normal`
  - Gives preference to more saturated colors of the normal color palette.
- `--sat_pref-dark`
  - Gives preference to more saturated colors of the dark color palette.
- `-v --version`
  -  Prints the PyPalEx version.

### NOTES
- When using PyPalEx, the use of either `-f --files` and/or `-p --path` is a **MUST**. Without either, or both of, these two options being specified, PyPalEx will not work.
- PyPalEx will skip over any files that are not images.
- Please note that all the `--pastel` and `--sat_pref` options only affect the 6 base colors (red, green, yellow, blue, magenta, cyan) and do **NOT** affect the background, foreground, black, and white colors.
- Please note that the user can individually select which palette to convert to pastel (do not mistake palette for "color scheme/color theme"). For more details, please refer to the PyPalEx wiki homepage to identify which "color scheme/color theme" contains the palette you wish to convert to pastel.

### EXAMPLE USAGE
#### **`-f --files` Option**
```sh
palex -f path/to/image/dir/image.jpeg
```
```sh
palex -f path/to/image/dir/image.jpeg path/to/image/dir/image2.PNG
```
The `-f --files` option can be used with a singular image file or with multiple image files. The user must specify the absolute file path to the image they want to use with PyPalEx. However, if the user is already within the directory where the images are located, then a relative file path is also acceptable.
```sh
~ > cd path/to
~/path/to >
~/path/to > palex -f image/dir/image.jpeg image/dir/image2.PNG
```
```sh
~ > cd path/to
~/path/to >
~/path/to > palex -f image/dir/image.jpeg
```
```sh
~/path/to > cd image/dir
~/path/to/image/dir >
~/path/to/image/dir > palex -f image.JPEG image2.png
```
The above examples are meant to show how a user can navigate to a direcotry with images, or at least relatively close to a directory with images, and then use PyPalEx with the `-f --files` option and relative file path(s).

<br>

#### **`-p --path` Option**
```sh
palex -p path/to/image/dir/
```
```sh
palex -p path/to/ -f image/dir/image.png
```
```sh
palex -p path/to/image/dir/ -f image.png
```
```sh
palex -f image1.png image2.jpg image3.jpeg -p path/to/image/dir/
```
The `-p --path` option can be used with a whole directory of images and files or it can be used as a reference point for the `-f --files` option. When the `-f --files` option is used with `-p --path`, the user does not have to specify the absolute path to the images, just the relative image names/filepath(s). The directory that was provided with `-p --path` will be searched for the image names/filepath(s) specified.

<br>

#### **`-o --output` Option**
```sh
palex -f path/to/image/dir/image.jpeg -o path/to/output/dir/ 
```
```sh
palex -o path/to/output/dir/ -p path/to/image/dir/
```
```sh
palex -p path/to/image/dir/ -f image.png -o path/to/output/dir/
```
```sh
palex -f image1.png image2.jpg image3.jpeg -o path/to/output/dir/ -p path/to/image/dir/
```
The `-o --output` option can be used with both the `-f --files` and `-p --path` options. The sole purpose of the `-o --output` option is to let the user override the default output directory. Please refer to [Environment Variables](#environment-variables) for details about the default output directory.

<br>

#### **`--pastel` Option**
```sh
palex --pastel -f path/to/image/dir/image.jpeg -o path/to/output/dir/
```
Converts all the extracted color palettes into pastel.

<br>

#### **`--pastel-light` Option**
```sh
palex --pastel-light -f path/to/image/dir/image.jpeg -o path/to/output/dir/
```
Converts light color palette into pastel.

<br>

#### **`--pastel-normal` Option**
```sh
palex --pastel-normal -f path/to/image/dir/image.jpeg -o path/to/output/dir/
```
Converts normal color palette into pastel.

<br>

#### **`--pastel-dark` Option**
```sh
palex --pastel-dark -f path/to/image/dir/image.jpeg -o path/to/output/dir/
```
Converts dark color palette into pastel.

<br>

#### **`--sat_pref` Option**
```sh
palex --sat_pref -f path/to/image/dir/image.jpeg -o path/to/output/dir/
```
Gives preference to more saturated colors of all color palettes during the extraction process.

<br>

#### **`--sat_pref-light` Option**
```sh
palex --sat_pref-light -f path/to/image/dir/image.jpeg -o path/to/output/dir/
```
Gives preference to more saturated colors of the light color palette during the extraction process.

<br>

#### **`--sat_pref-normal` Option**
```sh
palex --sat_pref-normal -f path/to/image/dir/image.jpeg -o path/to/output/dir/
```
Gives preference to more saturated colors of the normal color palette during the extraction process.

<br>

#### **`--sat_pref-dark` Option**
```sh
palex --sat_pref-dark -f path/to/image/dir/image.jpeg -o path/to/output/dir/
```
Gives preference to more saturated colors of the dark color palette during the extraction process.

<br>

#### **`-v --version` Option**
```sh
palex -v
```
```sh
palex --version
```
The `-v --version` option is used to print the PyPalEx version number.


<h2 align=center id="feedback">FEEDBACK</h2>

<p align=justify>
Any and all feedback is greatly appreciated and welcomed. On the PyPalEx GitHub repository, there is a <b><a href="https://github.com/AlTimofeyev/pypalex/discussions">Discussion</a></b> post that is available for each Release version of PyPalEx and open to everyone for any comments or feedback on the version of PyPalEx you are using.
</p>

[//]: # (Include Contributions Section Later)
