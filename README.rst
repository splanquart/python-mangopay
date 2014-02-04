===============
python-mangopay
===============

python-mangopay is a client library to work with `mangopay <http://www.mangopay.com/>`_
api V2.

Installation
------------

python-mangopay requires requests_, pycrypto_ and blinker_ to work.

.. _requests: http://docs.python-requests.org/en/latest/
.. _pycrypto: https://pypi.python.org/pypi/pycrypto
.. _blinker: https://pypi.python.org/pypi/blinker

To install it, simply ::

    pip install -e git+https://github.com/splanquart/python-mangopay.git#egg=python_mangopay


Inspiration
-----------

The data model of python-mangopay is highly inspired by `peewee <https://github.com/coleifer/peewee>`_.
In fact, python-mangopay is a port of python-leetchi.

Documentation
-------------

For documentation, usage, and examples, see:
https://python-mangopay.readthedocs.org/

In the wild
-----------

This library has been developed for the need of `PayPlug <https://www.payplug.fr>`_.
