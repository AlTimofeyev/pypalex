## <div align="center">PyPalEx</div>
### <div align="center">Python Palette Extractor</div>

## Table of Contents
- **[Description](#description)**
    - [Note](#note)
- **[Installation](#installation)**
    - [Dependencies](#dependencies)
    - [Environment Variables](#environment-variables)
    - [Install](#install)
- **[Code Documentation](#code-documentation)**


## **DESCRIPTION**
PyPalEx is a tool for extracting color palettes from images and generating a JSON format file with light, normal, and dark color schemes/palettes. This tool is intended to be non-OS dependant, for use by the tech community for developing their own custom theme managers or by artists who want to extract color palettes for thier art from images/pictures/wallpapers they adore.

PyPalEx does **NOT** select only dominant colors from an image. Instead, it picks out the most prominant light, normal, and dark color for each of the base colors (red, yellow, green, cyan, blue, magenta) in an image and constructs a color palette for each of these three variants. When a specific color is not present in an image, that color is borrowed from one of the colors that *is* present. (e.g. Colors red and cyan are missing from an image, so red and cyan are borrowed from the colors that are present in the image.)

### **_NOTE_**
Future update may include a `-p --pastel` option for generating pastelle palettes as well as a `-g --generate` option for generating missing colors from their respective hue range instead of borrowing missing colors from pre-existing colors in the image.


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
Two shell environement variables `PYPALEX_CACHE_DIR` and `PYPALEX_CONFIG_DIR` can be set in terminal. PyPalEx, by default, will either store extracted palettes into `PYPALEX_CONFIG_DIR` __OR__ wherever (`XDG_CONFIG_HOME/palex` or `$HOME/.config/palex`) points to.  
_This default storing location is, of course, overriden if pypalex is used with the `-o --Output` option._

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


## **CODE DOCUMENTATION**
\[[Documentation](https://github.com/AlTimofeyev/pypalex/blob/main/pypalex_code_documentation.pdf)]
