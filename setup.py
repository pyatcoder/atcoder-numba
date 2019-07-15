"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='atcoder-numba',
    version='0.1.0',
    description='AtCoder Numba AOT Tools',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    # keywords='sample setuptools development',
    packages=['atcoder_numba'],
    python_requires='>=3.4, <4',
    install_requires=['numba'],  # Optional
    entry_points={
        'console_scripts': [
            'atcoder-numba=atcoder_numba.main:main',
        ],
    },
)
