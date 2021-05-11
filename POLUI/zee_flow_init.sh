#!/bin/sh
# This file is called ./zee_flow_init.sh

LOG_SOURCE="/home/llr/info/chiron_u/PYTHON/ZEE_FLOW/CMSSW_11_0_0_pre13/src"
LOG_OUTPUT="/home/llr/info/chiron_u/PYTHON/ZEE_FLOW/CMSSW_11_0_0_pre13/src/TEMP"
RESULTFOLDER="/home/llr/info/chiron_u/PYTHON/ZEE_FLOW/CMSSW_11_0_0_pre13/src/Results-8c"
NB_EVTS=9000

echo "LOG_SOURCE : $LOG_SOURCE"

cd $LOG_SOURCE
#source /afs/cern.ch/cms/cmsset_default.sh
eval `scramv1 runtime -sh`
cd -
for (( i=0; i<1; i++ )) 
do
   /opt/exp_soft/cms/t3/t3submit -long -8c -singleout zee_flow.sh $i $LOG_SOURCE $NB_EVTS $RESULTFOLDER
done

