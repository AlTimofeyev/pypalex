##  @file   setup.py
#   @brief  palex - setup.py
#
#   @note   This code from Dylan Araps PyWal on github: https://github.com/dylanaraps/pywal
#           has been borrowed and used as a template.
#
#   @section authors Author(s)
#   - Created by Al Timofeyev on February 20, 2022.
#   - Modified by Al Timofeyev on April 7, 2023.
#   - Modified by Al Timofeyev on June 10, 2024.
#   - Modified by Al Timofeyev on July 8, 2024.


import sys
import setuptools

try:
    import pypalex
except ImportError:
    print("error: pypalex requires Python 3.6 or greater.")
    sys.exit(1)

LONG_DESC = open('README.md').read()
VERSION = pypalex.__version__
DOWNLOAD = "https://github.com/AlTimofeyev/pypalex/archive/%s.tar.gz" % VERSION
REQUIREMENTS = [
    'pillow >= 9.0',
    'numpy >= 1.21',
    'filetype >= 1.0'
    'PyYAML >= 5.4.1'
]

setuptools.setup(
    name="pypalex",
    version=VERSION,
    author="Al Timofeyev",
    author_email="al.timofeyev@outlook.com",
    description="Python Palette Extractor: extracts color palettes from images into json / yaml files.",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    install_requires=REQUIREMENTS,
    keywords=['python', 'pypalex', 'palex', 'color-palette', 'colorscheme', 'extract-colorscheme', 'extract-palette', 'extractor'],
    license="MIT",
    url="https://github.com/AlTimofeyev/pypalex",
    download_url=DOWNLOAD,
    project_urls={
        'Changelog': "https://github.com/AlTimofeyev/pypalex/blob/main/CHANGELOG.md",
        'Documentation': "https://github.com/AlTimofeyev/pypalex/blob/main/pypalex_code_documentation.pdf",
        'Wiki': "https://github.com/AlTimofeyev/pypalex/wiki",
        'Showcase': "https://github.com/AlTimofeyev/pypalex/wiki/Archive-of-Palette-Examples",
    },
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["pypalex"],
    entry_points={"console_scripts": ["palex=pypalex.__main__:main"]},
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False)
