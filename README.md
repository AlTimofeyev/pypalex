## <div align="center">PyPalEx</div>
### <div align="center">Python Palette Extractor</div>

## Table of Contents
- [**Description**](#description)
    - [Wiki Homepage](#wiki-homepage)
    - [Palette Examples Archive](#wiki-palette-examples-archive)
    - [Note](#note-1)
- [**Installation**](#installation)
    - [Dependencies](#dependencies)
    - [Environment Variables](#environment-variables)
    - [Install](#install)
- [**User Guide**](#user-guide)
    - [Options List](#options-list)
    - [Note](#note-2)
    - [Example Usage](#example-usage)
- [**Code Documentation**](#code-documentation)

<br>
<br>

## **DESCRIPTION**
PyPalEx is a tool for extracting color palettes from images and generating a JSON format file with light, normal, and dark color palettes. This tool is intended to be non-OS dependent, for use by the tech community for developing their own custom theme managers or by artists who want to extract color palettes for their art from images/pictures/wallpapers they adore.

PyPalEx picks out the most dominant light, normal, and dark color for each of the base colors [red, yellow, green, cyan, blue, magenta] in an image and constructs a color palette for each of these three variants. When a specific color is not present in an image, that color is borrowed from one of the colors that *is* present. (e.g. Colors red and cyan are missing from an image, so red and cyan are borrowed from the colors that are present in the image.)

### [**_WIKI HOMEPAGE_**](https://github.com/AlTimofeyev/pypalex/wiki/Welcome-to-the-PyPalEx-Wiki!)

### [**_WIKI PALETTE EXAMPLES ARCHIVE_**](https://github.com/AlTimofeyev/pypalex/wiki/Archive-of-Palette-Examples)

### **_NOTE 1_**
Future updates may include a `-p --pastel` option for generating pastel palettes from the extracted colors as well as a `-g --generate` option for generating missing colors from their respective hue range instead of borrowing missing colors from pre-existing colors in the image.


## **INSTALLATION**
### **_DEPENDENCIES_**
- `Python 3.7+`
- `Pillow (PIL) 9.0+`
    - For performing operations on images.
- `NumPy 1.21+`
    - To manage large amounts of image data.
- `filetype 1.0+`
    - To confirm filetypes are images file types.

Aside from `Python`, the rest are python packages/libraries that are installable with pip.

### **_ENVIRONMENT VARIABLES_**
Two shell environement variables `PYPALEX_CACHE_DIR` and `PYPALEX_CONFIG_DIR` can be set in terminal. By default, PyPalEx will either store extracted palettes into `PYPALEX_CONFIG_DIR` __or__ wherever `XDG_CONFIG_HOME/palex` points to in the system. If `PYPALEX_CONFIG_DIR` and `XDG_CONFIG_HOME` are not defined in the shell environment, then the default location becomes `$HOME/.config/palex`.  
_This default storing location is, of course, overriden if PyPalEx is used with the `-o --Output` option._

### **_INSTALL_**
### _PIP INSTALL_
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

### _MANUAL/GIT INSTALL_
```sh
git clone https://github.com/AlTimofeyev/pypalex
cd pypalex
pip3 install --user .

# Add local 'pip' to PATH:
# (In your .bashrc, .zshrc etc)
export PATH="${PATH}:${HOME}/.local/bin/"
```

## **USER GUIDE**
Instructions on how to use PyPalEx.  

### **_OPTIONS LIST_**
- `-f --files`
  - Specify the file path(s).
  - If used with `-d --directory` option, you only need to list the filename(s).
- `-d --directory`
  - Specify the directory from where to use images.
- `-o --output`
  - Specify the output directory where to store the JSON color palette.
- `-v --version`
  -  Prints the PyPalEx version.

### **_NOTE 2_**
When using PyPalEx, the use of either `-f --files` and/or `-d --directory` is a **MUST**. Without either, or both of, these two options being specified, PyPalEx will not work.

### **_EXAMPLE USAGE_**
#### **`-f --files` Option**
```sh
palex -f path/to/image/dir/image.jpeg
```
```sh
palex -f path/to/image/dir/image.jpeg path/to/image/dir/image2.PNG
```
The `-f --files` option can be used with a singular image file or with multiple image files. When used without the `-d --directory` option, the user must specify the full path to the image they want to use with PyPalEx.

<br>

#### **`-d --directory` Option**
```sh
palex -d path/to/image/dir/
```
```sh
palex -d path/to/image/dir/ -f image.png
```
```sh
palex -f image1.png image2.jpg image3.jpeg -d path/to/image/dir/
```
The `-d --directory` option can be used with a whole directory of images and files or it be used as a reference point for the `-f --files` option. PyPalEx will skip over files that are not images in the directory specified, if only the directory option is supplied by the user. The order of the options also does not matter, you can specify `-f --files` first and then `-d --directory` and vice versa. When the `-f --files` option is used with `-d --directory`, the user does not have to specify the full path to the images, just the image names, the directory that was provided will be searched for the image names specified.

<br>

#### **`-o --output` Option**
```sh
palex -f path/to/image/dir/image.jpeg -o path/to/output/dir/ 
```
```sh
palex -o path/to/output/dir/ -d path/to/image/dir/
```
```sh
palex -d path/to/image/dir/ -f image.png -o path/to/output/dir/
```
```sh
palex -f image1.png image2.jpg image3.jpeg -o path/to/output/dir/ -d path/to/image/dir/
```
The `-o --output` option can be used with both the `-f --files` and `-d --directory` options. The order of the options also does not matter. The sole purpose of the `-o --output` option is to let the user override the default save directory. As mentioned earlier, PyPalEx has a default save directory, where it can save all the extracted palettes to, which is either the global shell variable `PYPALEX_CONFIG_DIR` __or__ wherever (`XDG_CONFIG_HOME/palex` or `$HOME/.config/palex`) points to in the system.

<br>

#### **`-v --version` Option**
```sh
palex -v
```
```sh
palex --version
```
The `-v --version` option is used to print the PyPalEx version number.  
Please note the following:

```sh
palex --version -f path/to/image/dir/image.jpeg
```
This will also **ONLY** print the version number. If other options are used with PyPalEx when `-v --version` is used, PyPalEx will only print the version number and stop execution.

<br>

## [**CODE DOCUMENTATION**](https://github.com/AlTimofeyev/pypalex/blob/main/pypalex_code_documentation.pdf)
