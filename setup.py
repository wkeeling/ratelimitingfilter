from setuptools import setup

setup(
    author='Will Keeling',
    author_email='will@zifferent.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='A rate limiting filter for the Python logging system',
    license='MIT',
    long_description=open('README.rst').read(),
    keywords='ratelimitingfilter',
    name='ratelimitingfilter',
    packages=['ratelimitingfilter'],
    test_suite='nose.collector',
    tests_require=['mock==2.0'],
    url='https://github.com/wkeeling/ratelimitingfilter',
    version='1.1',
)
