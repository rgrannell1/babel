
import sublime, sublime_plugin, os, random
from random import sample
from ntpath import basename
import re

# -- utility functions

def recurwalk (folder, ignored_dirs, ignored_files):
	"""generate a flat list of directories in
	"""

	print(ignored_dirs)

	for path, dirs, files in os.walk(folder):
		# -- filter out ignored directories.
		for dir in dirs:
			if dir + '/' in ignored_dirs:
				dirs.remove(dir)

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

		# -- remove the empty lines
		patterns = [l for l in lines if not re.search(whitespace_line, l)]

		dirs     = [d for d in patterns if re.search(is_directory, d)]
		files    = [f for f in patterns if not re.search(is_directory, f)]

		return [dirs, files]










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

			ignored = read_babelignore(folder)

			valid_files = recurwalk(folder, ignored[0], ignored[1])
			file = rsample(valid_files)

			candidate_files.extend([file])

		chosen_file = rsample(candidate_files)

		# -- open an overwritable new tab,
		# -- so you can flick between files quickly.
		window.open_file(chosen_file, sublime.TRANSIENT)
