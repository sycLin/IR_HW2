#!/usr/bin/python
# -*- coding: utf8 -*-
import sys, os
from copy import deepcopy # for EM algorithm
from hw2 import Corpus, Category, Document # import my classes from hw2.py
from hw2 import ErrorExit, extractWordsFromFile # import my functions from hw2.py

def main():
	# check argument count
	if len(sys.argv) != 4:
		ErrorExit("wrong argument count")

	# check arguments
	trainDir = sys.argv[1]
	unlabelDir = sys.argv[2]
	testDir = sys.argv[3]
	if not (os.path.isdir(trainDir) and os.path.isdir(unlabelDir) and os.path.isdir(testDir)):
		ErrorExit("incorrect argument(s) given")

	# build corpus
	myCorpus = Corpus()
	myCorpus.batchAddCategories(os.listdir(trainDir)) # add categories
	for cname in myCorpus.getCategoryNames():
		for dname in os.listdir(os.path.join(trainDir, cname)):
			dpath = os.path.join(os.path.join(trainDir, cname), dname)
			myCorpus.buildVocabulary(cname, dname, extractWordsFromFile(dpath))

	# EM algorithm
	#
	# myCorpus.classify() => res
	# tmpCorpus = myCorpus + res
	# tmpCorpus.classify() => tmp_res
	# while tmp_res BETTER THAN res
	#     res = tmp_res
	#     tmpCorpus = myCorpus + tmp_res
	#     tmpCorpus.classify() => tmp_res
	
	# read unlabeled documents
	unlabelDocs = {} # key: docName, value: words
	for dname in os.listdir(unlabelDir):
		unlabelDocs[dname] = extractWordsFromFile(os.path.join(unlabelDir, dname))
	# classify unlabelDocs
	result = {}
	for dname, words in unlabelDocs.iteritems():
		result[dname] = myCorpus.classify(words)
	# add to myCorpus as tmpCorpus
	tmpCorpus = deepcopy(myCorpus)
	pass



if __name__ == "__main__":
	main()

