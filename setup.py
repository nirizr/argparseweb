from os.path import exists
from distutils.core import setup
import argparseweb

setup(
  name = 'argparseweb',
  packages = ['argparseweb'],
  version = argparseweb.__version__,
  description = 'Automatic exposure of argparse-compatible scripts as a web interface',
  long_description=(open('README.md').read() if exists('README.md') else ''),
  author = 'Nir Izraeli',
  author_email = 'nirizr@gmail.com',
  url = 'https://github.com/nirizr/argparseweb',
  download_url = 'https://github.com/nirizr/argparseweb/tarball/{}'.format(argparseweb.__version__),
  keywords = ['webui', 'web', 'user', 'interface', 'ui', 'argparse', 'webpy', 'web.py'],
  classifiers = [],
)
