__author__ = 'Steven LI'

from test_steps import *

def my_add(*args):
    ret = 0
    for i in args:
        ret += i
    return ret

#############################################################################
## Please notice sleep in my_mul function
def my_mul(*args):
    import time, random
    time.sleep(random.uniform(1,3))
    ret = 1
    for i in args:
        ret *= i
    return ret


def test_check_options():
    test_logger.info("To show the check with options functions")
    ## check("expr1 op expr2", globals=globals(), locals=locals(), **kwargs)
    ## **kwargs means options, we will see them one by one here
    # duration: the step will last at least duration seconds, sleep if return earlier
    check("my_add(3,4,5) == my_mul(3,4)", duration=3)
    # warning: pass this check anyway, but log a warning message
    check("my_add(3,4,6) == 12", warning=True)
    # timeout: if the step does not return in timeout seconds, it will fail
    check("my_mul(3,4,5) > 20", timeout=1, warning=True)
    # exception: expected there is an exception in the step, or fail
    check("my_mul(2,3)/my_add() == 5", exception=ZeroDivisionError)
    # passdesc/faildesc: the description for pass/fail to replace the code_string in the log
    check("my_mul(2,3)*my_add(1) >= 5", passdesc="result is 5, pass", faildesc="result <= 5")
    # xfail: expected fail, that is reverse the result
    check("my_mul(2,3)*my_add(3) < 5", xfail=True)
    # skip: skip this case, do not execute it, just pass
    check("my_mul(4,5)*5 == 0", skip=True)
    # repeat: repeat the step another second if the condition is not satisfied, until time out in 'repeat' seconds
    check("my_add(3,4) >= 11", repeat=5)

################ the log sample of above function test - test_check_options #######################
'''
2015-01-15 20:39:57,676 - INFO - To show the check with options functions
2015-01-15 20:40:00,678 - INFO - ------------------------------------------------------
2015-01-15 20:40:00,678 - INFO - Func test_check_options in file: /Users/xili4/PycharmProjects/TestSteps/test_examples/test_lesson4_checks.py
2015-01-15 20:40:00,678 - INFO - Check-1: my_add(3,4,5) == my_mul(3,4) - PASS - 12 == 12  - sleep 1 seconds (-d 3 set)
2015-01-15 20:40:00,678 - WARNING - --v-- condition not met (pass due to -w option set) --v--
2015-01-15 20:40:00,678 - INFO - Check-2: my_add(3,4,6) == 12 - PASS - 13 == 12
2015-01-15 20:40:01,680 - WARNING - --v-- condition not met (pass due to -w option set) --v--
2015-01-15 20:40:01,680 - INFO - Check-3: my_mul(3,4,5) > 20 - PASS -   - Step Timeout (-w 1 set)
2015-01-15 20:40:04,510 - INFO - Check-4: my_mul(2,3)/my_add() == 5 - PASS -  - exception: <class 'ZeroDivisionError'> caught
2015-01-15 20:40:06,161 - INFO - Check-5: result is 5, pass - PASS - 6 >= 5
2015-01-15 20:40:07,364 - INFO - Check-6: my_mul(2,3)*my_add(3) < 5 - PASS - 18 < 5   - Original result: False (-x option set)
2015-01-15 20:40:07,364 - INFO - Check-7: my_mul(4,5)*5 == 0 - PASS -   - SKIPPED (-s option set)
2015-01-15 20:40:12,367 - DEBUG - Results(-r 5 set) { 1:<7 >= 11>  2:<7 >= 11>  3:<7 >= 11>  4:<7 >= 11>  5:<7 >= 11>  }
2015-01-15 20:40:12,367 - ERROR - Check-8: my_add(3,4) >= 11 - FAIL - 7 >= 11 - tried 5 times in 5 seconds
'''
### If you review the logs, you can see additional information (including info and debug info)
### provided for the tester's information.




##########################################################################
### checks is another functions to do a bundle execution of check(s)
## You can use steps(), which totally equals to checks(), just another name
def test_checks_options():
    test_logger.info("To show the check with options functions")
    ## same functions as test_check_options
    checks('''
        my_add(3,4,5) == my_mul(3,4)    -d 3
        my_add(3,4,6) == 12     -w
        my_mul(3,4,5) > 20      -w  -t 1
        my_mul(2,3)/my_add() == 5   -e ZeroDivisionError
        my_mul(2,3)*my_add(1) >= 5  -p "result is 5, pass"  -f "result <= 5"
        my_mul(2,3)*my_add(3) < 5   -x
        my_mul(4,5)*5 == 0  -s
        my_add(3,4) >= 11   -r 5
    ''')

##### The similar log, same execution, but code looks cleaner, and easier to review.
## The default log file is '/tmp/test_yyyymmdd_hhmm.log
##
'''
2015-01-15 20:53:37,330 - INFO - To show the check with options functions
2015-01-15 20:53:40,332 - INFO - ------------------------------------------------------
2015-01-15 20:53:40,332 - INFO - Func test_check_options in file: /Users/xili4/PycharmProjects/TestSteps/test_examples/test_lesson4_checks.py
2015-01-15 20:53:40,332 - INFO - Check-1: my_add(3,4,5) == my_mul(3,4) -PASS- 12 == 12  - sleep 0 seconds (-d 3 set)
2015-01-15 20:53:40,332 - WARNING - --v-- condition not met (pass due to -w option set) --v--
2015-01-15 20:53:40,332 - INFO - Check-2: my_add(3,4,6) == 12 -PASS- 13 == 12
2015-01-15 20:53:41,333 - WARNING - --v-- condition not met (pass due to -w option set) --v--
2015-01-15 20:53:41,333 - INFO - Check-3: my_mul(3,4,5) > 20 -PASS-   - Step Timeout (-w 1 set)
2015-01-15 20:53:44,186 - INFO - Check-4: my_mul(2,3)/my_add() == 5 -PASS-  - exception: <class 'ZeroDivisionError'> caught
2015-01-15 20:53:45,519 - INFO - Check-5: result is 5, pass -PASS- 6 >= 5
2015-01-15 20:53:46,672 - INFO - Check-6: my_mul(2,3)*my_add(3) < 5 -PASS- 18 < 5   - Original result: False (-x option set)
2015-01-15 20:53:46,672 - INFO - Check-7: my_mul(4,5)*5 == 0 -PASS-   - SKIPPED (-s option set)
2015-01-15 20:53:51,675 - DEBUG - Results(-r 5 set) { 1:<7 >= 11>  2:<7 >= 11>  3:<7 >= 11>  4:<7 >= 11>  5:<7 >= 11>  }
2015-01-15 20:53:51,676 - ERROR - Check-8: my_add(3,4) >= 11 -FAIL- 7 >= 11 - tried 5 times in 5 seconds
'''

################################################################################
# in checks() function, we have a command-option-style option input, which is different than in check()
#
# you can use short or long prefix option as indicated below:

#  -------- in checks() ----------                             ----in check() -----
#   -t 30   or --timeout 30                           means       timeout=30
#   -r 10   or --repeat  10                           means       repeat=10
#   -d 10   or --duration 10                          means       duration=10
#   -x  or --xfail or -x True or --xfail True         means       xfail=True
#   -w  or --warning  or -w True  or --warning True   means       warning=True
#   -s  or --skip     or -s True  or --skip True      means       skip=True
#   -e MyException                                    means       exception=MyException
#   -p pass_str or --passdesc pass_str                means       passdesc=pass_str
#   -f fail_str or --faildesc fail_str                means       faildesc=fail_str


##################################################################################
# Sometimes, you want to continue the test even if there is one check failed, but after run all
# the checks, you want the case fail. Then, we need to introduce the batch parameter for checks()
# Please see lesson 5 to get more information
##################################################################################



if __name__ == '__main__':
    test_check_options()
    test_checks_options()
