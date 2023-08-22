"""
CVScanAI Setup Script
This script is used to configure the installation and distribution of the CVScanAI project.
Usage:
    python setup.py [command]
Commands:
    clean       Remove build artifacts and temporary files.
    test        Run the test suite for the CVScanAI project.
    build       Build the distribution packages for the CVScanAI project.
For more information, refer to the project documentation at:
https://github.com/COXIT-CO/CVScanAI
"""
from setuptools import setup
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path("./version.py")
with open(ver_path, encoding="utf-8") as ver_file:
    # pylint: disable-next=exec-used
    exec(ver_file.read(), main_ns)

__version__ = main_ns["__version__"]

setup(
    name="CVScanAI",
    version=__version__,
    url="https://github.com/COXIT-CO/CVScanAI",
    description="AI Driven CV Validator",
    author="COXIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: MIT",
        "Programming Language :: Python :: 3.9",
    ],
)
