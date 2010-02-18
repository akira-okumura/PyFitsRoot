"""
Setup script for PyFitsRoot
$Id: setup.py,v 1.7 2010/02/18 15:28:13 oxon Exp $
"""

from distutils.core import setup

setup(name="PyFitsRoot",
      version="1.1.5",
      description="Package for FITS interface in PyROOT",
      author="Akira Okumura",
      author_email="oxon@juno.phys.s.u-tokyo.ac.jp",
      packages=["fitsroot"]
      )
