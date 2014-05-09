
import sublime, sublime_plugin, os, random
from random import sample

# -- my python foo is lacking, so please don't be offended by my code...

class BabelCommand (sublime_plugin.WindowCommand):

	def run (self):

		window = self.window

		def ignored (filename):
			# -- replace this with a proper ignore file.
			return filename == ".git"

		open_folders = window.folders()

		candidate_files = []

		for folder in open_folders:
			contents = list(os.walk(folder))[0]

			# -- generate the full path names for none-ignored files.
			contained_files = [contents[0] + '/' + f for f in contents[2] if not ignored(f)]

			if len(contained_files) > 0:
				# -- append one file from each folder to a final list of candidates.

				random_file = list(sample(contained_files, 1))
				candidate_files.extend(random_file)

		unopened_candidates = [f for f in candidate_files if not currently_open(f)]

		# -- try open an unopened file.
		if len(unopened_candidates) > 0:
			list(sample(unopened_candidates, 1))[0]
		else:
			list(sample(candidate_files, 1))[0]

		chosen_file = list(sample(candidate_files, 1))[0]


		# -- open an overwritable new tab, so you can flick between files quickly.
		window.open_file(chosen_file, sublime.TRANSIENT)





