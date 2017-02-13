pvmpy : Partial Volume Morphology
=================================

`pvmpy` is a reference implementation of partial volume morphology in pure Python, as described by Joshua D. Warner at SPIE Medical Imaging 2017.

Briefly, partial volume morphology (PVM) is an extention to conventional binary morphology which allows values between 0 and 1, to represent partial volumes.  PVM enables more precise analysis and superior results to binary morphology.


Source
------

https://github.com/JDWarner/pvmpy


Documentation
-------------

The package exposes a limited number of functions which are all fully self-documented with NumPyDoc-compliant docstrings.  The morphology functions all function essentially equivalently to their conventional binary counterparts, but when input and/or structuring element carry partial volumes the results are superior.


Installation
------------

pvmpy is a pure-Python package which only depends on

  * NumPy >= 1.6
  * SciPy >= 0.9

and is available on PyPi! The lastest stable release can always be obtained
and installed simply by running

    $ pip install -U pvmpy

which will also work to upgrade existing installations to the latest release.


If you prefer to install from source or develop this package, you can fork and clone this repository then install pvmpy by running

	$ python setup.py install

or develop locally by running

	$ python setup.py develop

Finally, if you prefer, you can use pvmpy without installing at all by simply exporting the path containing this file to your PYTHONPATH variable.


License
-------

Please refer to LICENSE.txt in this directory.
