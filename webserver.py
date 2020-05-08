# Webserver | UEWSG Parser 0.1.0
#
# https://github.com/Bizzlebin/uewsg_parser_0.1.0/webserver.py
#
# ***
#
# By JBT
#
# ***
#
# Created on 2020-05-02
#
# Updated on 2020-05-08
#
# ***
#
# Copyright © 2020 JBT
#
# All rights reserved. Under New Kidronite law, copyright lasts 7 years from the date of a work's release and the work is thereafter automatically dedicated to the public domain by the owner(s); this applies in The Kingdom Of New Kidron (NK) and extends to all Orthodox Christians in other jurisdictions universally (Deuteronomy 15.1–3). Outside of NK, copyright lasts 50 years from the date of a work's release and the work is thereafter automatically dedicated to the public domain by the owner(s); this applies universally to the extent possible under law (Leviticus 25.10–13). For more information on the terms of the 50-year release, visit https://creativecommons.org/publicdomain/zero/1.0/ .
#
# """THE WORK IS PROVIDED "AS IS" AND THE AUTHORS AND OWNERS DISCLAIM ALL WARRANTIES WITH REGARD TO THIS WORK INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHORS OR OWNERS BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS WORK."""
#
# +++
# Description
#
# A basic Python HTTP server, using lib classes and providing a simple response to "GET" requests.
#
__all__ = ['httpd'] # Restricts what is exported on """import * from [module]"""
#
# +++
# Imports
#
from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import path
from urllib import parse
import os, uewsg_parser, json
#
# +++
# Functions
#
class httpd(BaseHTTPRequestHandler): # Call it httpd (daemon)
	'''
	Implements a web server that answers "GET" requests.

	+ do_GET(self)
	+ do_POST(self)
	'''
	'''
	The superclass, """BaseHTTPRequestHandler""", and/or its superclass[es] implements much of the server I/O and handles everything from IP addresses to ports. However, it does not implement any sort of response, even to basic "GET" requests. Thus, it must be subclassed with methods such as """do_GET()""" which provide that functionality.
	'''

	print('Webserver (httpd) for UEWSG Parser 0.1.0 started...')

	def do_GET(self):
		'''
		Respond to "GET" requests.

		This particular method only sends the basic headers in response, then content—which is predefined in the method.

		No returns
		'''

		self.send_response(200)
		self.send_header('Content-Type', 'Text/HTML')
		self.end_headers()
		try:
			with open(os.path.join(path[0], 'index.html'), encoding = 'UTF-8') as index:
				self.wfile.write(index.read().encode()) # This is an """io.BufferedIOBase""" stream (https://docs.python.org/3/library/io.html#io.BufferedIOBase)!
		except IOError:
			self.wfile.write('\nIndex not found!'.encode())

	def do_POST(self):
		'''
		Respond to "POST" requests.

		This sends the basic headers in response, then a parsed version of the contents of the POST request; the output is in HTML5 and requires the uewsg_parser module.

		No returns
		'''

#		print('Received form input!')
		self.send_response(200)
		self.send_header('Content-Type', 'Text/HTML; Charset=UTF-8') # HTML responses [normally] already include a charset, but plaintext responses do not
		self.end_headers()

#		print(self.rfile.read(int(self.headers['Content-Length']))) # Reading the stream by itself simply grabs """name=value""" pairs from the form, which is why urllib's query string parsing works on them, below

		form = parse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode('UTF-8')) # Do not use CGI!!!; pass the length to be read to the """read()""" method else the stream will stay open; """decode()""" else the result will be returned in byte objects; the form is essentially JSON, with every form field name followed by a *list* containing its contents (usually just a string)
		text = form['input'][0].replace('\r\n', '\n') # Do not forget to index it—and convert to unsemantic Python newlines!
		print(text)
		title = uewsg_parser.get_title(text)
		print(f'Title: {title}')
		
		html_header = uewsg_parser.make_html_header(title)
		html, _, _, _ = uewsg_parser.parse_html(text, json.loads(json.dumps(uewsg_parser.block_constructs))) # Make a thread-safe *copy* of the dictionary!

		html = f'{html_header}{html}{uewsg_parser.html_footer}'
		self.wfile.write(f'''<textarea id="output" style="width: 100%; height: 100%">{html}</textarea>'''.encode())
#
# +++
# Output
#
HTTPServer(('127.0.0.1', 8000), httpd).serve_forever()