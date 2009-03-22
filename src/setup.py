"""
Setup script for PyFitsRoot
$Id: setup.py,v 1.1 2009/03/22 10:25:43 oxon Exp $
"""

from distutils.core import setup

setup(name="PyFitsRoot",
      version="1.0.0",
      description="Package for FITS interface in PyROOT",
      author="Akira Okumura",
      author_email="oxon@ceres.phys.s.u-tokyo.ac.jp",
      packages=["fitsroot"]
      )
