__author__ = 'Steven LI'

from test_steps import *


def wait():
    import time

    time.sleep(5)
    return True


def test_1():
    eq(3 + 5, 8, "3+5 equals 8")
    ok("ok step")
    ok(3, "3 should pass")
    unmatch("shanghai", "beijing", "to see if shanghai is not beijing")

    test_logger.debug("The following step should fail. -- an example to use test_logger")
    match("Shanghai", "Beijing", "to see if shanghai is Beijing")
    # ok(5>6, "5>6?")
    #eq("sdf", "dsaf")
    gt(3.555, 3.222)
    lt(2.333, 435)
    le("34", "56", "34<56 ma... ")


def test_2():
    eq(3 + 5, 8)
    ok("ok step")
    ok(3, "3 should pass")
    unmatch("shanghai", "beijing", "to see if shanghai is not beijing")
    # match("Shanghai", "Beijing", "to see if shanghai is Beijing")
    #ok(5>6, "5>6?")
    #eq("sdf", "dsaf")
    gt(3.555, 3.222)
    lt(2.333, 435)
    le("34", "56", "34<56 ma... ")
    ge(55, 55)
    fail("anything")


def test_3step():
    step("'ok'> '5'", passdesc='OK > 5 should pass', faildesc='this should not be printed')
    # step("3 == 5")
    step("wait()", timeout=6, xfail=True, warning=True)
    step("3+6 == 9", duration=4)
    step("4 == 6", skip=True, duration=10, warning=True)
    step("abs(4-3) == 5", faildesc='abs(4-3) not equals 5')
    step("4 == 5", repeat=3, warning=True)


def test_4steps():
    steps("""
        'ok'> '5'
        3+6 == 9  -d 4
        3 == 5 -w
        4 == 6  -x
        abs(4-3) == 5
        9 > 0/0  -e ZeroDivisionError
        9 < 0/0  -e Exception
        9 == 0/0 -e SyntaxError
        4 == 5  --repeat 3
        """, batch=True)


def test_5steps():
    ret = steps("""
        'ok'> '5'
        3+6 == 9  -d 4
        3 == 5 -w
        4 == 6  -x
        abs(4-3) == 1
        9 > 0/0  -e ZeroDivisionError
        9 < 0/0  -e Exception
        """, batch=True)

    print(ret)


if __name__ == '__main__':
    # test_1()
    #test_2()
    #test_3step()
    test_5steps()
