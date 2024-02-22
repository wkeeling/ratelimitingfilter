from setuptools import setup
from sys import version_info

if version_info.major < 3 or \
  (version_info.major == 3 and version_info.minor < 4):
    tests_require=['mock']
else:
    tests_require=[]

setup(
    author='Will Keeling',
    author_email='will@zifferent.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description='A rate limiting filter for the Python logging system',
    license='MIT',
    long_description=open('README.rst').read(),
    keywords='ratelimitingfilter',
    name='ratelimitingfilter',
    packages=['ratelimitingfilter'],
    test_suite='tests',
    tests_require=tests_require,
    url='https://github.com/wkeeling/ratelimitingfilter',
    version='1.5',
)
