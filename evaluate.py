#!/usr/bin/python
# -*- coding: utf8 -*-
import sys, os


def print_usage():
	print >> sys.stderr, "Usage:"
	print >> sys.stderr, "\t" + "%s <true_answer> <your_answer>" % (sys.argv[0])

def evaluate(true_path, your_path):
	"""
	evaluate the classification result
	@true_path path to the file where the true answer is
	@your_path path to the file where your answer is
	@return
	"""
	# open the 2 files
	try:
		f1 = open(true_path, "r")
		f2 = open(your_path, "r")
	except:
		print >> sys.stderr, "evaluate(): error opening file at: %s, %s" % (true_path, your_path)
	# read the 2 files (into 2 dictionary)
	truth = {} # dictionary that contains the true answer
	yours = {} # dictionary that contains your answer
	for line in f1:
		line = line.strip()
		try:
			k, v = line.split()
			truth[k] = v
		except:
			print >> sys.stderr, "(%s) cannot parse this line: %s" % (true_path, line)
	for line in f2:
		line = line.strip()
		try:
			k, v = line.split()
			yours[k] = v
		except:
			print >> sys.stderr, "(%s) cannot parse this line: %s" % (your_path, line)
	# matching
	res = {'correct': 0, 'incorrect': 0, 'ratio': 0.0}
	for k, v in truth.iteritems():
		try:
			your_v = yours[k]
			if your_v == v:
				res['correct'] += 1
			else:
				res['incorrect'] += 1
		except:
			print >> sys.stderr, "(%s) didn't provide the answer of: %s" % (your_path, k)
	res['ratio'] = float(res['correct']) / float(res['correct'] + res['incorrect'])
	return res

if __name__ == "__main__":
	# check argument count
	if len(sys.argv) != 3:
		print >> sys.stderr, "wrong arguments!"
		print_usage()
		sys.exit(-1)
	# check arguments
	true_answer_path = sys.argv[1]
	your_answer_path = sys.argv[2]
	if not os.path.isfile(true_answer_path):
		print >> sys.stderr, "wrong <true_answer> argument!"
		print_usage()
		sys.exit(-1)
	if not os.path.isfile(your_answer_path):
		print >> sys.stderr, "wrong <your_answer> argument!"
		print_usage()
		sys.exit(-1)
	res = evaluate(true_answer_path, your_answer_path)
	print res
