
from setuptools import setup, find_packages
import test_steps

setup(
    name='test_steps',
    description='Simple way to run test steps and automatic logging',
    author='Steven LI',
    author_email='steven004@gmail.com',
    classifiers=[
        "Development Status :: 6 - Mature",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3"
    ],
    version=test_steps.__version__,
    url = "https://github.com/steven004/TestSteps",
    packages = find_packages(),
    include_package_data = True,
)

