__author__ = 'Steven LI'

from test_steps import *
import logging, time

def my_add(*args):
    ret = 0
    for i in args:
        ret += i
    return ret

def my_mul(*args):
    ret = 1
    for i in args:
        ret *= i
    return ret


def test_logger_setup():
    ''' Add file-logging into test_logger
        This is changed from 0.6.1 version.
        In previous version, this is added by default, but loss of flexibility.
        So, leave for user from 0.6.1
    '''

    file_name = time.strftime('/tmp/test'+"_%Y%m%d_%H%M.log")
    fh = logging.FileHandler(file_name)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    test_logger.addHandler(fh)


def test_basic():
    test_logger.info("To show the basic auto-log functions")
    ## eq(expr1, expr2, passdesc='', faildesc='')
    eq(my_add(3,4,5), my_mul(3,4), "3+4+5 == 3*4")
    ne(my_add(3,4,6), 12)
    gt(my_add(3,4,5), 10)
    ge(my_mul(3,4), 11)
    lt(my_add(5,6,7), my_add(3,4,5,7))
    le(my_add(5,6,7), my_add(3,4,5,6))
    match("Shanghai City", "City")  #regex can be used for the 2nd parameter
    unmatch("I ate an apple", r'banana|orange')
    ## ok(boolean_expr, passdesc='', faildesc='')
    ok(3>5, "3<5, logged when pass... ", "3<5, logged when fail")
    fail("Just fail and log. nothing more")

## The following logging information will be auto-logged in log file when running the test_basic
## The log file is '/tmp/test_yyyymmdd_hhmm.log'
##
'''
2015-01-15 20:09:13,731 - INFO - To show the basic auto-log functions
2015-01-15 20:09:13,746 - INFO - ------------------------------------------------------
2015-01-15 20:09:13,746 - INFO - Func test_basic in file: /TestSteps/test_examples/test_lesson1_autolog.py
2015-01-15 20:09:13,746 - INFO - Check-1: 3+4+5 == 3*4 - PASS - 12 == 12?
2015-01-15 20:09:13,746 - INFO - Check-2: 13 != 12 - PASS - 13 != 12?
2015-01-15 20:09:13,746 - INFO - Check-3: 12 > 10 - PASS - 12 > 10?
2015-01-15 20:09:13,746 - INFO - Check-4: 12 >= 11 - PASS - 12 >= 11?
2015-01-15 20:09:13,746 - INFO - Check-5: 18 < 19 - PASS - 18 < 19?
2015-01-15 20:09:13,747 - INFO - Check-6: 18 <= 18 - PASS - 18 <= 18?
2015-01-15 20:09:13,747 - INFO - Check-7: 'Shanghai City' =~ 'City' - PASS - 'Shanghai City' =~ 'City'?
2015-01-15 20:09:13,747 - INFO - Check-8: 'I ate an apple' !~ 'banana|orange' - PASS - 'I ate an apple' !~ 'banana|orange'?
2015-01-15 20:09:13,747 - ERROR - Check-9: 3<5, logged when fail - FAIL -
'''

########################################################################################
# Program stop on a failed step. (if you want it continue, take more lessons)
# Take lesson 2 to get more powerful functions
########################################################################################


if __name__ == '__main__':
    test_logger_setup()
    test_basic()