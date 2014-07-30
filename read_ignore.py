
import os
import sublime
import sublime_plugin
import random
import re
import sys










"""
read_ignore

read the .babelignore file in a folder, if one exists.

@param dir a string. The dir to check for a .babelignore file.

@return a string. The contents of the babelignore file. Returns the
        empty string if no file was found.

"""

def read_ignore (dir):

	dpath = os.path.join(dir, '.babelignore')

	try:
		conn = open(dpath, 'r')
	except IOError:
		# -- the .babelignore most likely wasn't found.
		""
	else:
		fcontents = conn.read()
		conn.close()

		return fcontents











"""
parse_ignore

@param contents a string. The raw text from a .babelignore file.

@return a dictionary with two fields: dir & file. dir is a unary
        predicate that tests if a directory should be recurred into.
        file is a unary predicate that tests if a file should be
        yielded.
"""

def parse_ignore (contents):

	empty_regexp   = '^$'
	comment_regexp = '[ 	]*#.*$'

	def patterns (contents):

		for line in contents.split('\n'):
			if not re.search(empty_regexp + '|' + comment_regexp, line):
				yield line










"""
ignored_paths

return predicates that filter paths and files.

@param dir a string. The dir to check for a .babelignore file.

@return a dictionary with two fields: dir & file. dir is a unary
        predicate that tests if a directory should be recurred into.
        file is a unary predicate that tests if a file should be
        yielded.
"""

def ignored_paths (dir):

	fcontents = read_ignore(dir)

	if fcontents:
		parse_ignore(contents)
	else:

		def valid_dir (dpath):

			dname = os.path.basename(dpath)

			versioning = {'.git/', '.hg/'}

			return dpath in versioning

		def valid_file (fpath):
			return True

		return {
			'dir' : valid_dir,
			'file': valid_file
		}