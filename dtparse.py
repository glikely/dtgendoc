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


# Test code to parse DTS Format
def parse_dts(string):
    byteexpr = Word(alphanums).setParseAction(lambda s,l,t: [int(t[0],base=16)])
    byteexpr = nestedExpr('[', ']', byteexpr)
    byteexpr.setParseAction(lambda s,l,t: [ pack('!%iB'%len(t[0]), *t[0]) ])

    cellexpr = Word(alphanums).setParseAction(lambda s,l,t: [int(t[0],base=0)])
    cellexpr = nestedExpr('<', '>', cellexpr)
    cellexpr.setParseAction(lambda s,l,t: [ pack('!%iI'%len(t[0]), *t[0]) ])

    strexpr = QuotedString(quoteChar='"', escChar='\\', escQuote='\\\\')
    strexpr.setParseAction(lambda s,l,t: [ t[0].encode() + b'\0' ])

    expr = OneOrMore (byteexpr | cellexpr | strexpr)
    expr.setParseAction(lambda s,l,t: [ b''.join(t) ])
    return expr.parseString(string)[0]

if __name__ == "__main__":
    tests = [
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

    class TestSequence(unittest.TestCase):
        pass

    def generate_test(dts_prop, dtb_prop):
        def test(self):
            self.assertEqual(parse_dts(dts_prop), dtb_prop)
        return test

    for t in tests:
        setattr(TestSequence, "test_"+t[0], generate_test(t[1], t[2]))
    unittest.main()


