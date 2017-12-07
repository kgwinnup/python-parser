import pytest
import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
from core.parser import *

def test_parse_char():
    ret = parse(char('a'), 'abcde')
    assert ret.value == 'a'

def test_parse_word():
    ret = parse(word('hello'), 'hello world abcde')
    assert ret.value == 'hello'

def test_parse_many():
    ret = parse(many(char('a')), 'aaahello world')
    assert ret.value == 'aaa'

def test_parse_digit():
    ret = parse(digit(), '1235asdfasdf')
    assert ret.value == '1'

def test_parse_many_digit():
    ret = parse(many(digit()), '10aaahello world')
    assert ret.value == '10'

def test_parse_integer():
    ret = parse(integer(), '10aaahello world')
    assert ret.value == 10

def test_parse_sequence():
    ret = parse(sequence([integer(), word('hello'), integer()], lambda xs: xs[1]), '10hello22 adsasdf')
    assert ret.value == 'hello'

def test_parse_oneof():
    ret = parse(oneof([char('a'), integer()]), '20 asdfasdf')
    assert ret.value == 20

def test_parse_sepby():
    ret = parse(sepby(digit(), char(',')), '1,2,3,4,5 adfaf')
    assert len(ret.value) == 5

def test_parse_alphanum():
    ret = parse(alphanum(), 'adf10aaahello world')
    assert ret.value == 'a'
    ret = parse(alphanum(), '10aaahello world')
    assert ret.value == '1'
    ret = parse(alphanum(), 'Z10aaahello world')
    assert ret.value == 'Z'

def test_parse_spaces():
    ret = parse(spaces(), '      hello ')
    assert ret.value == '      '
    ret2 = parse(word('hello'), ret)
    assert ret2.value == 'hello'

def test_parse_scientific():
    ret = parse(scientific(), '10.0001 adfasdf')
    assert ret.value == 10.0001

def test_parse_until():
    ret = parse(until(char(':')), 'hello:world')
    assert ret.offset == 6

def test_parse_any():
    ret = parse(anychar(), 'adsfasdf')
    assert ret.value == 'a'

