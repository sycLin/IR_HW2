#!/usr/bin/python
# -*- coding: utf8 -*-
import sys, os
from copy import deepcopy # for EM algorithm
from hw2 import Corpus, Category, Document # import my classes from hw2.py
from hw2 import ErrorExit, extractWordsFromFile # import my functions from hw2.py

def converge(newResult, oldResult):
	"""
	here is my own definition of convergence.
	for each document:
	    c_new == c_old, and
	    abs(est_new - est_old) <= 100
	"""

	old_sum = sum([detail[1] for dname, detail in oldResult.iteritems()])
	new_sum = sum([detail[1] for dname, detail in newResult.iteritems()])
	if abs(new_sum / old_sum - 1.0) > 0.001:
		return False
	return True

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
	result = {} # key: documentName, value: (cName, estimation)
	for dname, words in unlabelDocs.iteritems():
		result[dname] = myCorpus.classify(words)
	# add to myCorpus as tmpCorpus
	tmpCorpus = deepcopy(myCorpus)
	for dname, words in unlabelDocs.iteritems():
		cname = result[dname][0]
		tmpCorpus.buildVocabulary(cname, dname, words)
	# classify with tmpCorpus
	tmp_result = {} # key: documentName, value: (cName, estimation)
	for dname, words in unlabelDocs.iteritems():
		tmp_result[dname] = tmpCorpus.classify(words)
	# main while loop
	iter_counter = 1
	while not converge(newResult=tmp_result, oldResult=result):
		# record the last result in "result"
		result = deepcopy(tmp_result)
		# tmpCorpus <- myCorpus + result
		tmpCorpus = deepcopy(myCorpus)
		for dname, words in unlabelDocs.iteritems():
			cname = result[dname][0]
			tmpCorpus.buildVocabulary(cname, dname, words)
		# classify unlabelDocs with tmpCorpus => tmp_result
		tmp_result = {}
		for dname, words in unlabelDocs.iteritems():
			tmp_result[dname] = tmpCorpus.classify(words)
		iter_counter += 1
		# print >> sys.stderr, "iteration #%d" % (iter_counter)
	# print >> sys.stderr, "total iteration count = %d" % (iter_counter)


	# finish EM, and tmpCorpus is with adjusted parameters
	# classify the test data
	myCorpus = tmpCorpus
	for i in range(1, 9420):
		print "%d %s" % (i, myCorpus.classify(extractWordsFromFile(os.path.join(testDir, str(i))))[0])


	pass



if __name__ == "__main__":
	main()

