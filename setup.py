#! /usr/bin/env python

descr = """pvmpy: Partial Volume Morphology (PVM) for Python.

This package provides partial volume-aware morphology algorithms.
"""

DISTNAME            = 'pvmpy'
DESCRIPTION         = 'Partial Volume Morphology'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'Joshua Warner'
MAINTAINER_EMAIL    = 'joshua.dale.warner@gmail.com'
LICENSE             = 'Modified BSD'
URL                 = 'https://github.com/JDWarner/pvmpy'
DOWNLOAD_URL        = 'https://github.com/JDWarner/pvmpy'

import os
import sys

import setuptools
from distutils.command.build_py import build_py

if sys.version_info[0] < 3:
    import __builtin__ as builtins
else:
    import builtins

# This is a bit (!) hackish: we are setting a global variable so that the main
# pvmpy __init__ can detect if it is being loaded by the setup routine, to
# avoid attempting to load components that aren't built yet:
# the numpy distutils extensions that are used by pvmpy to recursively
# build the compiled extensions in sub-packages is based on the Python import
# machinery.
builtins.__PVMPY_SETUP__ = True


with open('./pvmpy/__init__.py') as fid:
    for line in fid:
        if line.startswith('__version__'):
            VERSION = line.strip().split()[-1][1:-1]
            break

with open('DEPENDS.txt') as fid:
    INSTALL_REQUIRES = []
    for line in fid.readlines():
        if line == '' or line[0] == '#' or line[0].isspace():
            continue
        INSTALL_REQUIRES.append(line.strip())

# requirements for those browsing PyPI
REQUIRES = [r.replace('>=', ' (>= ') + ')' for r in INSTALL_REQUIRES]
REQUIRES = [r.replace('==', ' (== ') for r in REQUIRES]


def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    config.set_options(
        ignore_setup_xxx_py=True,
        assume_default_configuration=True,
        delegate_options_to_subpackages=True,
        quiet=True)

    config.add_subpackage('pvmpy')

    return config


if __name__ == "__main__":
    try:
        from numpy.distutils.core import setup
        extra = {'configuration': configuration}
        # Do not try and upgrade larger dependencies
        for lib in ['numpy', 'scipy', 'matplotlib']:
            try:
                __import__(lib)
                INSTALL_REQUIRES = [i for i in INSTALL_REQUIRES
                                    if lib not in i]
            except ImportError:
                pass
    except ImportError:
        if len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or
                                   sys.argv[1] in ('--help-commands',
                                                   '--version',
                                                   'clean')):
            # For these actions, NumPy is not required.
            #
            # They are required to succeed without Numpy for example when
            # pip is used to install but Numpy is not yet present.
            from setuptools import setup
            extra = {}
        else:
            print('To install pvmpy from source, you will need numpy.\n' +
                  'Install numpy with pip:\n' +
                  'pip install numpy\n'
                  'Or use your operating system package manager.')
            sys.exit(1)

    setup(
        name=DISTNAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        license=LICENSE,
        url=URL,
        download_url=DOWNLOAD_URL,
        version=VERSION,
        package_data={
            # Include saved test image
            '': ['*.npy', '*.md', '*.txt'],
        },

        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS'],

        install_requires=INSTALL_REQUIRES,
        requires=REQUIRES,
        packages=setuptools.find_packages(exclude=['docs']),
        include_package_data=True,
        zip_safe=False,

        cmdclass={'build_py': build_py},
        **extra
    )
