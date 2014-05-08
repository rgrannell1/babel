import sublime, sublime_plugin, os, random
import itertools
from random import sample
from functools import reduce
from operator import add

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

			files = [contents[0] + '/' + f for f in contents[2]]

			return(sample(files, 1)[0])

		chosen_files = [get_random_file(folder) for folder in open_folders]
		chosen_file  = sample(chosen_files, 1)[0]

		self.window.open_file(chosen_file, sublime.TRANSIENT)