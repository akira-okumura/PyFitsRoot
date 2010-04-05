"""
Setup script for PyFitsRoot
$Id: setup.py,v 1.8 2010/04/05 05:48:59 oxon Exp $
"""

from distutils.core import setup

setup(name="PyFitsRoot",
      version="1.1.6",
      description="Package for FITS interface in PyROOT",
      author="Akira Okumura",
      author_email="oxon@juno.phys.s.u-tokyo.ac.jp",
      packages=["fitsroot"]
      )
