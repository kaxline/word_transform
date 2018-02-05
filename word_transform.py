import multiprocessing
from methods import *
import config

possible_words_sequence_forward = [
	[config.A]
]

possible_words_sequence_backward = [
	[config.B]
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
	
	# Note: Could be possible to parallelize the forward and backward processes as well if performance
	# is still an issue
	forward_results = [processor_pool.apply_async(process_word_sequence, t) for t in forward_tasks]
	backward_results = [processor_pool.apply_async(process_word_sequence, t) for t in backward_tasks]

	for forward_result in forward_results:
		new_word_list_part = forward_result.get()
		forward_new_word_list = forward_new_word_list + new_word_list_part

	for backward_result in backward_results:
		new_word_list_part = backward_result.get()
		backward_new_word_list = backward_new_word_list + new_word_list_part

	if len(forward_new_word_list) == 0 and len(backward_new_word_list) == 0:
		print "No solution found for %s and %s" % (config.A, config.B)
		exit()
	
	possible_words_sequence_forward.append(forward_new_word_list)
	possible_words_sequence_backward.append(backward_new_word_list)
	counter += 1






