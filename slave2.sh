#!/bin/bash
for i in 1 5 20 50 80 100 150
do
	echo "evaluating for labeled data size = ${i}"
	./evaluate.py ../ans.test nbc_${i}_output
	./evaluate.py ../ans.test em_${i}_output
	echo ""
done

