from __future__ import annotations

from setuptools import find_packages, setup

from py_typed_events import __version__

setup(
    name="py_typed_events",
    version=__version__,
    url="https://github.com/cspotcode/py_typed_events",
    author="Andrew Bradley",
    author_email="cspotcode@gmail.com",
    packages=find_packages(),
)
