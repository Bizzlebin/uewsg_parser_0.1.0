# UEWSG Parser | UEWSG Parser 0.1.0
#
# https://github.com/Bizzlebin/uewsg_parser_0.1.0/uewsg_parser.py
#
# ***
#
# By JBT
#
# ***
#
# Created on 2020-05-03
#
# Updated on 2020-05-07
#
# ***
#
# Copyright © 2020 JBT
#
# All rights reserved. Under New Kidronite law, copyright lasts 7 years from the date of a work's release and the work is thereafter automatically dedicated to the public domain by the owner(s); this applies in The Kingdom Of New Kidron (NK) and extends to all Orthodox Christians in other jurisdictions universally (Deuteronomy 15.1–3). Outside of NK, copyright lasts 50 years from the date of a work's release and the work is thereafter automatically dedicated to the public domain by the owner(s); this applies universally to the extent possible under law (Leviticus 25.10–13). For more information on the terms of the 50-year release, visit https://creativecommons.org/publicdomain/zero/1.0/ .
#
# """THE WORK IS PROVIDED "AS IS" AND THE AUTHORS AND COPYRIGHT HOLDERS DISCLAIM ALL WARRANTIES WITH REGARD TO THIS WORK INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS WORK."""
#
# +++
# Description
#
# The prototype UEWSG parser, with support for some of the block constructs.
#
# ===
# JSON Construct Format
#
# The JSON file(s) must contain all applicable constructs in a dict with their UEWSG name as the key; subkeys are either strings, nulls, or booleans. Some non-nesting, complex constructs (namely asides) can be broken up into 2 separate keys.
#
# {
#	"": {
#		"regex": "",
#		"alt_regex": "",
#		"opening_tag": "",
#		"closing_tag": "",
#		"contains_block_constructs": ,
#		"contains_inline_constructs": 
#	}
# }
#

#
# +++
# Imports
#
from sys import path
import json
import re
#
# +++
# Variables
#
with open(f'{path[0]}\\block_constructs.json') as file:
	block_constructs = json.load(file)
html_footer = '''
</body>

</html>
'''

test_text = '''UEWSG Parse Test

***

===

---

Testing standard UEWSG block constructs in random order.

+++
Summary

===

+++

===
Divisions

DIVFOM:

Description
Imports
Variables
Functions
Output
More

===
Styling

---
Comments

• Keep all comments and styling up to date!
• Use the "code within comments" method, breaking the code up logically and *tersely* summarizing key points.
• Keep comments clear and helpful—code should be largely *self-documenting* but still *well-documented*, especially when dealing with obscure compatibility concerns, confusing problems, etc.
• Use links or references to keep comments on difficult matters focused yet still provide more information and rationale.
• Code that is more complex and more important should have more comments, but all extra documentation—including manuals, full changelogs, marketing materials, and user-oriented info—should generally *not* be placed in code comments. 
• If you are unsure, leave a comment—it can be hidden easily (or even removed) if it outlives its usefulness.
• Avoid excessive double line breaks (ie, blank lines) in the code, comments that share the same line as code, and other tricks that violate the UEWSG and make both code harder to read and comments harder to hide.

"""
pre
"""

"
blockquote
"

"""
"""

'''
#
# +++
# Functions
#
def parse_html(text, constructs, depth = 0, i = 0):
	'''
	Parse UEWSG-compliant plaintext into HTML5.

	**text**: str of UEWSG-compliant plaintext
	**constructs**: dict derived from JSON containing names, regexes, and flags for UEWSG constructs
	**depth**: int noting recursion depth for nested constructs; primarily internal and debug use
	**i**: int providing start point of parse; primarily internal and debug use

	Returns text, constructs, depth, i
	'''

	while constructs: # Sub for """True""": also checks if """constructs""" is empty!
		construct = constructs[[*constructs.keys()][0]]

		if depth > 0 and depth % 2 == 1: # Only """alt_regex"""-containing constructs will ever set this and this use this, so no need to check field
			regex = re.compile(construct['alt_regex'], re.M) # Using a regex object allows for multiple searches
			match = regex.search(text, i) # """i""" starts the [next] match after the end position [of the last]
			alt_regex = re.compile(construct['regex'], re.M)
			alt_match = alt_regex.search(text, i)
		else:
			regex = re.compile(construct['regex'], re.M)
			match = regex.search(text, i)
			if construct['alt_regex']:
				alt_regex = re.compile(construct['alt_regex'], re.M)
				alt_match = alt_regex.search(text, i)
			else:
				alt_match = None

		if match:
			print(f'Success on {match.group(1)}')

			text = f'{text[:match.start(1)]}{construct["opening_tag"]}{match.group(1)}{text[match.end(1):]}'
			i = match.end(1) + len(construct['opening_tag'])
			subtext = ''

			if construct['alt_regex']:
				match = regex.search(text, i) # Search same tag again with new """i"""
				alt_i = i
				i = match.end(1)
				subtext = f'{text[alt_i:i - len(match.group(1)) - 1]}' # Subtracts the closing marker *and* newline
				print(f'Subtext: {subtext}')

			if match.group(1) == '': # Add blank line to escaped headings
				text = f'{text[:i]}{construct["closing_tag"]}\n{text[i:]}'
				i += len(construct['closing_tag']) + 1
			else:
				text = f'{text[:i]}{construct["closing_tag"]}{text[i:]}'
				i += len(construct['closing_tag'])
			
			# Beyond scope at this time!
			# if construct['contains_block_constructs']:
				# print(f'Subtext; BC length: {len(block_constructs)}')
				# subtext, _, _, j = parse_html(text[i:match.start(1)], block_constructs) # Parse only the contained text
				# print(subtext)
				# print(f'j = {j}')
				# text = f'{text[:match.end(1)]}{subtext}'

			# if match:
				# text = f'{text[:match.start(1) + len(subtext)]}{match.group(1)}{construct["closing_tag"]}{text[match.end(1):]}'
				# i = match.end() + len(construct['closing_tag']) + len(subtext)

		else:
			del constructs[[*constructs.keys()][0]]
#			print(len(constructs))
			text, constructs, depth, i = parse_html(text, constructs)

	return text, constructs, 0, i

def get_title(text):
	'''
	Get the UEWSG title from a string.

	Assumes the title is not escaped or in a container, ie it is the first single line in the string.

	**text**: str

	Returns str
	'''

	return re.compile('\\A(.*?)$', re.M).search(text).group(1)

def make_html_header(title):
	'''
	Make an HTML header with a given title.

	The header body is based upon the UEWSG [0.2.0] recommendations; only the title can currently be modified programmatically.

	**title**: str

	Returns str
	'''

	return f'''<!doctype html>

<html lang="en" dir="ltr">	

<head>
	<title>{title}</title>
	<meta charset="UTF-8">
	<meta name="Viewport" content="initial-scale=1">
	<link rel="stylesheet" type="text/css" media="all, screen, print" href="http://uewsg.org/uewsg_0.2.0.css">
</head>

<body>

'''
#
# +++
# Output
#
if __name__ == '__main__':
	html, _, _, _ = parse_html(test_text, json.loads(json.dumps(block_constructs))) # Remember: complex returns are tuples: unpack them; and deepcopy using JSON is thread-safe (https://stackoverflow.com/questions/5105517/deep-copy-of-a-dict-in-python): use it so the dictionary doesn't get depleted!
	print(html)
	title = get_title(test_text)
	print(f'Title: {title}')
	print(make_html_header(title))