__author__ = 'Steven LI'


from test_steps import *

## The example to test return value - enhancement in 0.7.1 to fix issue#20
## When a function return 0 or None, it will be treated as pass(True),
##     to be consistent with the Linux command exit code (0 as successful).
##

def simple_fun_return0():
    return 0

def simple_fun_noReturn():
    pass

def test_returnvalue0():
    ok(simple_fun_return0(), "return 0 means pass")
    check("simple_fun_return0()", duration=2)
    eq(simple_fun_return0(), 0)
    check("simple_fun_return0() == 5", duration=2, warning=True)


def test_noReturn():
    ok(simple_fun_noReturn(), "noReturn means pass")
    check("simple_fun_noReturn()", duration=2)
    eq(simple_fun_noReturn(), None)
    check("simple_fun_noReturn() == None", duration=2, warning=True)
    check("simple_fun_noReturn() == 0", duration=2, warning=True)

##############################################################################
## This log might not be what you want to see
##  because it logged checks into different functions, it looks a mess
## This is because the test_steps module auto detect the function which call check functions
##  and for a new function, it will re-count the check.
'''
INFO - ------------------------------------------------------
INFO - Func test_returnvalue0 in file: /Users/Steven/PycharmProjects/TestSteps/test_examples/test_lesson7_returnvalue.py
INFO - Check-1: return 0 means pass -PASS-
INFO - Check-2: simple_fun_return0() -PASS- 0  - sleep 1 seconds (-d 2 set)
INFO - Check-3: 0 == 0 -PASS- 0 == 0?
INFO - Check-4: simple_fun_return0() == 5 -PASS- 0 == 5  - sleep 1 seconds (-d 2 set)
WARNING -   ^^^  condition not met (pass due to -w option set)  ^^^
INFO - ------------------------------------------------------
INFO - Func test_noReturn in file: /Users/Steven/PycharmProjects/TestSteps/test_examples/test_lesson7_returnvalue.py
INFO - Check-1: noReturn means pass -PASS-
INFO - Check-2: simple_fun_noReturn() -PASS- None  - sleep 1 seconds (-d 2 set)
INFO - Check-3: None == None -PASS- None == None?
INFO - Check-4: simple_fun_noReturn() == None -PASS- None == None  - sleep 1 seconds (-d 2 set)
INFO - Check-5: simple_fun_noReturn() == 0 -PASS- None == 0  - sleep 1 seconds (-d 2 set)
WARNING -   ^^^  condition not met (pass due to -w option set)  ^^^
'''




if __name__ == '__main__' :
    test_returnvalue0()
    test_noReturn()

