from __future__ import unicode_literals

from setuptools import setup

classify = [
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python",
    "Topic :: Games/Entertainment :: Role-Playing",
    "Topic :: Games/Entertainment",
]

setup(
    classifiers=classify,
    description="TubeStrike!\n\nAn Endless Commuter",
    entry_points={"console_scripts": ["tubestrike = tubestrike:main"]},
    install_requires=["pygame"],
    license="GPLv3+",
    name="tubestrike",
    version="0.0.1"
)
