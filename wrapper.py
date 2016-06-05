#!/usr/bin/python
#
# wrapper.py
#
# this file will output the makefile command corresponding to shell command
#
import sys, os

if __name__ == "__main__":
	command = "make"

	# check which makefile rule to apply
	which = 0
	if "naive" in sys.argv[1]:
		command += " NBC"
		which = 1
	elif "EM" in sys.argv[1]:
		command += " EM"
		which = 2
	else:
		sys.exit(-1) # error occurred
	
	# get the parameter
	train = None
	unlabel = None
	test = None
	labelsize = None
	outfile = None
	for i in range(2, len(sys.argv)):
		if sys.argv[i] == "-i":
			train = os.path.join(sys.argv[i+1], "Train")
			unlabel = os.path.join(sys.argv[i+1], "Unlabel")
			test = os.path.join(sys.argv[i+1], "Test")
		if sys.argv[i] == "-o":
			outfile = sys.argv[i+1]
		if sys.argv[i] == "-n":
			labelsize = sys.argv[i+1]
	
	# form the final command
	command += " TRAIN_DIR=%s" % (train)
	if which == 2:
		command += " UNLABEL_DIR=%s" % (unlabel)
	command += " TEST_DIR=%s" % (test)
	if labelsize:
		command += " LABEL_SIZE=%s" % (labelsize)
	command += " OUT_FILE=%s" % (outfile)

	# output command to stdout
	print command
