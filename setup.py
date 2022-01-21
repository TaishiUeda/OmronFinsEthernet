#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2022 Taishi Ueda <taishi.ueda@gmail.com.inc>
#
from setuptools import setup, find_packages

setup(
        name='omronfins',
        version='1.0.0',
        description='Utilities for OMRON FINS protocol',
        author='Taishi Ueda',
        author_email='taishi.ueda@gmail.com',
        packages=["omronfins"],
        package_dir={'': 'src'},
        )
