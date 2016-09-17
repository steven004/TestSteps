#from testbed.yaml_testbed import init_testbed
from test_steps import ok, eq, ne, init_testbed

tb_m = init_testbed("lesson8_testbed_obj.yaml")

def test_no_param():
    ok(tb_m)
    print(tb_m)
    print(tb_m.obj1)
    ok(tb_m.obj1)
    ok(tb_m.obj1.ppp())

def test_with_param_in_func():
    #tb_m = init_testbed("lesson8_testbed_obj.yaml")
    eq(tb_m.obj1.ppp2(3,5), 8)
    ne(tb_m.obj1.ppp2(100,20), 102)
    eq(tb_m.obj1.ppp2(4,6,10), 20)

def test_with_param_in_class():
    eq(tb_m.obj2.get_value(), 17)
    eq(tb_m.obj2.multiple(10), 170)
    eq(tb_m.obj2.get_value(), 170)

def test_with_paramoption_in_class():
    eq(tb_m.obj3.get_msg(), 'Goodafternoon')
    eq(tb_m.obj4.get_msg(), 'Goodqq')

def test_with_index_file():
    eq(tb_m.obj5.get_value(), 22)
    eq(tb_m.obj6.get_value(), 17)
    eq(tb_m.obj6.get_msg(), 'Goodafternoon')
    eq(tb_m.obj6.multiple(10), 170)


if __name__ == '__main__':
    test_no_param()
    test_with_param_in_func()
    test_with_param_in_class()
    test_with_paramoption_in_class()
    test_with_index_file()

