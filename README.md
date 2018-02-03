# Word Transform

A Python script that, given a dictionary, finds the shortest transformation between two five letter words, A and B, such that only one letter can be changed at a time and all intermediate words in the tranformation must exist in the dictionary.

## Getting Started

First, you'll need to install [Python 2.7](https://www.python.org/downloads/) if you haven't already.

Then, download this repo.

Once downloaded, run the script with the provided sample dictionary and the following arguments:

`python ./word_transform.py smart brain sample_dict.py`

You should see an output like this:

```bash
Solution 1

smart
  start
  stark
  stack
  slack
  black
  blank
  bland
  brand
  braid
brain
```

If you'd like to use your own dictionary, replace `sample_dict.py` in the command above with a path to the text file you'd wish to use. Dictionary files must only contain space-separated words.

If you wish to use the dictionary provided by the [Natural Language Toolkit](http://www.nltk.org/), simply leave off the filename like so:

`python ./word_transform.py smart brain`

Please note that with the full `nltk` dictionary, some queries may take up to a few minutes.