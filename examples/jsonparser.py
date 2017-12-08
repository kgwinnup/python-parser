
from pyparser import *

def jstring():
    return sequence1(1, char('"'), many(oneof(alphanum())), char('"'))

def jbool(): 
    return oneof(word('true'), word('True'), word('False'), word('false'), _type='bool')

def jnumber():
    return oneof(integer(), scientific())

def jlist():
    return sequence1(1, char('\['), sepby(oneof(jstring(), jbool(), jnumber()), sequence(spaces1(), char(','), spaces1())), char(']'))

def jkey():
    return oneof(jstring(), jnumber(), jbool())

def jpair():
    def _jobject():
        return sequence1(2, char('{'), spaces1(), sepby(_jpair(), sequence(spaces1(), char(','), spaces1())), spaces1(), char('}'))

    def _jpair():
        return sequence2(0,4, jkey(), spaces1(), char(':'), spaces1(), jkey(), type='jpair')

    return sequence2(0,4, jkey(), spaces1(), char(':'), spaces1(), oneof(jstring(), jbool(), jlist(), _jobject()), type='jpair')

def jobject():
    return sequence1(2, char('{'),
                        spaces1(),
                        sepby(jpair(), sequence(spaces1(), char(','), spaces1())),
                        spaces1(),
                        char('}'))

if __name__ == '__main__':
    ret = parse(jstring(), '"hello": "world"')
    print(ret)
    ret = parse(jbool(), "True adfadf")
    print(ret)
    ret = parse(jlist(), '["hello", "world", "yo"]')
    print(ret)
    ret = parse(jobject(), '{"hello": "world", "foo": "bar", "zoo": "boo", "dude": {"yo": "man"}}')
    print(ret)

