#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X, BSD

.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

License : GPL(v3)

**python-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**python-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.

Build process :
- ask user what to do (zmq way in pip)
- or parametrizes it
    --dev : use local sources and cythonize way (for python-openzwave devs, ...)
    --embed : use local sources and cpp file (for third parties packagers, ...)
    --git : download openzwave from git (for geeks)
    --shared : use pkgconfig and cython (for debian devs and common users)
    --pybind : use pybind alternative (not tested)
    --auto (default) : try static, shared and cython, fails if it can't
"""
import os
import sys

print('bdist_wheel' in sys.argv)
if 'bdist_wheel' in sys.argv:
    bdist_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'build',
        'bdist_wheel'
    )

    os.environ['PYTHONPATH'] = bdist_dir
else:
    bdist_dir = ''

from setuptools import setup, find_packages
from distutils.extension import Extension
from pyozw_common import build_clib
from pyozw_version import pyozw_version
from pyozw_setup import LOCAL_OPENZWAVE, SETUP_DIR
from pyozw_setup import current_template, parse_template, get_dirs, data_files_config, install_requires, build_requires
from pyozw_setup import Template, DevTemplate, GitTemplate, EmbedTemplate, SharedTemplate
from pyozw_setup import bdist_egg, bdist_wheel, build_openzwave, build, clean, develop, install


# print(current_template)
# print(current_template.ctx)
# print(install_requires())

options = current_template.options
options.update(dict(bdist_wheel=dict(bdist_dir=bdist_dir)))

setup(
    name='python_openzwave',
    author='Sébastien GALLET aka bibi2100',
    author_email='bibi21000@gmail.com',
    version=pyozw_version,
    setup_requires=install_requires(),
    zip_safe=False,
    url='https://github.com/OpenZWave/python-openzwave',
    ext_modules=[Extension(**current_template.ctx)],
    options=options,
    libraries=current_template.library,
    install_requires=[
        'pyserial',
        'PyDispatcher>=2.0.5;python_version>="3.0"',
        'louie;python_version<"3.0"',
        'six'
    ],
    cmdclass=dict(
        build_ext=current_template.build_ext,
        build_clib=build_clib,
        bdist_egg=bdist_egg,
        bdist_wheel=bdist_wheel,
        build=build,
        build_openzwave=build_openzwave,
        clean=clean,
        develop=develop,
        install=install,
    ),
    packages=(
        find_packages('src-lib') +
        find_packages('src-api') +
        find_packages('src-manager') +
        find_packages('src-python_openzwave')
    ),
    entry_points=dict(
        console_scripts=[
            'pyozw_check=python_openzwave.scripts.pyozw_check:main',
            'pyozw_shell=python_openzwave.scripts.pyozw_shell:main'
        ]
    ),
    package_dir=dict(
        openzwave='src-api/openzwave',
        python_openzwave='src-python_openzwave/python_openzwave',
        pyozwman='src-manager/pyozwman',
        libopenzwave='src-lib'
    ),
    description=(
        'python_openzwave is a python wrapper for the openzwave c++ library.'
    ),
    long_description=(
        'A full API to map the ZWave network in Python objects. '
        'Look at examples at : https://github.com/OpenZWave/python-openzwave'
    ),
    download_url=(
        'https://raw.githubusercontent.com/OpenZWave/python-openzwave/'
        'master/archives/python_openzwave-{0}.zip'.format(pyozw_version)
    ),
    keywords=['openzwave', 'zwave'],
    classifiers=[
        "Topic :: Home Automation",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD",
        "Programming Language :: C++",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        (
            "License :: OSI Approved :: "
            "GNU General Public License v3 or later (GPLv3+)"
        ),
    ],
)
