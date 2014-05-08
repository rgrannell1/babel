import sublime, sublime_plugin, os, random
import itertools
from random import sample
from functools import reduce
from operator import add

# -- my python foo is lacking, so please don't be offended by my code...

# -- semantic selectors
def firstOf (coll):
	return coll[0]

def secondOf (coll):
	return coll[1]

def thirdOf (coll):
	return coll[2]

class BabelCommand( sublime_plugin.WindowCommand ):
	def run( self ):

		open_folders = self.window.folders()

		def get_random_file (folder):
			# -- string -> string
			# -- return a random file somewhere recursively within a folder.

			contents = list(os.walk(folder))[0]

			files = [firstOf(contents) + '/' + f for f in contents[2]]

			return(firstOf(sample(files, 1)))

		chosen_files = [get_random_file(folder) for folder in open_folders]
		chosen_file  = firstOf(sample(chosen_files, 1))

		self.window.open_file(chosen_file, sublime.TRANSIENT)
