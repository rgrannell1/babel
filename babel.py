
import sublime, sublime_plugin, os, random
from random import sample
from ntpath import basename

# -- utility functions

def recurwalk (folder):
	# -- generate a flat list of directories in 

	for path, dirs, files in os.walk(folder):
		if '.git' in dirs:
			# -- replace this with a proper .ignore / reject!
			dirs.remove('.git')
		for file in files:
			yield os.path.join(path, file)

def rsample (iter):
	# -- use reservoir sampling to avoid loading the folder in memory.

	for ith, elem in enumerate(iter, 1):
		if random.randrange(ith) == 0:
			selected = elem

	return selected

def valid_files (folder):
	# -- yield every non-ignored file in a folder.









class BabelCommand (sublime_plugin.WindowCommand):
	"""babel loads a random file from your
	currently open folders.
	"""

	def run (self):

		excluded_dirs  = {'.git'}
		excluded_files = {} 

		def currently_open (filename):
			# -- is the file currently open?.

			views = window.views()

			open_files = {view.file_name() for view in views}

			return filename in open_files

		window = self.window
		open_folders = window.folders()

		candidate_files = []

		for folder in open_folders:
			valid_files = recurwalk(folder)
			file = rsample(valid_files)
			
			candidate_files.extend([file])

		chosen_file = rsample(candidate_files)

		# -- open an overwritable new tab, 
		# -- so you can flick between files quickly.
		window.open_file(chosen_file, sublime.TRANSIENT)
