
import re
import functools

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, state, offset, value='', datatype='char'):
        self.state = state
        self.offset = offset
        self.value = value
        self.datatype = datatype

    def __repr__(self):
        if len(self.state) < 20:
            return "State<'%s', %s>" % (self.state[:20], self.offset)
        else:
            return "State<'%s...', %s>" % (self.state[:20], self.offset)

    def peek(self, n):
        return self.state[self.offset:self.offset + n]

    def read(self, n):
        return Parser(self.state, self.offset + n)

    def incr_offset(self):
        self.offset = self.offset + 1
        return self

    def set_value(self, v):
        self.value = v
        return self

    def set_type(self, t):
        self.datatype = t
        return self

def parse(f, _bytes):
    if type(_bytes) == Parser:
        return f(_bytes)
    else:
        s = Parser(_bytes, 0)
        return f(s)

def char(rpattern, _bytes=False):
    def _char(parser):
        if re.match(rpattern, parser.peek(1)):
            return parser.read(1).set_value(parser.peek(1)).set_type('char')
        raise ParseError("Char: Error matching pattern, found '%s', expecting '%s'" % (parser.peek(1), rpattern))
    return _char

def word(word):
    def _word(parser):
        if parser.peek(len(word)) == word:
            return parser.read(len(word)).set_value(word).set_type('string')
        raise ParseError("Word: Error matching pattern, found '%s', expecting '%s'" % (parser.peek(len(word)), word))
    return _word

def many(f):
    def _many(parser):
        acc = []
        cur = parser
        for i in range(len(cur.state)):
            try:
                temp = f(cur)
                acc.append(temp.value)
                cur = temp
            except:
                break
        val = ''.join(acc)
        return cur.set_value(val)
    return _many

def sequence(fs, f = lambda x: x, _type='string'):
    def _sequence(parser):
        acc = []
        cur = parser
        for g in fs:
            temp = g(cur)
            acc.append(temp.value)
            cur = temp
        return cur.set_value(f(acc)).set_type(_type)
    return _sequence

def oneof(fs):
    def _oneof(parser):
        for f in fs:
            try:
                return f(parser)
            except:
                pass
        raise ParseError("Oneof: no pattern match found")
    return _oneof

def sepby(f, by):
    def _sepby(parser):
        acc = []
        cur = parser
        while len(cur.state) > 0:
            temp = f(cur)
            acc.append(temp)
            cur = temp
            
            try:
                temp = by(cur)
                cur = temp
            except:
                break

        return cur.set_value(acc).set_type('list')
    return _sepby

def anychar():
    def _anychar(parser):
        val = parser.state[0]
        return parser.read(1).set_value(val)
    return _anychar

def until(f):
    def _until(parser):
        cur = parser
        for i in range(len(parser.state)):
            try:
                temp = f(cur)
                return temp
            except:
                temp = anychar()(cur)
                cur = temp
        raise ParseError("Until: unable to find until pattern")
    return _until

def digit(): return char('[0-9]')

def alphanum(): return char('[0-9a-zA-Z]')

def space(): return char('[ ]')

def spaces(): return many(space())

def newline(): return char('\n')

def integer(): 
    def _integer(parser):
        d = many(digit())(parser)
        return d.set_value(int(d.value)).set_type('integer')
    return _integer

def scientific():
    def _float(parser):
        return sequence([many(digit()), char('.'), many(digit())], lambda xs: float(xs[0] + xs[1] + xs[2]))(parser)
    return _float



