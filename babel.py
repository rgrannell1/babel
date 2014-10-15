#! /usr/bin/env python 3

import os
import sublime
import sublime_plugin
import random
import re
import sys






__version__ = '0.2.1'
__authors__ = ['Ryan Grannell (@RyanGrannell)']

# -- default options. Find way to load in custom options.

options = {
	'ignore_version_control': True
}








# -- utility functions

def recurwalk (folder, ignored_dirs, ignored_files):
	"""
	generate a flat list in a non-ignored
	files in a directory.
	"""

	def is_valid_dir (dir):
		return not any([dir + '/' == igdir for igdir in ignored_dirs])

	def is_valid_file (file):
		return not any([re.search(igfile, file) for igfile in ignored_files])






	for path, dirs, files in os.walk(folder, topdown = True):
		# -- filter out ignored directories.

		# -- modify dirs in place.
		dirs[:] = [dir for dir in dirs if is_valid_dir(dir)]

		for file in files:

			if is_valid_file(file):
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
		# -- no babel ignore file found.

		print("NOTE: no .babelignore found in " + folder)

		return {
			'dir':  ['.git/', '.hg/'] if options['ignore_version_control'] else [],
			'file': []
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
	is_directory  = "[/]$"

	lines = contents.split('\n')

	# -- remove the empty lines
	patterns = [l for l in lines if not re.search(is_formatting, l)]

	# -- lexically close over 'igdirs' and 'igfiles',
	# -- create testing functions.

	return {
		'dir':  [d for d in patterns if     re.search(is_directory, d)],
		'file': [f for f in patterns if not re.search(is_directory, f)]
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

				ignored      = read_babelignore(folder)
				non_ignored  = recurwalk(folder, ignored['dir'], ignored['file'])

				non_open     = remove_open(non_ignored)

				for file in non_open:
					yield file

		# -- choose a random, non-ignored file in your open folders.
		chosen_file = rsample(project_files(open_folders))

		window.open_file(chosen_file, sublime.TRANSIENT)
