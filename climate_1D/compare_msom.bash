#!/bin/bash

# checks for repeatabilty in training runs

YEAR=2022
NEPOCHS=30
RATE=0.300000 # must have 6 decimal points
INIT=random   # pca or random
SIGMA=1.5
MSOMDIR=../data/1D/$YEAR/msom
FILE=../data/1D/$YEAR/$YEAR\_zahists.npy
NORM=zanorm     # nonorm, zanorm, zpnorm
DECAY=linear

# ----------------------------------------------------------------
TARGETDIR=$MSOMDIR/$RATE\_$NEPOCHS\_$DECAY\_$NORM

# in case first time
if ! [ -d $TARGETDIR ]; then
    mkdir -p $TARGETDIR 
fi

# write parameters to results file
echo "YEAR=${YEAR}" > $TARGETDIR/results_$RATE\_$NEPOCHS.txt
echo "NEPOCHS=${NEPOCHS}" >> $TARGETDIR/results_$RATE\_$NEPOCHS.txt
echo "RATE=${RATE}" >> $TARGETDIR/results_$RATE\_$NEPOCHS.txt
echo "INIT=${INIT}" >> $TARGETDIR/results_$RATE\_$NEPOCHS.txt
echo "SIGMA=${SIGMA}" >> $TARGETDIR/results_$RATE\_$NEPOCHS.txt
echo "FILE=${FILE}" >> $TARGETDIR/results_$RATE\_$NEPOCHS.txt
echo "TARGETDIR=$TARGETDIR" >> $TARGETDIR/results_$RATE\_$NEPOCHS.txt
echo "NORM=${NORM}" >> $TARGETDIR/results_$RATE\_$NEPOCHS.txt
echo "DECAY=${DECAY}" >> $TARGETDIR/results_$RATE\_$NEPOCHS.txt
echo " " >> $TARGETDIR/results_$RATE\_$NEPOCHS.txt

# write to terminal
echo "compare_msom: generating the initial cluster and labels"
COUNT=0
./train_msom.py -o $TARGETDIR -e $NEPOCHS -r $RATE -t $COUNT -s $SIGMA -i $INIT -f $FILE -d $DECAY

echo "compare_msom: classifying initial data: ../data/1D/${YEAR}/${INFILE} with ${TARGETDIR}/${RATE}_${NEPOCHS}_${COUNT}.labels"
somclass -f $TARGETDIR/$RATE\_$NEPOCHS\_$COUNT.labels < $FILE > $TARGETDIR/$RATE\_$NEPOCHS\_$COUNT.npy
echo "compare_msom: finished classifying ${INFILE}"

# generate more clusters for comparisons
((COUNT++))
while [ $COUNT -lt 10 ]; do

    echo "#---------------------------------------------"
    echo " "
    echo "compare_msom: processing count: $COUNT"
    echo " "
    echo "#---------------------------------------------"

    # cluster the same data (train) again
    ./train_msom.py -o $TARGETDIR -e $NEPOCHS -r $RATE -t $COUNT -s $SIGMA -i $INIT -f $FILE -d $DECAY

    echo "compare_msom: classifying initial data: $FILE with ${TARGETDIR}/${RATE}_${NEPOCHS}_${COUNT}.labels"
    somclass -f $TARGETDIR/$RATE\_$NEPOCHS\_$COUNT.labels < $FILE > $TARGETDIR/$RATE\_$NEPOCHS\_$COUNT.npy
    echo "compare_msom: finished classifying $FILE"

    echo "compare_msom: comparing images"
    ../bin/show_diff.py -f $TARGETDIR/$RATE\_$NEPOCHS\_0 -s $TARGETDIR/$RATE\_$NEPOCHS\_$COUNT -l $POLI_HOME/luts/cetin.lut 2>> $TARGETDIR/results_$RATE\_$NEPOCHS.txt
 
    ((COUNT++))
done
