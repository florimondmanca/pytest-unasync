from setuptools import setup, find_packages

import unasync

setup(
    name="pycomputer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    cmdclass={"build_py": unasync.build_py},
)
