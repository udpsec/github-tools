import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(here, 'README.md')) as f:
        README = f.read()
except IOError:
    VERSION = README = ''

install_requires = ['pygithub']

setup(
    name='github_star_purge',
    version='0.1.0',
    description="A utility to help you remove all of the Github stars from your profile",
    long_description=README,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='github',
    author='Darin Gordon',
    author_email='dkcdkg@gmail.com',
    url='https://www.github.com/dowwie/github_star_purge',
    license='Apache License 2.0',
    install_requires=install_requires,
    entry_points="""\
    [console_scripts]
    github_star_purge = github_star_purge.star_purge:main
    """
)
