import pytest
import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
from pyparser import *

def test_parse_char():
    ret = parse(char('a'), 'abcde')
    assert ret._value == 'a'

def test_parse_specialchars():
    ret = parse(char('/'), '/asdf.')
    assert ret._value == '/'

def test_parse_word():
    ret = parse(word('hello'), 'hello world abcde')
    assert ret._value == 'hello'

def test_parse_many():
    ret = parse(many(char('a')), 'aaahello world')
    assert ret._value == 'aaa'
    assert ret._offset == 3

def test_parse_digit():
    ret = parse(digit(), '1235asdfasdf')
    assert ret._value == '1'

def test_parse_many_digit():
    ret = parse(many(digit()), '10aaahello world')
    assert ret._value == '10'

def test_parse_integer():
    ret = parse(integer(), '10aaahello world')
    assert ret._value == 10

def test_parse_sequence():
    ret = parse(sequence(integer(), word('hello'), integer()), '10hello22 adsasdf')
    assert ret._value[0] == 10
    assert ret._value[1] == 'hello'
    assert ret._offset == 9

def test_parse_oneof():
    ret = parse(oneof(char('a'), integer()), '20 asdfasdf')
    assert ret._value == 20

def test_parse_sepby():
    ret = parse(sepby(digit(), char(',')), '1,2,3,4,5 adfaf')
    assert len(ret._value) == 5
    ret = parse(sepby(integer(), char(',')), '1,2,3,4,5')
    assert len(ret._value) == 5
    assert ret._value[0]._value == 1
    assert ret._value[4]._value == 5
    ret = parse(sepby(word('hello'), spaces()), "hello hello      hello")
    assert len(ret._value) == 3

def test_parse_alphanum():
    ret = parse(alphanum(), 'adf10aaahello world')
    assert ret._value == 'a'
    ret = parse(alphanum(), '10aaahello world')
    assert ret._value == '1'
    ret = parse(alphanum(), 'Z10aaahello world')
    assert ret._value == 'Z'

def test_parse_manyalphanum():
    ret = parse(many(alphanum()), 'afwefd adfqwef adfs')
    assert ret._value == 'afwefd'
    assert ret._offset == 6

def test_parse_spaces():
    ret = parse(spaces(), '      hello ')
    assert ret._value == '      '
    ret2 = parse(word('hello'), ret)
    assert ret2._value == 'hello'

def test_parse_spaces1():
    ret = parse(spaces1(), '   adsafds')
    print(ret)
    assert ret._offset == 3
    ret = parse(spaces1(), 'adsafds')
    assert ret._offset == 0

def test_parse_scientific():
    ret = parse(scientific(), '10.0001 adfasdf')
    assert ret._value == 10.0001

def test_parse_until():
    ret = parse(skip_till(char(':')), 'hello:world')
    assert ret._offset == 6

def test_parse_any():
    ret = parse(anychar(), 'adsfasdf')
    assert ret._value == 'a'
    ret = parse(anychar(), '\nadf')
    assert ret._value == '\n'

def test_parse_optional():
    ret = parse(optional(integer()), 'asdf')
    assert ret._offset == 0
    ret = parse(optional(integer()), '100asdf')
    assert ret._offset == 3
    assert ret._value == 100

def test_many_till():
    ret = parse(many_till(alphanum(), char('\n'), _type='string'), 'aaaaaa\nBBBBB')
    assert ret._value == 'aaaaaa'
    assert ret._offset == 7

def test_many_oneof():
    ret = parse(many(oneof(char('/'), alphanum())), '///xx/bbb.py adf')
    assert ret._value == '///xx/bbb'

def test_many_seq():
    ret = parse(sequence(word('hello'),
        spaces1(),
        many(oneof(char('/'), alphanum(), char('.'))),
        spaces1()), 'hello      aa/bb  ')
    assert ret._value[0] == 'hello'
    assert ret._value[2] == 'aa/bb'

def test_many_n():
    ret = parse(manyN(3, alphanum()), 'abcdefg')
    assert ret._value == ['a', 'b', 'c']
