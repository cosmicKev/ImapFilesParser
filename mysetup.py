from distutils.core import setup
import py2exe

setup(name="name",
      # console based executables
      console=[main.py],

      # windows subsystem executables (no console)
      windows=[],

      # py2exe options
      zipfile=None,
      )
