

class X(object):
    a = ''
    b = ''

    def __init__(self, d):
        self.__dict__ = d

    def __getattr__(self, name):
        if name in self:
            return self[name]

    # def __setattr__(self, name, value):
    #     self[name] = value

tt = {'a': 'aaaa', 'b': 'bbbbb'}
x = X(tt)
print x.a
x['a'] = 'lala'
print x.a
