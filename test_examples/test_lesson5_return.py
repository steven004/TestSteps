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


#############################################################################
# you can get the return dict from the check() and checks() function,
# when it passed. (it will raise exception when it failed)
#
def test_check():
    test_logger.info("To show return of the check function")
    ## same functions as test_check_options

    ret = check("my_add(3,4,5) == my_mul(3,4)", duration=3)
    test_logger.debug(ret)

################# The return of check is a dict #############################
# The format:
# { "result" : boolean, "values": [expr1_vul, expr2_vul], "info": infostr, "exception": exception }
#
'''
2015-01-19 20:44:39,316 - INFO - To show return of the check function
2015-01-19 20:44:42,317 - INFO - ------------------------------------------------------
2015-01-19 20:44:42,317 - INFO - Func test_check in file: /TestSteps/test_examples/test_lesson5_return.py
2015-01-19 20:44:42,317 - INFO - Check-1: my_add(3,4,5) == my_mul(3,4) -PASS- 12 == 12  - sleep 0 seconds (-d 3 set)
2015-01-19 20:44:42,317 - DEBUG - {'result': True, 'values': [12, 12], 'info': '12 == 12  - sleep 0 seconds (-d 3 set)', 'exception': None}
'''

def test_checks():
    test_logger.info("To show the checks with options functions")
    ret = checks('''
        my_add(3,4,5) == my_mul(3,4)    -d 3
        my_add(3,4,6) == 12 -w
        my_mul(3,4,5) > 20   -w -t 1
        ''')

    test_logger.debug(ret)

##############################################################################################
# checks() return a dict, like:
# { "result": True or False,  'step_result': [a list of each step return]
#
'''
2015-01-19 20:54:13,846 - INFO - To show the checks with options functions
2015-01-19 20:54:16,848 - INFO - ------------------------------------------------------
2015-01-19 20:54:16,848 - INFO - Func test_checks in file: /TestSteps/test_examples/test_lesson6_return.py
2015-01-19 20:54:16,848 - INFO - Check-1: my_add(3,4,5) == my_mul(3,4) -PASS- 12 == 12  - sleep 0 seconds (-d 3 set)
2015-01-19 20:54:16,849 - INFO - Check-2: my_add(3,4,6) == 12 -PASS- 13 == 12
2015-01-19 20:54:16,849 - WARNING -   ^^^  condition not met (pass due to -w option set)  ^^^
2015-01-19 20:54:17,850 - INFO - Check-3: my_mul(3,4,5) > 20 -PASS-   - Step Timeout (-t 1 set)
2015-01-19 20:54:17,850 - WARNING -   ^^^  condition not met (pass due to -w option set)  ^^^
2015-01-19 20:54:17,851 - DEBUG - {'step_results': [{'values': [12, 12], 'info': '12 == 12  - sleep 0 seconds (-d 3 set)', 'result': True, 'exception': None},
                                                    {'values': [13, 12], 'info': '13 == 12', 'result': True, 'exception': None},
                                                    {'values': [None], 'info': '  - Step Timeout (-t 1 set)', 'result': True, 'exception': None}],
                                   'result': True}
'''


if __name__ == '__main__':
    test_check()
    test_checks()
