
import os
import random

"""
recurwalk

get a flat iterator of every file in a directory,
as filtered by a predicate.

@param  folder a string. The path to recur through.

@param  valid_dir a unary predicate. A function
        that determines whether a directory should
        be recurred into.

@param  valid_file a unary predicate. A function
        that determines whether a file should be
        included in the output.

@return an iterator that yields every file in
        a directory·

"""

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











"""
rsample

return a random element from an iterator, with equal probability.

@details rsample uses reservoir-sampling to return a random element
         from a collection of unknown length, with equal probability
         of any element being returned.

@param iter. The iterator to return an element from.

@return a value from the iterator. If no elements are found,
        defaults to None to prevent an error.
"""
def rsample (iter):

	selected = None

	for ith, elem in enumerate(iter, 1):
		if random.randrange(ith) == 0:
			selected = elem

	return selected











"""
chain

join iterators end-to-end

@param *iters spread parametre for iterators. The iterators to
       concatenate end-to-end.

@return an iterator.
"""

def chain (*iters):

	for iter in iters:
		for elem in iter:
			yield elem
