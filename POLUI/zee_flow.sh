#!/bin/sh
# This file is called ./zee_flow.sh

if [ "$1" == "" ] 
then
	echo "zee_flow.sh has no argument"
	exit
fi

echo "nb : $1"
echo "chemin : $2"
echo "nb evts : $3"
echo "result folder : $4"

LOG_SOURCE=$2
echo "Step 1 in : $LOG_SOURCE"
echo "Step 1 in : $2"

#cd $LOG_SOURCE
cd $2
#source /afs/cern.ch/cms/cmsset_default.sh
eval `scramv1 runtime -sh`
cd -

cmsRun $2/step2.py $1 $2 $3

cmsRun $2/step3.py $1 $2 $3
ls
echo '=='
rm step2*.root
ls
echo '=='

cmsRun $2/step4.py $1 $2 $3
rm step3*.root
ls
echo '=='

