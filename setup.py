import io
import os

try:
  from setuptools import setup
  # Opciones que solo entiende setuptools; distutils las rechazaria.
  extra = {
    'long_description_content_type': 'text/markdown',
    'python_requires': '>=2.7',
  }
except ImportError:
  # Python 2.7 sin setuptools: distutils es parte de la stdlib.
  from distutils.core import setup
  extra = {}

here = os.path.abspath(os.path.dirname(__file__))
try:
  with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
except IOError:
  # Un sdist mal armado podria no traer el README; no es motivo para romper install.
  long_description = 'String Random Generation'

setup(
  name = 'pyrandstring',
  packages = ['pyrandstring'], # this must be the same as the name above
  version = '0.1.0',
  description = 'String Random Generation',
  long_description = long_description,
  author = 'Alvaro De Leon',
  author_email = 'info@alvarodeleon.com',
  url = 'https://github.com/alvarodeleon/pyrandstring', # use the URL to the github repo
  download_url = 'https://github.com/alvarodeleon/pyrandstring/tarball/0.1.0',
  keywords = ['password', 'generator', 'random'],
  license = 'GPL-3.0',
  classifiers = [
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Topic :: Security :: Cryptography',
  ],
  **extra
)
