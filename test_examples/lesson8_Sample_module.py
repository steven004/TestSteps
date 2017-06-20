### This is just for test

class something(object):
    def __init__(self):
        pass

    def ppp(self):
        print("Great, you can see this now, in ppp function")

    def ppp2(self, x, y, z=0):
        return x+y+z

class something2(object):
    def __init__(self, mm, nn, oo, pp='pp', qq='qq'):
        self.value = mm + nn + oo
        self.msg = pp + qq

    def get_value(self):
        return self.value

    def multiple(self, kk):
        self.value *= kk
        return self.value

    def get_msg(self):
        return self.msg


class something3():
    value = 0
    def get_value(self):
        self.value += 1
        return self.value
