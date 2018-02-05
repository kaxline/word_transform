import sys
import nltk
from nltk.corpus import words

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