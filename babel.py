#! /usr/bin/env python 3

import os
import sublime
import sublime_plugin
import random
import re
import sys

from babel.flotsam     import recurwalk, rsample, chain
from babel.read_ignore import read_babelignore, parse_babelignore

print('babel loaded.')










__version__ = '0.1.0'
__authors__ = ['Ryan Grannell (@RyanGrannell)']

is_python3 = sys.version_info[0] > 2












# -- default options. Find way to load in custom options.

options = {
	'ignore_version_control': True
}











class BabelCommand (sublime_plugin.WindowCommand):
	"""
	babel loads a random file from your
	currently open folders.
	"""

	def run (self):

		print('running')

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
