Changelog
=========


v0.9.5
------
* Add defult log file-handler support using an environment variable TESTSTEP_LOG_PATH. When this
environment variable is defined. It will check if the path exists, if yes, logs will be automatically
saved in the defined directory, if not, do nothing.


v0.9.0
------
* Fix issue #30: Fix the .py type testbed config file import problem.


v0.8.9
------
* Fix issue #28: Change the environment variable TESTBED_CONFIG_PATH to TESTSUITE_CONFIG_PATH
to avoid concept confusion.


v0.8.8
------
* Fix #27: Environment variable TESTBED_CONFIG_PATH support. Now the scripts could use the same test bed configuration
file, but the tester can place the file into different folders for different purpose. When running the test, the config
file under the path indicated by TESTBED_CONFIG_PATH will be used.


v0.8.6
------
* Fix #24: relative path handling in yaml_testbed function. Now it will check the path relative to the cwd(),
if not exists, it will try to get the file relative to the parent file location.

v0.8.3
------
* Fix #25: default test bed file support. Now you can invoke init_testbed() without parameters.
In this case, it will automatically load the .yaml file with the same base name of the script file.


v0.8.2
------
* Fix the python2 compatible issue.


v0.8.1
------
* Implement enhancement of the issue#21. Implement a function init_testbed to
initialize objects in a test bed, which is described in a .py or .yaml file.
and added a new example to use init_testbed function


v0.7.1
------
* Fix the issue#20, let the step pass when return is 0 or Zone by default. This can be reset by
changing the RunPassSet.


v0.6.2
------
* Change the log to Standard output only by default, the user can add more handlers by self


v0.6.0
------
* add has(=>) and hasnt(!>) operator, to check if a set has or hasnt an item.


v0.5.1
------
* add __auto_func_detection__ local variable to disable the function detection
* add function to disable auto function detection globally
* add function for user to start a function logging explicitly.


v0.4.0
------
* add lesson 5 example for checks batch argument
* fix issue #12: multiple options for checks error


v0.3.0
------
* add passdesc (-p) and faildesc (-f) option for step/check function
* add check/checks as alias for step/steps
* add the return values for step and steps function
* add a batch parameter to steps/checks function


v0.2.0
------
* added debug info logging
* added -e and -w option for exception and warning
* add a mechanism for new option insertion
* enhanced the ok function


v0.1.0
------

This is a fairly complete list of v0.1, which can
serve as a reference for test engineers.

* automatically log test cases and steps
* implemented general operators and corresponding functions, including::
    eq, ne, gt, lt, ge, le, match, unmatch
* implemented the framework for adding new operators and functions
* implemented step/steps/s functions, which can be used in some test frameworks
