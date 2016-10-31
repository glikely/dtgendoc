#!/usr/bin/env python3
#
# Code for working with devicetree data
#
# These functions implement a subset of functionality for working with
# devicetree files.
#
# Copyright (C) 2016 Grant C. Likely
#
# SPDX-License-Identifier: GPL-2.0
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import unittest
from pyparsing import *
from struct import pack


# Grammer

# Property value expressions
propbyte = Word(alphanums).setParseAction(lambda s,l,t: [int(t[0],base=16)])
propbyte = nestedExpr('[', ']', propbyte)
propbyte.setParseAction(lambda s,l,t: [ pack('!%iB'%len(t[0]), *t[0]) ])

propcell = Word(alphanums).setParseAction(lambda s,l,t: [int(t[0],base=0)])
propcell = nestedExpr('<', '>', propcell)
propcell.setParseAction(lambda s,l,t: [ pack('!%iI'%len(t[0]), *t[0]) ])

propstr = QuotedString(quoteChar='"', escChar='\\', escQuote='\\\\')
propstr.setParseAction(lambda s,l,t: [ t[0].encode() + b'\0' ])

propval = OneOrMore (propbyte | propcell | propstr)
propval.setParseAction(lambda s,l,t: [ b''.join(t) ])
propval.setResultsName("val")

propnodename = Word(alphanums+",._+*#?@-").setResultsName("name")

label = Combine(Word(alphas+'_') + Optional(Word(alphanums+'_')) + Suppress(':'))
label.setResultsName("label")

prop = Group(ZeroOrMore(label) + propnodename + Optional(Suppress('=') + propval) + Suppress(';'))

node = Forward()
nodebody = nestedExpr('{', '}', node | prop)
node <<= ZeroOrMore(label) + propnodename + nodebody + Suppress(';')
rootnode = '/' + nodebody + Suppress(';')


# Unittests
if __name__ == "__main__":
    import pprint

    propvaltests = [
        ['str0', '""', b'\0'],
        ['str1', '"abcdefg"', b'abcdefg\0'],
        ['bytes0', '[ ]', b''],
        ['bytes1', '[ 00 01 ff fe 0 ]', b'\x00\x01\xff\xfe\x00'],
        ['bytes2', '[ 33 ]', b'\x33'],
        ['bytes3', '[ff]', b'\xff'],
        ['bytes4', '[ aa ] [ab cd ef 01][93]', b'\xaa\xab\xcd\xef\x01\x93'],
        ['cells0', '< >', b''],
        ['cells1', '< 0 >', b'\0\0\0\0'],
        ['cells2', '< 0xff 0x11 0x22 0x33 0x44 >',
                   b'\0\0\0\xff\0\0\0\x11\0\0\0\x22\0\0\0\x33\0\0\0\x44'],
        ['cells3', '< 100 0xABCDEF12><0x29342 2341 >',
                   b'\0\0\0\x64\xab\xcd\xef\x12\0\2\x93\x42\0\0\x09\x25'],
        ['mixed0', '<>[]""""[]<>', b'\0\0'],
        ['mixed1', '"test" <256>', b'test\0\0\0\1\0'],
    ]

    proptests = [
    ]

    test_dts = '''
    / {
        #address-cells = <1>;
        #size-cells = <1>;
        compatible = "acme,fancy1";
        cpus {
            #address-cells = <1>;
            #size-cells = <1>;
            cpu@0 { reg = <0>; };
            cpu@1 { reg = <1>; };
            cpu@2 { reg = <2>; };
            cpu@3 { reg = <3>; };
        };
    };
    '''

    class TestSequence(unittest.TestCase):
        def test_fulldts(self):
            tree = rootnode.parseString(test_dts)
            print(tree)

    def generate_test(dts_prop, dtb_prop):
        def test(self):
            self.assertEqual(propval.parseString(dts_prop)[0], dtb_prop)
        return test

    for t in propvaltests:
        setattr(TestSequence, "test_propval_"+t[0], generate_test(t[1], t[2]))
    unittest.main()
