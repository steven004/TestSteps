
from setuptools import setup
import test_steps

setup(
    name='test_steps',
    description='Simple way to run test steps and automatic logging',
    author='Steven LI',
    author_email='steven004@gmail.com',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Topic :: System :: Logging",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ],
    version=test_steps.__version__,
    url = "https://github.com/steven004/TestSteps",
    packages = ['test_steps'],
    #include_package_data = True,
)

