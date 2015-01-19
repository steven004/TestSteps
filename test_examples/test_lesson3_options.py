__author__ = 'Steven LI'

from test_steps import *

def my_add(*args):
    ret = 0
    for i in args:
        ret += i
    return ret

#############################################################################
## Please notice sleep in my_mul function
##     for options explanation
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
## Got the following log from he default log file test_20150117_1707.log
'''
2015-01-17 17:07:26,548 - INFO - To show the check with options functions
2015-01-17 17:07:29,549 - INFO - ------------------------------------------------------
2015-01-17 17:07:29,550 - INFO - Func test_check_options in file: /TestSteps/test_examples/test_lesson3_options.py
2015-01-17 17:07:29,550 - INFO - Check-1: my_add(3,4,5) == my_mul(3,4) -PASS- 12 == 12  - sleep 1 seconds (-d 3 set)
2015-01-17 17:07:29,550 - INFO - Check-2: my_add(3,4,6) == 12 -PASS- 13 == 12
2015-01-17 17:07:29,550 - WARNING -   ^^^  condition not met (pass due to -w option set)  ^^^
2015-01-17 17:07:30,551 - INFO - Check-3: my_mul(3,4,5) > 20 -PASS-   - Step Timeout (-t 1 set)
2015-01-17 17:07:30,552 - WARNING -   ^^^  condition not met (pass due to -w option set)  ^^^
2015-01-17 17:07:33,481 - INFO - Check-4: my_mul(2,3)/my_add() == 5 -PASS-  - exception: <class 'ZeroDivisionError'> caught
2015-01-17 17:07:35,560 - INFO - Check-5: result is 5, pass -PASS- 6 >= 5
2015-01-17 17:07:38,415 - DEBUG -  -vvv- reverse the result (due to -x option set) -vvv-
2015-01-17 17:07:38,416 - INFO - Check-6: my_mul(2,3)*my_add(3) < 5 -PASS- 18 < 5   - Original result: False (-x option set)
2015-01-17 17:07:38,416 - INFO - Check-7: my_mul(4,5)*5 == 0 -PASS-   - SKIPPED (-s option set)
2015-01-17 17:07:43,420 - DEBUG -  -vv-  Results(-r 5 set) { 1:<7 >= 11>  2:<7 >= 11>  3:<7 >= 11>  4:<7 >= 11>  5:<7 >= 11>  }  -vv-
2015-01-17 17:07:43,420 - ERROR - Check-8: my_add(3,4) >= 11 -FAIL- 7 >= 11 - tried 5 times in 5 seconds
'''
### If you review the logs, you can see additional information (including info and debug info)
### provided for the tester's information.
#
################### Supported options by default #######################################################
    # timeout=30, fail if the step could not complete in 30 seconds
    # repeat=20, repeat in another second if fail until pass, timeout in 20s
    # duration=15, stay in this step for 15 seconds, even it completed shortly
    # xfail=True, expected failure, report pass when fail, vice versa
    # warning=True, Pass the step anyway, but log a warning message if the condition is not met
    # skip=True, just skip this case.
    # exception=NameError, expected exception will be raised. pass if so, or fail
    # passdesc="the string to log if passed" (replace the code_string in the log)
    # faildesc="the string to log if failed" (replace the code_string in the log)
    #



## All the options will let you write a scenario in one line and easy to understand.
## Can we even write the code shorter. The answer is YES, the checks() function
## makes it simpler, and provide more functionalities.
## Take lesson 4 to get more.



if __name__ == '__main__':
    test_check_options()