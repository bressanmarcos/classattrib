from setuptools import setup, find_packages
from os.path import join, dirname

with open(join(dirname(__file__), "dynattrib", "__version__.py")) as v:
    __version__ = None
    exec(v.read().strip())

with open("README.md") as f:
    long_description = f.read()

setup(
    name="dynattrib",
    packages=find_packages(include=["dynattrib*"]),
    version=__version__,
    author="Marcos Bressan",
    author_email="bressan@dee.ufc.br",
    description="Dynamic class attributes for Python context managers.",
    long_description=long_description,
    long_description_content_type="text/mardown",
    url="https://github.com/bressanmarcos/dynattrib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=True,
)
