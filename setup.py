#!/usr/bin/python

from os.path import exists
from setuptools import setup

def get_requirements():
  return open('./requirements.txt').readlines()

def get_version():
  context = {}
  execfile('./argparseweb/version.py', context)
  return context['__version__']

setup(
  name = 'argparseweb',
  packages = ['argparseweb'],
  version = get_version(),
  description = 'Automatic exposure of argparse-compatible scripts as a web interface',
  long_description=(open('README.md').read() if exists('README.md') else ''),
  author = 'Nir Izraeli',
  author_email = 'nirizr@gmail.com',
  url = 'https://github.com/nirizr/argparseweb',
  keywords = ['webui', 'web', 'user', 'interface', 'ui', 'argparse', 'webpy', 'web.py'],
  install_requires = get_requirements(),
  classifiers = [],
)
