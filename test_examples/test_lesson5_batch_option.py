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


def test_checks():
    test_logger.info("To show the check with options functions")
    ## same functions as test_check_options
    checks('''
        my_add(3,4,5) == my_mul(3,4)    -d 3
        my_add(3,4,6) == 12     -w
        my_mul(3,4,5) > 20      -t 1
        my_mul(2,3)/my_add() == 5   -e ZeroDivisionError
        my_mul(2,3)*my_add(1) >= 5  -p "result is 5, pass"  -f "result <= 5"
        my_mul(2,3)*my_add(3) < 5   -x
        my_mul(4,5)*5 == 0  -s
        my_add(3,4) >= 11   -r 5
    ''')

## The following logging information will be auto-logged in log file when running the test_basic
## As you can see, just 3 checks had been executed, since there is an error happens in check-3
'''
2015-01-17 17:29:57,745 - INFO - To show the check with options functions
2015-01-17 17:30:00,748 - INFO - ------------------------------------------------------
2015-01-17 17:30:00,748 - INFO - Func test_checks in file: /Users/xili4/PycharmProjects/TestSteps/test_examples/test_lesson5_batch_option.py
2015-01-17 17:30:00,748 - INFO - Check-1: my_add(3,4,5) == my_mul(3,4) -PASS- 12 == 12  - sleep 0 seconds (-d 3 set)
2015-01-17 17:30:00,749 - INFO - Check-2: my_add(3,4,6) == 12 -PASS- 13 == 12
2015-01-17 17:30:00,749 - WARNING -   ^^^  condition not met (pass due to -w option set)  ^^^
2015-01-17 17:30:01,750 - ERROR - Check-3: my_mul(3,4,5) > 20 -FAIL-   - Step Timeout (-t 1 set)
'''


###### The only difference is the batch argument, (by default batch=False)
def test_checks_batch():
    test_logger.info("To show the check with options functions")
    ## same functions as test_check_options
    checks('''
        my_add(3,4,5) == my_mul(3,4)    -d 3
        my_add(3,4,6) == 12     -w
        my_mul(3,4,5) > 20      -t 1
        my_mul(2,3)/my_add() == 5   -e ZeroDivisionError
        my_mul(2,3)*my_add(1) >= 5  -p "result is 5, pass"  -f "result <= 5"
        my_mul(2,3)*my_add(3) < 5   -x
        my_mul(4,5)*5 == 0  -s
        my_add(3,4) >= 11   -r 5
    ''', batch=True)


## The following logging information will be auto-logged in log file when running the test_basic
## What's the difference from the case above? it executed all checks, when set batch=True
## At the same time, additional check added for the overall batch-check, see check-9
'''
2015-01-17 17:30:01,757 - INFO - To show the check with options functions
2015-01-17 17:30:04,759 - INFO - ------------------------------------------------------
2015-01-17 17:30:04,759 - INFO - Func test_checks_batch in file: /Users/xili4/PycharmProjects/TestSteps/test_examples/test_lesson5_batch_option.py
2015-01-17 17:30:04,759 - INFO - Check-1: my_add(3,4,5) == my_mul(3,4) -PASS- 12 == 12  - sleep 1 seconds (-d 3 set)
2015-01-17 17:30:04,759 - INFO - Check-2: my_add(3,4,6) == 12 -PASS- 13 == 12
2015-01-17 17:30:04,759 - WARNING -   ^^^  condition not met (pass due to -w option set)  ^^^ 
2015-01-17 17:30:05,761 - ERROR - Check-3: my_mul(3,4,5) > 20 -FAIL-   - Step Timeout (-t 1 set)
2015-01-17 17:30:05,761 - DEBUG -     ^^^ 4: my_mul(3,4,5) > 20 - FAIL - TestStepFail('my_mul(3,4,5) > 20', '  - Step Timeout (-t 1 set)')   ^^^
2015-01-17 17:30:07,560 - INFO - Check-4: my_mul(2,3)/my_add() == 5 -PASS-  - exception: <class 'ZeroDivisionError'> caught
2015-01-17 17:30:10,456 - INFO - Check-5: result is 5, pass -PASS- 6 >= 5
2015-01-17 17:30:13,445 - DEBUG -     vvv  reverse the result (due to -x option set)  vvv
2015-01-17 17:30:13,446 - INFO - Check-6: my_mul(2,3)*my_add(3) < 5 -PASS- 18 < 5   - Original result: False (-x option set) 
2015-01-17 17:30:13,446 - INFO - Check-7: my_mul(4,5)*5 == 0 -PASS-   - SKIPPED (-s option set)
2015-01-17 17:30:18,449 - DEBUG -    vvv  Results(-r 5 set) { 1:<7 >= 11>  2:<7 >= 11>  3:<7 >= 11>  4:<7 >= 11>  5:<7 >= 11>  }  vvv
2015-01-17 17:30:18,450 - ERROR - Check-8: my_add(3,4) >= 11 -FAIL- 7 >= 11 - tried 5 times in 5 seconds
2015-01-17 17:30:18,450 - DEBUG -     ^^^ 9: my_add(3,4) >= 11 - FAIL - TestStepFail('my_add(3,4) >= 11', '7 >= 11 - tried 5 times in 5 seconds')   ^^^
2015-01-17 17:30:18,450 - ERROR - Check-9: Overall Batch Result: 2 checks failed -FAIL- 1st failed step: (line_10) my_mul(3,4,5) > 20
'''


if __name__ == '__main__':
    test_checks()
    test_checks_batch()
