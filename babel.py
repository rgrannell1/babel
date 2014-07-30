#! /usr/bin/env python 3

import os
import sublime
import sublime_plugin
import random
import re
import sys

__version__ = '0.1.0'
__authors__ = ['Ryan Grannell (@RyanGrannell)']

is_python3 = sys.version_info[0] > 2

# -- default options. Find way to load in custom options.

options = {
	'ignore_version_control': True
}








# -- utility functions

def recurwalk (folder, valid_dir, valid_file):
	"""
	generate a flat list in a non-ignored
	files in a directory.
	"""

	for path, dirs, files in os.walk(folder):
		# -- filter out ignored directories.
		for dir in dirs:
			if not valid_dir(dir):
				dirs.remove(dir)

		for file in files:
			if valid_file(file):
				yield os.path.join(path, file)











def rsample (iter):
	"""
	return a random element from a generator
	without loading the generator into memory.
	"""

	selected = None

	for ith, elem in enumerate(iter, 1):
		if random.randrange(ith) == 0:
			selected = elem

	return selected











def chain (*iters):
	"""
	join iterators together end to end.
	"""

	for iter in iters:
		for elem in iter:
			yield elem










def read_babelignore (folder):
	"""
	try to read the .babelignore folder
	and if it is present return two functions
	denoting if a file or folder is valid.
	"""

	file = os.path.join(folder, '.babelignore')

	try:
		conn = open(file, 'r')
	except IOError:
		# -- don't print. This happens all the time.

		def valid_dir (dir):
			"""
			is the dir not-ignored?
			"""

			# -- match the whole sentence; replace asterices with regex wildcards.

			versioning = {'.git/', '.hg/'}

			if dir + '/' in versioning and options['ignore_version_control']:
				return False

			return True

		return {
			'dir':  valid_dir,
			'file': lambda file: True
		}

	else:
		contents = conn.read()
		conn.close()

		return parse_babelignore(contents)










def parse_babelignore (contents):
	"""
	given the contents of a .babelignore file
	return functions that dictate whether a file
	or folder is ignored or not.
	"""

	is_formatting = "^\s*$|^\s*[#]$"
	is_directory    = "[/]$"

	lines = contents.split('\n')

	# -- remove the empty lines
	patterns = [l for l in lines if not re.search(is_formatting, l)]

	dirs     = [d for d in patterns if re.search(is_directory, d)]
	files    = [f for f in patterns if not re.search(is_directory, f)]

	# -- lexically close over 'dirs' and 'files',
	# -- create testing functions.

	def valid_dir (dir):
		"""
		is the dir not-ignored?
		"""

		# -- match the whole sentence; replace asterices with regex wildcards.
		dir_pattern = '^' + dir.replace('[*]', '.+') + '/' + '$'

		versioning = {'.git/', '.hg/'}

		if dir + '/' in versioning and options['ignore_version_control']:
			return False

		for igdir in dirs:

			if re.search(dir_pattern, igdir):
				return False

		return True

	def valid_file (file):
		"""
		is the file not-ignored?
		"""

		# -- match the whole sentence; replace asterices with regex wildcards.
		file_pattern = '^' + file.replace('[*]', '.+') + '/' + '$'

		for igfile in files:

			if re.search(file_pattern, igfile):
				return False

		return True

	return {
		'dir':  valid_dir,
		'file': valid_file
	}








class BabelCommand (sublime_plugin.WindowCommand):
	"""
	babel loads a random file from your
	currently open folders.
	"""

	def run (self):

		window = self.window
		open_folders = window.folders()

		def remove_open (files):
			"""
			return a generator that filters out open files
			from a generator of files.
			"""

			views = window.views()

			open_files = {view.file_name() for view in views}

			for file in files:
				if not file in open_files:
					yield file

		def project_files (open_folders):
			"""
			yield the non-open, non-ignored files available
			to choose from.
			"""

			for folder in open_folders:
				is_valid     = read_babelignore(folder)
				non_ignored  = recurwalk(folder, is_valid['dir'], is_valid['file'])

				non_open     = remove_open(non_ignored)

				for file in non_open:
					yield file

		# -- choose a random, non-ignored file in your open folders.
		chosen_file = rsample(project_files(open_folders))

		window.open_file(chosen_file, sublime.TRANSIENT)
