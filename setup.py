"""
palex - setup.py

NOTE:
This code from Dylan Araps PyWal on github: https://github.com/dylanaraps/pywal
has been borrowed and used as a template.
"""
import sys
import setuptools

try:
    import pypalex
except ImportError:
    print("error: pypalex requires Python 3.7 or greater.")
    sys.exit(1)

LONG_DESC = open('README.md').read()
VERSION = pypalex.__version__
DOWNLOAD = "https://github.com/AlTimofeyev/pypalex/archive/%s.tar.gz" % VERSION

setuptools.setup(
    name="pypalex",
    version=VERSION,
    author="Al Timofeyev",
    author_email="al.timofeyev@outlook.com",
    description="Python Palette Extractor: extracts color palettes from images into json files.",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    install_requires=['Pillow', 'numpy', 'filetype'],
    # keywords="python palex color-palette colorscheme extract-colorscheme extract-palette extractor",
    keywords=['python', 'pypalex', 'palex', 'color-palette', 'colorscheme', 'extract-colorscheme', 'extract-palette', 'extractor'],
    license="MIT",
    url="https://github.com/AlTimofeyev/pypalex",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["pypalex"],
    entry_points={"console_scripts": ["palex=pypalex.__main__:main"]},
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False)
