__author__ = 'Steven LI'


from test_steps import *

## This is just an example, to create an operator to judge is two data strings stand for the same date
## i.e. '1/4/2015' =d= '01-04-2015' is true
## desc parameter can be omitted here, but can be used later in cases
def compDate(date1, date2):
    import re
    pattern = re.compile(r'^(\d+).(\d+).(\d+)$')
    match1 = pattern.match(date1)
    match2 = pattern.match(date2)
    day1, month1, year1 = (int(i) for i in match1.group(1,2,3))
    day2, month2, year2 = (int(i) for i in match2.group(1,2,3))
    ok((year1==year2) and (month1==month2) and (day1==day2),
       passdesc = '%s =d= %s'%(date1, date2),
       faildesc = '%s =!d= %s'%(date1, date2) )


def test_date():
    eq(3+5, 8)
    compDate('11/4/2015', '11-04-2015')
    ok("ok step")
    ok(3, "3 should pass")
    compDate('12/4/2014', '12-04/2015')

##############################################################################
## This log might not be what you want to see
##  because it logged checks into different functions, it looks a mess
## This is because the test_steps module auto detect the function which call check functions
##  and for a new function, it will re-count the check.
'''
Steven:tmp $ cat test_20150121_2049.log 
2015-01-21 20:49:07,917 - INFO - ------------------------------------------------------
2015-01-21 20:49:07,917 - INFO - Func test_date in file: /TestSteps/test_examples/test_lesson6_func_auto_check.py
2015-01-21 20:49:07,917 - INFO - Check-1: 8 == 8 -PASS- 8 == 8?
2015-01-21 20:49:07,918 - INFO - ------------------------------------------------------
2015-01-21 20:49:07,918 - INFO - Func compDate in file: /Users/xili4/PycharmProjects/TestSteps/test_examples/test_lesson6_func_auto_check.py
2015-01-21 20:49:07,918 - INFO - Check-1: 11/4/2015 =d= 11-04-2015 -PASS- 
2015-01-21 20:49:07,918 - INFO - ------------------------------------------------------
2015-01-21 20:49:07,918 - INFO - Func test_date in file: /Users/xili4/PycharmProjects/TestSteps/test_examples/test_lesson6_func_auto_check.py
2015-01-21 20:49:07,918 - INFO - Check-1: ok step -PASS- 
2015-01-21 20:49:07,918 - INFO - Check-2: 3 should pass -PASS- 
2015-01-21 20:49:07,918 - INFO - ------------------------------------------------------
2015-01-21 20:49:07,919 - INFO - Func compDate in file: /Users/xili4/PycharmProjects/TestSteps/test_examples/test_lesson6_func_auto_check.py
2015-01-21 20:49:07,919 - ERROR - Check-1: 12/4/2014 =!d= 12-04/2015 -FAIL- 
'''


###################### How to make it better ######################################
# a local variable is introduced to disable auto-function-detection
# Example: rewrite the compDate functions by setting __auto_func_detection__ = False
def compDate2(date1, date2):
    __auto_func_detection__ = False        # set it to false
    import re
    pattern = re.compile(r'^(\d+).(\d+).(\d+)$')
    match1 = pattern.match(date1)
    match2 = pattern.match(date2)
    day1, month1, year1 = (int(i) for i in match1.group(1,2,3))
    day2, month2, year2 = (int(i) for i in match2.group(1,2,3))
    ok((year1==year2) and (month1==month2) and (day1==day2),
       passdesc = '%s =d= %s'%(date1, date2),
       faildesc = '%s !=d= %s'%(date1, date2) )



def test_date2():
    eq(3+5, 8)
    compDate2('11/4/2015', '11-04-2015')
    ok("ok step")
    ok(3, "3 should pass")
    compDate2('12/4/2014', '12-04/2015')

#################################################################################
# Now the log is what you want. 
#
'''
2015-01-21 21:15:44,360 - INFO - Func test_date2 in file: /TestSteps/test_examples/test_lesson6_func_auto_check.py
2015-01-21 21:15:44,361 - INFO - Check-1: 8 == 8 -PASS- 8 == 8?
2015-01-21 21:15:44,361 - INFO - Check-2: 11/4/2015 =d= 11-04-2015 -PASS- 
2015-01-21 21:15:44,361 - INFO - Check-3: ok step -PASS- 
2015-01-21 21:15:44,361 - INFO - Check-4: 3 should pass -PASS- 
2015-01-21 21:15:44,361 - ERROR - Check-5: 12/4/2014 =!d= 12-04/2015 -FAIL- 
'''


if __name__ == '__main__' :
    test_date()
    test_date2()

