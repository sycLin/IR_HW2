#!/usr/bin/python
# -*- coding: utf8 -*-
import sys, os
import re
from collections import defaultdict
from math import log

#
# class definition
#
class Corpus(object):
	def __init__(self):
		"""
		constructor, initialize some fields
		"""
		self.categories = [] # list of Category instances
		self.vocabulary = defaultdict(int) # dictionary of vocab mapping its occurrences
		self.vocabSize = 0 # the size of the vocabulary

	def getVocabulary(self):
		ret = []
		for k, v in self.vocabulary.iteritems():
			ret.append(k)
		return ret

	def countWord(self, word):
		"""
		@return the number of occurrence of word in this category
		"""
		return self.vocabulary[word.lower()]

	def getCategoryCount(self):
		"""
		@return the number of categories this corpus has
		"""
		return len(self.categories)

	def getCategoryNames(self):
		"""
		@return a list of category names
		"""
		ret = []
		for i in self.categories:
			ret.append(i.getName())
		return ret

	def getCategoryByName(self, cName):
		for i in self.categories:
			if i.getName() == cName:
				return i
		return None
	
	def hasCategory(self, categoryName):
		"""
		@return a boolean whether this corpus has this category
		"""
		for c in self.categories:
			if c.getName() == categoryName:
				return True
		return False

	def addCategory(self, categoryName):
		"""
		to add a category in this corpus
		"""
		if not self.hasCategory(categoryName):
			newCategory = Category(categoryName)
			self.categories.append(newCategory)

	def batchAddCategories(self, listOfCategoryNames):
		"""
		to add a list of categories in this corpus
		"""
		for cn in listOfCategoryNames:
			self.addCategory(cn)

	def buildVocabulary(self, cName, dName, words):
		"""
		building up vocabulary
		"""
		for w in words:
			# change all vocabulary to lower-case
			# increment the count
			if self.vocabulary[w.lower()] == 0:
				# new vocab
				self.vocabSize += 1
			self.vocabulary[w.lower()] += 1
		self.getCategoryByName(cName).buildVocabulary(dName, words)

	def __str__(self):
		s = "This corpus has %d categories\n" % (self.getCategoryCount())
		s += "and their names are:\n"
		s += str(self.getCategoryNames()) + "\n"
		s += "number of occurrences of 'how' is " + str(self.countWord('how'))
		return s

	def classify(self, words):
		"""
		to classify a document, given the words in it
		@return (categoryName, estimation)
		"""
		# pre-processing: ignore words with low collection frequency
		# words = [w for w in words if self.countWord(w) > 15] # will delete those <= 15
		estimation = float("-INF") # initialization
		categoryName = ""          # initialization
		for c in self.categories:
			e = c.estimate(words, self.vocabSize)
			if e > estimation:
				estimation = e
				categoryName = c.getName()
		return (categoryName, estimation)


class Category(object):
	def __init__(self, categoryName):
		self.name = categoryName
		self.totalWordCount = 0
		self.vocabulary = defaultdict(int) # dictionary of vocab mapping its occurrences
		self.documents = []

	def getVocabulary(self):
		ret = []
		for k, v in self.vocabulary.iteritems():
			ret.append(k)
		return ret

	def getName(self):
		"""
		@return the name of this category
		"""
		return self.name

	def getDocumentCount(self):
		"""
		@return the number of documents this category has
		"""
		return len(self.documents)

	def getDocumentNames(self):
		"""
		@return a list of document names
		"""
		ret = []
		for i in self.documents:
			ret.append(i.getName())
		return ret

	def getDocumentByName(self, dName):
		for i in self.documents:
			if i.getName() == dName:
				return i
		# not found, creat one
		d = Document(dName)
		self.documents.append(d)
		return self.documents[-1]

	def buildVocabulary(self, dName, words):
		"""
		building up vocabulary
		"""
		for w in words:
			self.vocabulary[w.lower()] += 1
			self.totalWordCount += 1
		self.getDocumentByName(dName).buildVocabulary(words)

	def countWord(self, word):
		"""
		@return the number of occurrence of word in this category
		"""
		return self.vocabulary[word.lower()]

	def getTotalWordCount(self):
		"""
		self.totalWordCount is maintained, so just return it
		"""
		return self.totalWordCount

	def __str__(self):
		s = "This category has %d documents\n" % (self.getDocumentCount())
		s += "number of occurrences of 'how' is " + str(self.countWord('how'))
		return s

	def estimate(self, words, globalVocabSize):
		"""
		to estimate the probability of a document with "words" belonging to this category
		(utilizing getWordProb() function)
		@globalVocabSize the vocabulary size of corpus, for smoothing in getWordProb()
		@return the estimation, floating point number
		"""
		estimation = 0.0
		for w in words:
			estimation += log(self.getWordProb(w, globalVocabSize))
		return estimation

	def getWordProb(self, word, globalVocabSize):
		"""
		to get the probability of "word"
		@globalVocabSize the vocabulary size of corpus, for smoothing
		@return the probability
		"""
		return float(self.countWord(word) + 0.5) / float(self.totalWordCount + globalVocabSize * 0.5)


class Document(object):
	def __init__(self, documentName):
		self.name = documentName
		self.totalWordCount = 0
		self.vocabulary = defaultdict(int) # dictionary of vocab mapping its occurrences

	def getVocabulary(self):
		ret = []
		for k, v in self.vocabulary.iteritems():
			ret.append(k)
		return ret

	def getName(self):
		"""
		@return the name of this document
		"""
		return self.name

	def countWord(self, word):
		"""
		@return the number of occurrence of word in this document
		"""
		return self.vocabulary[word.lower()]

	def buildVocabulary(self, words):
		for w in words:
			self.vocabulary[w.lower()] += 1

#
# global variables
#


#
# helper functions
#
def ErrorExit(msg):
	print >> sys.stderr, msg
	sys.exit(-1)

def extractWordsFromFile(filePath):
	"""
	use the "re" module to find all words in a file
	@return the words found
	"""
	with open(filePath, "r") as f:
		return re.findall(r'[a-zA-Z]+[a-zA-Z0-9\'\-@]*', f.read())
	return [] # default return

def main():

	# check argument
	if len(sys.argv) != 3 and len(sys.argv) != 4:
		ErrorExit("wrong argument count");

	# build corpus
	myCorpus = Corpus()

	# build categories by listing directory: sys.argv[1]
	trainDir = sys.argv[1]
	try:
		labelDataSize = int(sys.argv[3])
	except:
		labelDataSize = None
	if not os.path.isdir(trainDir):
		ErrorExit("argument <Train_dir>: %s is not a directory" % (trainDir))
	myCorpus.batchAddCategories(os.listdir(trainDir))
	# loop through all documents and build vocabulary
	for categoryName in os.listdir(trainDir):
		counter = 0
		for docName in os.listdir(os.path.join(trainDir, categoryName)):
			doc_path = os.path.join(os.path.join(trainDir, categoryName), docName)
			myCorpus.buildVocabulary(categoryName, docName, extractWordsFromFile(doc_path))
			counter += 1
			if labelDataSize != None and counter >= labelDataSize:
				break
	# print for debug
	# print myCorpus
	# print "the word 'steven' has collection freq = %d" % (myCorpus.countWord("steven"))
	# print "the word 'lin' has collection freq = %d" % (myCorpus.countWord("lin"))
	#
	# try to classify a doc
	# for i in range(1, 10):
	# 	print "Test %d classified: %s" % (i, myCorpus.classify(extractWordsFromFile("../20news/Test/%d" % (i))))
	#
	# real testing data
	testDir = sys.argv[2]
	if not os.path.isdir(testDir):
		ErrorExit("argument <Test_dir>: %s is not a directory" % (testDir))
	for i in range(1, 9420):
		print "%d %s" % (i, myCorpus.classify(extractWordsFromFile(os.path.join(testDir, str(i))))[0])

if __name__ == "__main__":
	main()

