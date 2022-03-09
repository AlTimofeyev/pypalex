## <div align="center">PyPalEx</div>
### <div align="center">Python Palette Extractor</div>

## Table of Contents
- [**Description**](#description)
    - [Wiki Homepage](#wiki-homepage)
    - [Palette Examples Archive](#wiki-palette-examples-archive)
    - [Note](#note)
- [**Installation**](#installation)
    - [Dependencies](#dependencies)
    - [Environment Variables](#environment-variables)
    - [Install](#install)
- [**User Guide**](#user-guide)
- [**Code Documentation**](#code-documentation)

<br>
<br>

## **DESCRIPTION**
PyPalEx is a tool for extracting color palettes from images and generating a JSON format file with light, normal, and dark color palettes. This tool is intended to be non-OS dependent, for use by the tech community for developing their own custom theme managers or by artists who want to extract color palettes for their art from images/pictures/wallpapers they adore.

PyPalEx picks out the most dominant light, normal, and dark color for each of the base colors [red, yellow, green, cyan, blue, magenta] in an image and constructs a color palette for each of these three variants. When a specific color is not present in an image, that color is borrowed from one of the colors that *is* present. (e.g. Colors red and cyan are missing from an image, so red and cyan are borrowed from the colors that are present in the image.)

### [**_WIKI HOMEPAGE_**](https://github.com/AlTimofeyev/pypalex/wiki)

### [**_WIKI PALETTE EXAMPLES ARCHIVE_**](https://github.com/AlTimofeyev/pypalex/wiki/Palette-Examples-Archive)

### **_NOTE_**
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
There are three argument options: `-f --Files`, `-d --Directory`, `-o --Output`. When using PyPalEx, the use of either `-f --Files` and/or `-d --Directory` is a **MUST**. Without either, or both of, these two options being specified, PyPalEx will not work.

### **_EXAMPLE USAGE_**
#### **`-f --Files` Option**
```sh
palex -f path/to/image/dir/image.jpeg
```
```sh
palex -f path/to/image/dir/image.jpeg path/to/image/dir/image2.PNG
```
The `-f --Files` option can be used with a singular image file or with multiple image files. When used without the `-d --Directory` option, the user must specify the full path to the image they want to use with PyPalEx.

<br>

#### **`-d --Directory` Option**
```sh
palex -d path/to/image/dir/
```
```sh
palex -d path/to/image/dir/ -f image.png
```
```sh
palex -f image1.png image2.jpg image3.jpeg -d path/to/image/dir/
```
The `-d --Directory` option can be used with a whole directory of images and files or it be used as a reference point for the `-f --Files` option. PyPalEx will skip over files that are not images in the directory specified, if only the directory option is supplied by the user. The order of the options also does not matter, you can specify `-f --Files` first and then `-d --Directory` and vice versa. When the `-f --Files` option is used with `-d --Directory`, the user does not have to specify the full path to the images, just the image names, the directory that was provided will be searched for the image names specified.

<br>

#### **`-o --Output` Option**
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
The `-o --Output` option can be used with both the `-f --Files` and `-d --Directory` options. The order of the options also does not matter. The sole purpose of the `-o --Output` option is to let the user override the default save directory. As mentioned earlier, PyPalEx has a default save directory, where it can save all the extracted palettes to, which is either the global shell variable `PYPALEX_CONFIG_DIR` __or__ wherever (`XDG_CONFIG_HOME/palex` or `$HOME/.config/palex`) points to in the system.

<br>

## [**CODE DOCUMENTATION**](https://github.com/AlTimofeyev/pypalex/blob/main/pypalex_code_documentation.pdf)
