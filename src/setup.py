"""
Setup script for PyFitsRoot
$Id: setup.py,v 1.5 2009/11/02 09:58:50 oxon Exp $
"""

from distutils.core import setup

setup(name="PyFitsRoot",
      version="1.1.3",
      description="Package for FITS interface in PyROOT",
      author="Akira Okumura",
      author_email="oxon@juno.phys.s.u-tokyo.ac.jp",
      packages=["fitsroot"]
      )
