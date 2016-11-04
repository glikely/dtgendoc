#!/usr/bin/env python3
#
# Code for working with devicetree schemas
#
# These functions implement a subset of functionality for working with
# devicetree schema files.
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
from voluptuous import Schema, Match, Email
from email.utils import parseaddr
import yaml
from pprint import pprint


# Grammer

def NameEmail(v):
    name, addr = parseaddr(v)
    s = Schema({'name':str, 'addr': Email()})
    s({'name': name, 'addr': addr})
    return v

# This is the schema for DT Schema files
schema = Schema({
	'id': str,
	'version': int,
	'title': str,
	'maintainers': [NameEmail],
	'types': [],
	'match': [],
	'schema': [],
	'doc': str,
})

test_schema = '''
%YAML 1.2
---
version: 1
id: schema-testing-acme-toaster
title: DT Schema unittest data
maintainers:
- Jill Doe <jill@nowhere-but-here.com>
- jill@nowhere-but-here.com

doc: >
  This describes a binding for a non-existent device

types:
- cell
- phandle
- string

match:
- compatible = string-list(contains="acme,toaster-1.0");

schema:
- property: spi-cs-high
  value: empty
  doc: >
    Set if skeleton device configuration pins are set for
    chip select polarity high

- property: spi-
'''


# Unittests
if __name__ == "__main__":
	s = yaml.load(test_schema)
	pprint(s)
	schema(s)
