
import os
import sublime
import sublime_plugin
import random
import re
import sys

"""
read_babelignore





"""

def read_babelignore (folder):

	fpath = os.path.join(folder, '.babelignore')

	try:

		conn = open(fpath, 'r')

	except IOError:
		# -- the file wasn't found or couldn't be read, so
		# -- create default file/dir filtering functions.

		def valid_dir (dpath):

			dname = os.path.basename(dpath)

			versioning = {'.git/', '.hg/'}

			return dpath in versioning:

		def valid_file (fpath):
			return True

		return {
			'dir' : valid_dir,
			'file': valid_file
		}

	else:

		contents = conn.read()
		conn.close()

		return parse_babelignore(fcontents)











"""
parse_babelignore




"""

def parse_babelignore (contents):

	empty_regexp   = '^$'
	comment_regexp = '[ 	]*#.*$'

	def patterns (contents):

		for line in contents.split('\n'):
			if not re.search(empty_regexp + '|' + comment_regexp, line):
				yield line