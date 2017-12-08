
import re

class ParseError(Exception):
    pass

class Parser:
    """
    Parser class, this object holds all data related to parsing, including the
    _state, _offset and after a combinator is parsed, the _value and _datatype
    """
    def __init__(self, _state, _offset, _value=None, _datatype=None):
        self._state = _state
        self._offset = _offset
        self._value = _value
        self._datatype = _datatype

    def __repr__(self):
        return "Parser<'%s', '%s'>" % (self._datatype, self._value)

    def peek(self, n):
        return self._state[self._offset:self._offset + n]

    def read(self, n, _type='string'):
        return Parser(self._state, self._offset + n, self._state[self._offset:self._offset + n], _type)

    def set_value(self, v):
        self._value = v
        return self

    def set_type(self, t):
        self._datatype = t
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
            return parser.read(1)
        raise ParseError("Char: Error matching pattern, found '%s', expecting '%s'" % (parser.peek(1), rpattern))
    return _char

def word(word):
    def _word(parser):
        if parser.peek(len(word)) == word:
            return parser.read(len(word))
        raise ParseError("Word: Error matching pattern, found '%s', expecting '%s', _offset %s" % (parser.peek(len(word)), word, parser._offset))
    return _word

def many(f, _type='string'):
    def _many(parser):
        acc = []
        cur = parser
        for i in range(len(cur._state)):
            try:
                temp = f(cur)
                acc.append(temp._value)
                cur = temp
            except:
                break
        val = ''.join(acc)
        return Parser(cur._state, cur._offset, val, _type)
    return _many

def sequence(*fs, **kwargs):
    def _sequence(parser):
        acc = []
        cur = parser
        for f in fs:
            temp = f(cur)
            acc.append(temp._value)
            cur = temp
        return Parser(cur._state, cur._offset, acc, kwargs['type'] if 'type' in kwargs else 'list')
    return _sequence

def sequence1(index, *fs, **kwargs):
    def _sequence1(parser):
        temp = sequence(*fs, **kwargs)(parser)
        return temp.set_value(temp._value[index])
    return _sequence1

def sequence2(index, index2, *fs, **kwargs):
    def _sequence1(parser):
        temp = sequence(*fs, **kwargs)(parser)
        return temp.set_value((temp._value[index], temp._value[index2]))
    return _sequence1


def oneof(*fs, _type='string'):
    def _oneof(parser):
        for f in fs:
            try:
                temp = f(parser)
                return Parser(temp._state, temp._offset, temp._value, _type)
            except:
                pass
        raise ParseError("Oneof: no pattern match found")
    return _oneof

def sepby(f, by):
    def _sepby(parser):
        acc = []
        cur = parser
        while True:
            try:
                temp = f(cur)
                acc.append(temp)
                cur = temp
            except:
                break
                
            try:
                temp = by(cur)
                cur = temp
            except:
                break

        return Parser(cur._state, cur._offset, acc, 'list')
    return _sepby

def anychar():
    def _anychar(parser):
        val = parser._state[0]
        return parser.read(1).set_value(val)
    return _anychar

def skip_until(f):
    def _until(parser):
        cur = parser
        for i in range(len(parser._state)):
            try:
                temp = f(cur)
                return temp
            except:
                temp = anychar()(cur)
                cur = temp
        raise ParseError("Until: unable to find until pattern")
    return _until

def optional(f):
    def _optional(parser):
        try:
            return f(parser)
        except:
            return parser
    return _optional

def digit(): return char('[0-9]')

def alphanum(): return char('[0-9a-zA-Z]')

def space(): return char('[ ]')

def spaces(): return many(space())

def spaces1(): 
    def _spaces1(parser):
        try:
            return spaces()(parser)
        except:
            return parser
    return _spaces1

def newline(): return char('\n')

def integer(): 
    def _integer(parser):
        d = many(digit())(parser)
        return d.set_value(int(d._value)).set_type('integer')
    return _integer

def scientific():
    def _float(parser):
        temp = sequence(many(digit()), char('.'), many(digit()))(parser)
        val = float(temp._value[0] + temp._value[1] + temp._value[2])
        return Parser(temp._state, temp._offset, val, 'float')
    return _float



