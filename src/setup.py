"""
Setup script for PyFitsRoot
$Id: setup.py,v 1.6 2009/12/19 07:12:22 oxon Exp $
"""

from distutils.core import setup

setup(name="PyFitsRoot",
      version="1.1.4",
      description="Package for FITS interface in PyROOT",
      author="Akira Okumura",
      author_email="oxon@juno.phys.s.u-tokyo.ac.jp",
      packages=["fitsroot"]
      )
