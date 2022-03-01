"""
palex - setup.py

NOTE:
This code has been borrowed from Dylan Araps PyWal
on github: https://github.com/dylanaraps/pywal
"""
import sys
import setuptools
# NEEDS TO BE UPDATED LATER!!!!!
# UPDATE PYTHON VERSION, KEYWORDS, AND TESTS (test if needed).
try:
    import pypalex
except ImportError:
    print("error: pypalex requires Python 3.5 or greater.")
    sys.exit(1)

LONG_DESC = open('README.md').read()
VERSION = pypalex.__version__
DOWNLOAD = "https://github.com/AlTimofeyev/pypalex/archive/%s.tar.gz" % VERSION

setuptools.setup(
    name="pypalex",
    version=VERSION,
    author="Al Timofeyev",
    author_email="al.timofeyev@outlook.com",
    description="Extract color palettes from images into json files",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    # keywords="wal colorscheme terminal-emulators changing-colorschemes",
    license="MIT",
    url="https://github.com/AlTimofeyev/pypalex",
    download_url=DOWNLOAD,
    classifiers=[
        "License :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["pypalex"],
    entry_points={"console_scripts": ["palex=pypalex.__main__:main"]},
    python_requires=">=3.5",
    # test_suite="tests",
    include_package_data=True,
    zip_safe=False)