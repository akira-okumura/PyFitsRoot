"""
Setup script for PyFitsRoot
$Id: setup.py,v 1.2 2009/05/28 16:18:04 oxon Exp $
"""

from distutils.core import setup

setup(name="PyFitsRoot",
      version="1.1.0",
      description="Package for FITS interface in PyROOT",
      author="Akira Okumura",
      author_email="oxon@ceres.phys.s.u-tokyo.ac.jp",
      packages=["fitsroot"]
      )
