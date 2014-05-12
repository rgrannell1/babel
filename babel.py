
import sublime, sublime_plugin, os, random
from random import sample
from ntpath import basename


# -- my python foo is lacking, so please don't be offended by my code...

class BabelCommand (sublime_plugin.WindowCommand):

	def run (self):

		window = self.window

		def currently_open (filename):
			# -- is the file currently open?.

			views = window.views()

			open_files = {view.file_name() for view in views}

			return filename in open_files

		open_folders = window.folders()

		def recurwalk (folder):
			# -- generate a flat list of directories in 

			for path, dirs, files in os.walk(folder):
				if '.git' in dirs:
					# -- replace this with a proper .ignore / reject!
					dirs.remove('.git')
				for file in files:
					yield os.path.join(path, file)

		def reservoir_sample (iter):
			# -- use reservoir sampling to avoid loading the folder in memory.

			for ith, elem in enumerate(iter, 1):
				if random.randrange(ith) == 0:
					selected = elem

			return selected

		candidate_files = []

		for folder in open_folders:
			valid_files = recurwalk(folder)
			file = reservoir_sample(valid_files)
			
			candidate_files.extend(file)		

		unopened_candidates = [f for f in candidate_files if not currently_open(f)]

		# -- try open an unopened file.
		if len(unopened_candidates) > 0:
			chosen_file = list(sample(unopened_candidates, 1))[0]
		else:
			chosen_file = list(sample(candidate_files, 1))[0]

		# -- open an overwritable new tab, 
		# -- so you can flick between files quickly.
		window.open_file(chosen_file, sublime.TRANSIENT)
