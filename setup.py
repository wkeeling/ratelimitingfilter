try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(name='ratelimitingfilter',
      version='0.3',
      description='A rate limiting filter for the Python logging system',
      long_description=long_description,
      url='https://github.com/wkeeling/ratelimitingfilter',
      download_url='https://github.com/wkeeling/ratelimitingfilter/archive/0.3.tar.gz',
      author='Will Keeling',
      author_email='will@zifferent.com',
      maintainer='Will Keeling',
      maintainer_email='will@zifferent.com',
      license='MIT',
      packages=['ratelimitingfilter'],
      keywords='logging filter SMTPHandler ratelimit throughput',
      tests_require=['mock==2.0'])
