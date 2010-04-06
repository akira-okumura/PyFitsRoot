"""
Setup script for PyFitsRoot
$Id: setup.py,v 1.9 2010/04/06 01:36:10 oxon Exp $
"""

from distutils.core import setup

setup(name="PyFitsRoot",
      version="1.1.7",
      description="Package for FITS interface in PyROOT",
      author="Akira Okumura",
      author_email="oxon@juno.phys.s.u-tokyo.ac.jp",
      packages=["fitsroot"]
      )
