"""
This pytest plugin is very simple, which is for users who use test_steps in py.test framework.
Use this plugin, the function detection mechanism is using pytest runtest_setup to do it, instead of
using the original mechanism, which requires users know more about the auto-function-detection while
writing scripts originally.
Now, it will be all set, while taken care of by this plugin.
"""


__author__ = 'Steven LI'

import test_steps
import pytest


def pytest_configure(config):
    test_steps.auto_func_detection(False)


def pytest_runtest_setup(item):
    test_steps.log_new_func(item.name, str(item.fspath) )

