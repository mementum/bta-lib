#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import codecs  # To use a consistent encoding
import os.path
import setuptools

# Some settings
AUTHOR = 'Daniel Rodriguez'

PACKAGENAME = 'btalib'
PYPINAME = 'bta-lib'

GITHUB_BASE = 'https://github.com'
GITHUB_USER = 'mementum'
GITHUB_NAME = 'bta-lib'

LICENSE = 'MIT'

KEYWORDS = ['trading', 'development', 'backtesting', 'algotrading',
            'technical analysis']

REQUIREMENTS = ['pandas']
PYTHON_VERSION = '>=3.6'

DESCRIPTION = 'bta-lib technical analysis library'

README = 'README.rst'
VERSION_PY = 'version.py'


# Get the long description from the relevant file
cwd = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(cwd, README), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# GET the version ... execfile is only on Py2 ... use exec + compile + open
with open(os.path.join(PACKAGENAME, VERSION_PY)) as f:
    exec(compile(f.read(), VERSION_PY, 'exec'))

# Generate links
GITHUB_URL = '/'.join((GITHUB_BASE, GITHUB_USER, GITHUB_NAME))
GITHUB_DOWN_URL = '/'.join((GITHUB_URL, 'tarball', __version__))  # noqa: F821

# SETUP Proceedings
setuptools.setup(
    name=PYPINAME,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,  # noqa: F821

    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,

    # The project's main homepage.
    url=GITHUB_URL,
    download_url=GITHUB_DOWN_URL,

    # Author details
    author=AUTHOR,

    # Choose your license
    license=LICENSE,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',

        # Indicate which Topics are covered by the package
        'Topic :: Software Development',
        'Topic :: Office/Business :: Financial',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        # Operating Systems on which it runs
        'Operating System :: OS Independent',
    ],

    # specify minimum vresion
    python_requires=PYTHON_VERSION,

    # What does your project relate to?
    keywords=KEYWORDS,

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # packages=[PACKAGENAME],
    packages=setuptools.find_packages(),

    # List run-time dependencies here.
    # These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=['six'],
    install_requires=REQUIREMENTS,

    # List additional groups of dependencies here
    # (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    # extras_require={},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={'sample': ['package_data.dat'],},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={'console_scripts': ['sample=sample:main',],},

    # scripts=[],
)
