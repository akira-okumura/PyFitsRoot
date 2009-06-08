"""
Setup script for PyFitsRoot
$Id: setup.py,v 1.4 2009/06/08 15:39:18 oxon Exp $
"""

from distutils.core import setup

setup(name="PyFitsRoot",
      version="1.1.2",
      description="Package for FITS interface in PyROOT",
      author="Akira Okumura",
      author_email="oxon@ceres.phys.s.u-tokyo.ac.jp",
      packages=["fitsroot"]
      )
