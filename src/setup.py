"""
Setup script for PyFitsRoot
$Id: setup.py,v 1.3 2009/06/05 14:23:51 oxon Exp $
"""

from distutils.core import setup

setup(name="PyFitsRoot",
      version="1.1.1",
      description="Package for FITS interface in PyROOT",
      author="Akira Okumura",
      author_email="oxon@ceres.phys.s.u-tokyo.ac.jp",
      packages=["fitsroot"]
      )
