from distutils.core import setup

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setup(
  name = 'argparseweb',
  packages = ['argparseweb'],
  version = '0.1.1',
  description = 'Automatic exposure of argparse-compatible scripts as a web interface',
  author = 'Nir Izraeli',
  author_email = 'nirizr@gmail.com',
  url = 'https://github.com/nirizr/argparseweb',
  download_url = 'https://github.com/nirizr/argparseweb/tarball/0.1.1',
  keywords = ['webui', 'web', 'user', 'interface', 'ui', 'argparse', 'webpy', 'web.py'],
  install_requires = requirements,
  classifiers = [],
)
