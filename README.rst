Test Steps functions for each assertion and automatic logging
=============================================================

The package test_steps is to implement a bunch of functions about test checks and logging.
The purpose is to simplify the assertion and automatically logging the checks,
which are not supported in most of the current python test frames.

All the checks and logging functions can be used independently, or be used in test frameworks
as py.test or nose


Magics in source code
---------------------

To make is extensible and more flexible, meta-programming and functional programming technologies
are used in this package. It makes the source is thus likely not something for Python beginners.
However, you are welcome if you want to study meta-programming or functional programming, and
your comments are always appreciated


Install test_steps
------------------

::

    pip install test_steps


Lessons with examples
---------------------

lesson 1 - the basic auto-log boolean functions:
https://github.com/steven004/TestSteps/blob/master/test_examples/test_lesson1_autolog.py

lesson 2 - the check function with auto-log string:
https://github.com/steven004/TestSteps/blob/master/test_examples/test_lesson2_check.py

lesson 3 - the check functions with options:
https://github.com/steven004/TestSteps/blob/master/test_examples/test_lesson3_options.py

lesson 4 - the checks functions - another format for multiple check(s):
https://github.com/steven004/TestSteps/blob/master/test_examples/test_lesson4_checks.py

lesson 5 - get return from check and checks function:
https://github.com/steven004/TestSteps/blob/master/test_examples/test_lesson5_return.py

lesson 6 - function auto-detection mechanism (pytest/nose users can skip this, use plugin instead):
https://github.com/steven004/TestSteps/blob/master/test_examples/test_lesson6_func_auto_check.py

lesson 7 - return value setting as case pass (0 or None is considerred as pass by default:
https://github.com/steven004/TestSteps/blob/master/test_examples/test_lesson7_returnvalue.py

lesson 8 - yaml test bed initialization support:
https://github.com/steven004/TestSteps/blob/master/test_examples/test_lesson8_yaml_testbed.py
https://github.com/steven004/TestSteps/blob/master/test_examples/test_lesson8_yaml_testbed2.py

lesson 9 - python format test bed initialization support:
https://github.com/steven004/TestSteps/blob/master/test_examples/test_lesson9_pytestbed.py


pytest-autochecklog/nose-autochecklog plugin
--------------------------------------------

For pytest or nosetests user, you can use the pytest-autochecklog or nose-autochecklog plugin
to use test_steps module. The pytest-autochecklog or nose-autochecklog plugin
has better auto-func-detection mechanism.

Get it from: https://pypi.python.org/pypi?:action=display&name=pytest-autochecklog

or: https://pypi.python.org/pypi?:action=display&name=nose-autochecklog



Example for using simple-step functions
---------------------------------------

.. code-block:: python

    from test_steps import *
    def test_example()
        ok("just pass the check and log it")
        #fail("Just fail the check and log it")
        ok(3+2 == 5, "pass if expr else fail")
        #eq("Shanghai", "Beijing", "Shanghai not equal to Beijing")
        eq(4+5, 9)
        ne("Shanghai", "Beijing", "Pass, Shanghai not equal to Beijing")
        #'Shanghai City' contains 'Country', the second parameter could be regex
        match("Shanghai City", "Country")
        unmatch("Shanghai City", "Country", "Pass, not contains, regex can be used too")

More functions: lt, gt, more operators/functions can be added, see the section:
add more operators/check functions via 3 steps


Logging of the steps
--------------------
If the log_level is set to INFO, and you added the data-time format to it,
the logging of the execution of test_example() case would be like::

    2015-01-10 20:43:22,787 - INFO - ------------------------------------------------------
    2015-01-10 20:43:22,788 - INFO - Func test_example in file: /Users/Steven004/test/demo.py
    2015-01-10 20:43:22,788 - INFO - Check-1: just pass the check and log it - PASS:
    2015-01-10 20:43:26,789 - INFO - Check-2: pass if expr else fail - PASS:
    2015-01-10 20:43:26,789 - INFO - Check-3: 9 == 9 - PASS:
    2015-01-10 20:43:26,789 - INFO - Check-4: Pass, Shanghai not equal to Beijing - PASS:
    2015-01-10 20:43:29,792 - ERROR - Check-5: "Shanghai City" =~ "Country" - FAIL: "Shanghai City" =~ "Country"?


The log-level can be setting, and logging handler can be set by the user, as all you
can do for standard logging.
If a check function is in a loop, there will be multiple checks logged.


Advanced check functions
------------------------

To simplify the testing,

.. code-block:: python

    check(code_string, globals=globals(), locals=locals(), **kwargs)
    checks(multiple_checks_code_string_with_options, globals=globals(), locals=locals())
    # s is an alias of checks, step=check, s=steps=checks

The check function is to execute the code string in the particular name spaces, with some options
to provide some advanced feature. The code string will be recorded for the check if desc is None.
The checks function is for writing multiple checks in a simpler format.

Supported optional args in check::

    - timeout: e.g. timeout=30, fail if the step could not complete in 30 seconds
    - repeat: e.g. repeat=20, repeat in another second if fail until pass, timeout in 20s
    - duration: e.g. duration=15, stay in this step for 15 seconds, even it completed shortly
    - xfail: e.g. xfail=True, expected failure, report pass when fail, vice versa
    - warning: e.g. warning=True, Pass the step anyway, but log a warning message if the condition is not met
    - skip: e.g. skip=True, just skip this case.
    - exception: e.g. exception=NameError, expected exception will be raised. pass if so, or fail
    - passdesc: e.g. passdesc="the string to log if passed" (replace the code_string in the log)
    - faildesc: e.g. faildesc="the string to log if failed" (replace the code_string in the log)

Please be noticed that for any step fails, the test will be terminated (in py.test or other test framework,
the current case will be terminated), unless you set *warning* option for it.


Examples:

.. code-block:: python

    # Just as match(string1.range(1..4), r'\w\-\w') function
    check("match(string1.range(1..4), r'\w\-\w')")
    # Run the code string; pass if it return in 15 seconds, or fail with timeout exception
    check("num_async.data_sync()", timeout = 15)
    # repeat option. In 20 seconds, if the expr returns False, re-run it every another second,
    # until it returns True (which means pass), or time is out (which means fail)
    check("num_async.get_value() == 500", repeat = 20, xfail = True)
    # Run code_string in a particular name space, here, to run code string in shanghai object's name space
    check("cars.averagespeed() > 50 ", globals = shanghai.__dict__)
    check("1/0", exception=ZeroDivisionError, passdesc='Pass, expected to have the ZeroDivisionError')


Not as the other check functions (eq, ne, ...), the check/checks functions just use operator to
write the checks in a string. The mapping of operators and check functions::

    == : eq         != : ne         > : gt      < : lt      >= : ge     <= : le
    =~ : match      !~ : unmatch    =>: has     !> hasnt


*checks* is another way to write checks in one statement. When the function checks (or s) is used,
the format is a little bit different. It uses command-arguments-like format. And you can set the
name spaces in one shot for all the checks in the code string.
The following code has the same function as the 3 first 3 steps in the code above

.. code-block:: python

    checks('''
        string1.range(1..4) =~ r'\w\-\w'
        num_async.data_sync()   -t 15
        num_async.get_value() == 500    -r 20   -x
        ''')

Options in checks(or s) ::

    -t 30   or --timeout 30    in checks()             means       timeout=30    in check()
    -r 10   or --repeat  10    in checks()             means       repeat=10
    -d 10   or --duration 10                          means       duration=10
    -x  or --xfail or -x True or --xfail True         means       xfail=True
    -w  or --warning  or -w True  or --warning True   means       warning=True
    -s  or --skip     or -s True  or --skip True      means       skip=True
    -e MyException                                    means       exception=MyException
    -p pass_str or --passdesc pass_str                means       passdesc=pass_str
    -f fail_str or --faildesc fail_str                means       faildesc=fail_str


Add more operators/check functions via 3 steps
----------------------------------------------
For different product, or scenarios, some other operation you may want to define and add them
for logging, it's easy based on this framework.

1. Define a comparing function for two expressions, e.g., to compare to date string

.. code-block:: python

    ##  compDate('1/4/2015', '01-04-2015') return True
    def compDate(date1, date2):
        import re
        pattern = re.compile(r'(\d+).(\d+).(\d+)')
        match1 = pattern.match(date1)
        match2 = pattern.match(date2)
        day1, month1, year1 = (int(i) for i in match1.group(1,2,3))
        day2, month2, year2 = (int(i) for i in match2.group(1,2,3))
        return (year1==year2) and (month1==month2) and (day1==day2)


2. Register it into the test_steps framework:

.. code-block:: python

    # bind the compDate function with '=d=' operator
    # After this step, you can directly use the operator in step/steps/s functions
    addBiOperator('=d=', compDate)

3. Get the opWapperFunction

.. code-block:: python

    sameDate = getOpWrapper('=d=')

Now, everything is good, you can write the following steps in your scripts now, and
everything will be auto logged.

.. code-block:: python

    sameDate("01/03/2015", "1-3-2015", "description: this step should pass")
    check(" '03/05/2014' =d= '3/5/2014' ")


Currently, just binary operators are supported.


Test Bed initialization (Environment Variable: TESTSUITE_CONFIG_PATH)
---------------------------------------------------------------------

This feature is to improve test scripts portabiity. When we write scripts, we'd like to separate
test bed description and code into separated files. One test suite could run on different test beds.
This feature support an environment variable *TESTSUITE_CONFIG_PATH*, which indicate where the test bed
description file is located. Two kinds of format of test beds are supported: .py or .yaml

Examples:

.. code-block:: python

    # Initiate a test bed which is indicated as a absolute path
    # Initiated test bed will be return as a module
    tb_m = init_testbed("/Users/xili4/PycharmProjects/TestSteps/test_examples/lesson8_testbed_obj.yaml")

    # Initiated a test bed which is in the path TESTSUITE_CONFIG_PATH indicated
    # or get it from the scripts path if no TESTSUITE_CONFIG_PATH defined
    tb_m = init_testbed('test_lesson8_yaml_testbed2.yaml')

    # Initiated a test bed which has the same base name of the scripts file, but using yaml as extended name
    tb_m = init_testbed()

    # Initiate a .py test bed described in the path TESTSUITE_CONFIG_PATH indicated
    # or in the scripts located path
    tb_m = init_testbed('lesson9_pytestbed_config.py')


logging setting (Environment Variable: TESTSTEP_LOG_PATH)
---------------------------------------------------------

The default logger test_logger is a Python logging instance, from the code like:

.. code-block:: python

    test_logger = logging.getLogger("Test").

You can directly use it to write logs, such as:

.. code-block:: python

    test_logger.info("This will be write in to the /tmp/test_log/mm-dd-yyyy.log file")
    test_logger.debug("debug information")

By default, log level is WARNING, and the log will be outputted to standard output automatically. If
*TESTSTEP_LOG_PATH* environment variable is defined. The log will be outputted to the defined directory
too with a time stamp each time when running a test. For example, when you defined

.. code-block::

    #export TESTSTEP_LOG_PATH='/home/steven004/test'


And the directory does actually exist, you will find the test logs in that directory /home/steven004/test/
anytime you run a test.


You can change the default test_logger or combine with another one using the setlogger method:

.. code-block:: python

    setlogger(your_logger)
    # your_logger could be a logging object, or any object which support methods like info, error, ...


