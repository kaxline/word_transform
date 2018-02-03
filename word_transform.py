import sys
import nltk
from nltk.corpus import words
import sys
from difflib import ndiff
import re
import multiprocessing

# Check that two valid words were given
try:
	A = sys.argv[1]
	B = sys.argv[2]
except IndexError:
	print 'Please provide an initial word as the first argument and a target word as the second argument'
	exit()

if len(A) is not 5 or len(B) is not 5:
	print 'Error: Both words must be exactly five characters'
	exit()

if A == B:
	print A
	print B
	exit()


# Check for user provided dictionary of words
user_dictionary = None

try:	
	user_dictionary = sys.argv[3]
except IndexError as index_error:
	pass

word_list = []

# If no dictionary provided, download a list from nltk
if user_dictionary is None:
	nltk.download('words')

	word_list = set(words.words())

else:
	# Parse space-separated user dictionary into words
	text = []
	with open(user_dictionary, 'r') as inputfile:
		for line in inputfile:
			raw_words = line.split(' ')
			clean_words = []
			# Remove any line break characters
			for word in raw_words:
				clean_words.append(word.translate(None, '\n'))
			text = text + clean_words
	word_list = set(text)

# Select all five letter words from list
five_letter_words = [word for word in word_list if len(word) == 5]

# Make sure the words provided are part of the list
is_A_valid = len([word for word in five_letter_words if word == A]) > 0

is_B_valid = len([word for word in five_letter_words if word == B]) > 0

if not is_A_valid:
	print 'Sorry, %s is not a known word' % A
	exit()
if not is_B_valid:
	print 'Sorry, %s is not a known word' % B
	exit()

def flatten_sequence_words(sequence):
	''' 
	Takes a list of word lists and returns a single list with all the words included in the lists.

	Parameters
	----------
	sequence : list
		A list of lists of strings
	
	Returns
	-------
	list
		A list of all strings included in all sequence lists
	'''
	flat_list = []
	for string_list in sequence:
		for string in string_list:
			words_from_string = re.compile('\w+').findall(string)
			for word in words_from_string:
				flat_list.append(word)			
	return list(set(flat_list))

def generate_possible_words(initial_word, target_word, excluded_words_list):
	''' 
	Generates possible words that would transform one letter in initial_word into the same letter as the target_word at the same position. 

	Parameters
	----------
	initial_word : str
		The word to transform

	target_word : str
		The word to transform to

	excluded_words_list : list
		List of strings to exclude from consideration when translating
	
	Returns
	-------
	list
		A list of words that share one letter with the target_word and four letters with the initial_word
	'''
	possible_words = []

	for index, letter in enumerate(initial_word):
		if target_word[index] == letter:
			# No need to check the letters that are already the same
			continue
		beginning_substring = initial_word[:index]
		ending_substring = initial_word[(index + 1):]
		possible_words_at_position_change = [word for word in five_letter_words if word != initial_word and (word not in excluded_words_list) and word[:index] == beginning_substring and word[(index + 1):] == ending_substring]
		possible_words = possible_words + possible_words_at_position_change

	return possible_words

def process_word_sequence(word_sequence, direction, previous_words):
	''' 
	Takes a word sequence and finds a list of potential word translations.

	Parameters
	----------
	word_sequence : list
		A list of lists of strings

	direction : str
		Either 'forward' or 'backward' depending on which sequence is being passed in

	previous_words : list
		A list of strings to avoid attempting to transform
	
	Returns
	-------
	list
		A list of all potential word combinations, presented as a space separated series of words.
		e.g. ['smart start', 'smart skart']
	'''
	new_word_list = []

	word = word_sequence[-5:]

	target_word = B if direction == 'forward' else A
	
	possible_words = generate_possible_words(word, target_word, previous_words)

	for possible_word in possible_words:
		updated_string = word_sequence + ' ' +  possible_word
		new_word_list.append(updated_string)

	return new_word_list

def check_for_solutions(forward_word_sequence_list, backward_word_sequence_list):
	''' 
	See if the forward-looking process and backward-looking process have met. If so, combine the
	two overlapping strings into one solution and return a list of solutions.

	Parameters
	----------
	forward_word_sequence_list : list
		A list of lists of strings

	backward_word_sequence_list : list
		A list of lists of strings
	
	Returns
	-------
	list
		A list of all solutions
	'''
	solutions = []
	for forward_word_sequence in forward_word_sequence_list:
		for backward_word_sequence in backward_word_sequence_list:
			backward_words = re.compile('\w+').findall(backward_word_sequence)
			forward_words = re.compile('\w+').findall(forward_word_sequence)
			most_recent_backward_word = backward_words[-1]
			most_recent_forward_word = forward_words[-1]
			if most_recent_forward_word == most_recent_backward_word:
				# Drop the overlapping word
				backward_words = backward_words[:-1]
				# Reverse the list
				backward_words = backward_words[::-1]
				solution_string = ' '.join(forward_words) + ' ' + ' '.join(backward_words)
				solutions.append(solution_string)

	return solutions


def print_solutions(solutions):
	''' 
	Format all solutions and print them to the console.

	Parameters
	----------
	solutions : list
		A list of strings
	
	Returns
	-------
	None
	'''
	for index, solution in enumerate(solutions):
		print ' '
		print 'Solution %s' % (index + 1)
		print ' '
		words_from_string = re.compile('\w+').findall(solution)
		for index, word in enumerate(words_from_string):
			if index == 0:
				print word
				continue
			if word == B:
				print word
				print ''
				print ''
				continue
			print '  ' + word

possible_words_sequence_forward = [
	[A]
]

possible_words_sequence_backward = [
	[B]
]

solutions = []

counter = 0

processor_pool = multiprocessing.Pool(multiprocessing.cpu_count())

print 'Working ...'

while True:
	forward_word_sequence_list = possible_words_sequence_forward[counter]
	forward_previous_words = flatten_sequence_words(possible_words_sequence_forward)

	backward_word_sequence_list = possible_words_sequence_backward[counter]
	backward_previous_words = flatten_sequence_words(possible_words_sequence_backward)

	solutions = check_for_solutions(forward_word_sequence_list, backward_word_sequence_list)
	
	if len(solutions) > 0:
		print_solutions(solutions)
		exit()	

	forward_new_word_list = []
	backward_new_word_list = []
	forward_tasks = []
	backward_tasks = []

	for word_sequence in forward_word_sequence_list:
		forward_tasks.append((word_sequence, 'forward', forward_previous_words))

	for word_sequence in backward_word_sequence_list:
		backward_tasks.append((word_sequence, 'backward', backward_previous_words))
	
	forward_results = [processor_pool.apply_async(process_word_sequence, t) for t in forward_tasks]
	backward_results = [processor_pool.apply_async(process_word_sequence, t) for t in backward_tasks]

	for forward_result in forward_results:
		new_word_list_part = forward_result.get()
		forward_new_word_list = forward_new_word_list + new_word_list_part

	for backward_result in backward_results:
		new_word_list_part = backward_result.get()
		backward_new_word_list = backward_new_word_list + new_word_list_part

	if len(forward_new_word_list) == 0 and len(backward_new_word_list) == 0:
		print "No solution found for %s and %s" % (A, B)
		exit()
	
	possible_words_sequence_forward.append(forward_new_word_list)
	possible_words_sequence_backward.append(backward_new_word_list)
	counter += 1






