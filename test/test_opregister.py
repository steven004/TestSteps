
__author__ = 'Steven LI'


from test_steps import *

## This is just an example, to create an operator to judge is two data strings stand for the same date
## i.e. '1/4/2015' =d= '01-04-2015' is true
## desc parameter can be omitted here, but can be used later in cases
def compDate(date1, date2):
    import re
    pattern = re.compile(r'(\d+).(\d+).(\d+)')
    match1 = pattern.match(date1)
    match2 = pattern.match(date2)
    day1, month1, year1 = (int(i) for i in match1.group(1,2,3))
    day2, month2, year2 = (int(i) for i in match2.group(1,2,3))
    return (year1==year2) and (month1==month2) and (day1==day2)

def setup():
    global sameDate, feq
    addBiOperator('=d=', compDate)
    sameDate = getOpWrapper('=d=')

    # add one more operator =f= to compare two float numbers
    addBiOperator('=f=', lambda o1, o2: abs(o1 - o2) < 1.0e-6)
    feq = getOpWrapper('=f=')

def test_3():
    eq(3+5, 8)
    ok("ok step")
    ok(3, "3 should pass")
    sameDate('1/4/2015', '01-04-2015', "the same date: Jan. 04 2015")

def test_4():
    eq(3+5, 8)
    ok("ok step")
    ok(3, "3 should pass")
    sameDate('11/4/2015', '1-04-2015', "Different date, should fail")

if __name__ == '__main__' :
    setup()
    test_3()
    test_4()
