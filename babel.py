
import sublime, sublime_plugin, os, random
from random import sample
from ntpath import basename
import re

# -- utility functions

def recurwalk (folder):
	"""generate a flat list of directories in
	"""

	excluded_dirs  = {'.git'}

	for path, dirs, files in os.walk(folder):
		if '.git' in dirs:
			# -- replace this with a proper .ignore / reject!
			dirs.remove('.git')
		for file in files:
			yield os.path.join(path, file)











def rsample (iter):
	"""use reservoir sampling to avoid loading the folder in memory.
	"""

	for ith, elem in enumerate(iter, 1):
		if random.randrange(ith) == 0:
			selected = elem

	return selected











def read_babelignore (folder):
	"""parse the .babelignore file

	Each line specifies a pattern
	"""

	file = os.path.join(folder, '.babelignore')

	try:
		conn = open(file, 'r')
	except IOError:
		print("cannot open ", file, ": file probably does not exist.")
	else:
		contents = conn.read()
		conn.close()

		# -- get directories.
		whitespace_line = "^\s*$"
		is_directory = "[/]$"

		lines = contents.split('\n')

		# -- mimic the .gitignore format


		# -- remove the empty lines
		non_empty = (l for l in lines if not re.search(whitespace_line, l))









class BabelCommand (sublime_plugin.WindowCommand):
	"""
	babel loads a random file from your
	currently open folders.
	"""

	def run (self):

		def currently_open (filename):
			# -- is the file currently open?.

			views = window.views()

			open_files = {view.file_name() for view in views}

			return filename in open_files
		excluded_files = {}

		window = self.window
		open_folders = window.folders()

		candidate_files = []

		for folder in open_folders:

			read_babelignore(folder)

			valid_files = recurwalk(folder)
			file = rsample(valid_files)

			candidate_files.extend([file])

		chosen_file = rsample(candidate_files)

		# -- open an overwritable new tab,
		# -- so you can flick between files quickly.
		window.open_file(chosen_file, sublime.TRANSIENT)
