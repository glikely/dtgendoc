#!/usr/bin/python
 
# Copyright 2015 Konsulko Group, Matt Porter <mporter@konsulko.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

import string
import sys
import yaml

def gen_md(doc):
	# Title is mandatory
	print "# " + doc["title"]

	# Description is optional (shouldn't be, but many bindings don't have
	# one now)
	if "description" in doc:
		print doc["description"]

	# Compatible strings are optional, and many may exist
	if "compatible" in doc:
		print "## Compatible Strings"
		for c in doc["compatible"]:
			if "name" in c:
				tname = c["name"].replace("<", "\<")
				compatible = tname.replace(">", "\>")
			elif "deprecated" in c:
				tname = c["deprecated"].replace("<", "\<")
				compatible = tname.replace(">", "\>") + " - DEPRECATED"
			sys.stdout.write("* **" + '{}'.format(compatible) + "**")
			if c.get("description"):
				print(" - " + '{}'.format(c["description"]))
			else:
				print
		print

	# Each property category is optional, so check before outputing a
	# heading.

	if "required" in doc:
		print "## Required Properties"
		for prop in doc["required"]:
			print("* **" + '{}'.format(prop["name"]) + "** - " + '{}'.format(prop["description"]))
			print
			if "reference" in prop:
				ref = prop["reference"]
				sys.stdout.write("    *Refer to [" + '{}'.format(ref) +"](" + '{}'.format(ref) + ") for more information.*\n")
		print

	if "optional" in doc:
		print "## Optional Properties"
		for prop in doc["optional"]:
			print("* **" + '{}'.format(prop["name"]) + "** - " + '{}'.format(prop["description"]))
			print
			if "reference" in prop:
				ref = prop["reference"]
				sys.stdout.write("    *Refer to [" + '{}'.format(ref) +"](" + '{}'.format(ref) + ") for more information.*\n")
		print

	if "deprecated" in doc:
		print "## Deprecated Properties"
		for prop in doc["deprecated"]:
			print("* **" + '{}'.format(prop["name"]) + "** - " + '{}'.format(prop["description"]))
			print
			if "reference" in prop:
				ref = prop["reference"]
				sys.stdout.write("    *Refer to [" + '{}'.format(ref) +"](" + '{}'.format(ref) + ") for more information.*\n")
		print

	# At least one example is required, but support multiple
	print "## Example"
	for e in doc["example"]:
		if "description" in e:
			print e["description"]
		print
		print "```"
		print e["dts"]
		print "```"
	print

	# Maintainer is optional (it might someday become required, but for now
	# this is based on the MAINTAINERS entry where that works most of the
	# time)
	if "maintainer" in doc:
		print "## Maintainer"
		for m in doc["maintainer"]:
			print("*" + '{}'.format(m["name"]) + "*")
		print

with open(sys.argv[1], 'r') if len(sys.argv) > 1 else sys.stdin as f:
	for doc in yaml.load_all(f):
		gen_md(doc)
