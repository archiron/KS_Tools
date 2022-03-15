#!/bin/sh
# This file is called ./zee_flow.sh 11_3_0_pre4

if [ "$1" == "" ] 
then
	echo "zee_flow.sh has no argument"
	exit
fi

echo "chemin START : $1"
echo "chemin WORK : $2"
echo "result folder : $3"

#cd $LOG_SOURCE
cd $1
#source /afs/cern.ch/cms/cmsset_default.sh
eval `scramv1 runtime -sh`
cd -

cd $2
#python3 $1/reduceSize.py
#echo "executing $1/reduceSize.py"
#python3 $1/extractValues.py
#echo "executing $1/extractValues.py"
#python3 $1/createFiles.py
#echo "executing $1/reduccreateFileseSize.py"
python3 $1/zeeMapDiff.py
#echo "executing $1/zeeMapDiff.py"

