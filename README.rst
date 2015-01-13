Test Steps functions for each assertion and automatic logging
===============================================================

.. image:: https://pypip.in/v/test_steps/badge.png
    :target: https://crate.io/packages/test_steps/

.. image:: https://pypip.in/d/test_steps/badge.png
    :target: https://crate.io/packages/test_steps/

TestSteps is to implement a bunch of functions about test steps and logging.
The purpose is to simplify the assertion and automatically logging the steps,
which are not supported in most of the current python test frames.

All the step and logging functions can be used independently, or be used in test frameworks
as py.test or nose


Install test_steps
------------------

::

    pip install test_steps


Example for using simple-step functions
---------------------------------------

.. code-block:: python

    from test_steps import *
    def test_example()
        ok("just pass the step and log it")
        #fail("Just fail the step and log it")
        ok(3+2 == 5, "pass if expr else fail")
        #eq("Shanghai", "Beijing", "Shanghai not equal to Beijing")
        eq(4+5, 9)
        ne("Shanghai", "Beijing", "Pass, Shanghai not equal to Beijing")
        #'Shanghai City' contains 'Country', the second parameter could be regex
        match("Shanghai City", "Country")
        unmatch("Shanghai City", "Country", "Pass, not contains, regex can be used too")

More functions: lt, gt, more operators/functions can be added, see the section:
add more operators/step functions via 3 steps


Logging of the steps
--------------------
If the log_level is set to INFO, and you added the data-time format to it,
the logging of the execution of test_example() case would be like::

    2015-01-10 20:43:22,787 - Test - INFO - ------------------------------------------------------
    2015-01-10 20:43:22,788 - Test - INFO - Case test_example in file: /Users/Steven004/test/demo.py
    2015-01-10 20:43:22,788 - Test - INFO - Step-1: just pass the step and log it - PASS:
    2015-01-10 20:43:26,789 - Test - INFO - Step-2: pass if expr else fail - PASS:
    2015-01-10 20:43:26,789 - Test - INFO - Step-3: 9 == 9 - PASS:
    2015-01-10 20:43:26,789 - Test - INFO - Step-4: Pass, Shanghai not equal to Beijing - PASS:
    2015-01-10 20:43:29,792 - Test - ERROR - Step-5: "Shanghai City" =~ "Country" - FAIL: "Shanghai City" =~ "Country"?


The log-level can be setting, and logging handler can be set by the user, as all you
can do for standard logging.
If a step function is in a loop, there will be multiple steps logged.


Advanced step functions
-----------------------

To simplify the testing,

.. code-block:: python

    step(code_string, globals=globals(), locals=locals(), **args)
    steps(multiple_steps_code_string_with_options, globals=globals(), locals=locals())
    # s is an alias of steps

The step function is to execute the code string in the particular name spaces, with some options
to provide some advanced feature. The code string will be recorded for the step if desc is None.
The steps function is for writing multiple steps in a simpler format.

Supported optional args in step::

    - timeout: e.g. timeout=30, fail if the step could not complete in 30 seconds
    - repeat: e.g. repeat=20, repeat in another second if fail until pass, timeout in 20s
    - duration: e.g. duration=15, stay in this step for 15 seconds, even it completed shortly
    - xfail: e.g. xfail=True, expected failure, report pass when fail, vice versa
    - warning: e.g. warning=True, Pass the step anyway, but log a warning message if the condition is not met
    - skip: e.g. skip=True, just skip this case.

Please be noticed that for any step fails, the test will be terminated (in py.test or other test framework,
the current case will be terminated), unless you set *warning* option for it.


Examples:

.. code-block:: python

    # Just as match(string1.range(1..4), r'\w\-\w') function
    step("match(string1.range(1..4), r'\w\-\w')")
    # Run the code string; pass if it return in 15 seconds, or fail with timeout exception
    step("num_async.data_sync()", timeout = 15)
    # repeat option. In 20 seconds, if the expr returns False, re-run it every another second,
    # until it returns True (which means pass), or time is out (which means fail)
    step("num_async.get_value() == 500", repeat = 20, xfail = True)
    # Run code_string in a particular name space, here, to run code string in shanghai object's name space
    step("cars.averagespeed() > 50 ", globals = shanghai.__dict__)


Not as the other step functions (eq, ne, ...), the step/steps functions just use operator to
write the steps in a string. The mapping of operators and step functions::

    == : eq         != : ne         > : gt      < : lt      >= : ge     <= : le
    =~ : match      !~ : unmatch


*steps* is another way to write steps in one statement. When the function steps (or s) is used,
the format is a little bit different. It uses command-arguments-like format. And you can set the
name spaces in one shot for all the steps in the code string.
The following code has the same function as the 3 first 3 steps in the code above

.. code-block:: python

    steps('''
        string1.range(1..4) =~ r'\w\-\w'
        num_async.data_sync()   -t 15
        num_async.get_value() == 500    -r 20   -x
        ''')

Options in steps(or s) ::

    -t 30   or --timeout 30    in steps()             means           timeout=30    in step()
    -r 10   or --repeat  10    in steps()             means           repeat=10
    -d 10   or --duration 10                          means           duration=10
    -x  or --xfail or -x True or --xfail True         means           xfail=True
    -w  or --warning  or -w True  or --warning True   means           warning=True
    -s  or --skip     or -s True  or --skip True      means           skip=True


Add more operators/step functions via 3 steps
---------------------------------------------
For different product, or scenarios, some other operation you may want to define and add them
for logging, it's easy based on this framework.

1. Define a comparing function for two objects, e.g., to compare to date string

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


#. Register it into the test_steps framework:

.. code-block:: python

    # bind the compDate function with '=d=' operator
    # After this step, you can directly use the operator in step/steps/s functions
    addBiOperator('=d=', compDate)

#. Get the opWapperFunction

.. code-block:: python

    sameDate = getOpWrapper('=d=')

Now, everything is good, you can write the following steps in your scripts now, and
everything will be auto logged.

.. code-block:: python

    sameDate("01/03/2015", "1-3-2015", "description: this step should pass")
    step(" '03/05/2014' =d= '3/5/2014' ")


Currently, just binary operators are supported.



logging setting
---------------

The default logger is Python logging module. You can directly use it to write logs, such as:

.. code-block:: python

    test_logger.info("This will be write in to the /tmp/test_log/mm-dd-yyyy.log file")
    test_logger.debug("debug information")


You can set your own logger for your test as below:

.. code-block:: python

    test_steps.setlogger(your_logger)
    # your_logger could be a logging object, or any object which support methods like info, error, ...

Or, you can directly config or format the test_logger, just as you do for a normal logging object.

Of course, you can set your log format, and the log files. By default, the log is print to the
standard output.





