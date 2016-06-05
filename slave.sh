#!/bin/bash
echo ""
echo "==================== start running ===================="
echo ""
for i in 5 20 50 80 100 150
do
	echo "---------- running with labeled-data size = ${i} ----------"
	echo ""

	echo "running naive bayes classifier ... "
	time ./naivebayes.sh  -i ../20news -o nbc_${i}_output -n ${i}
	echo "finished naive bayes classifier. (results saved as nbc_${i}_output)"
	echo ""
	echo "running EM algorithm ..."
	time ./EM.sh -i ../20news -o em_${i}_output -n ${i}
	echo "finished EM algorithm. (results saved as em_${i}_output)"
	echo ""
done

echo ""
echo "==================== finish running ===================="
echo ""
