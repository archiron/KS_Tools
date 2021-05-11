#!/bin/sh
# This file is called ./zee_flow_init.sh

LOG_SOURCE='/pbs/home/c/chiron/private/ZEE_Flow/CMSSW_11_3_0_pre4/src/'
LOG_OUTPUT='/sps/cms/chiron/TEMP/'
RESULTFOLDER='/sps/cms/chiron/CMSSW_11_3_0_pre4-16c'
NB_EVTS=9000

echo "LOG_SOURCE : $LOG_SOURCE"

cd $LOG_SOURCE
#source /afs/cern.ch/cms/cmsset_default.sh
eval `scramv1 runtime -sh`
cd -
for (( i=0; i<1; i++ )) 
do
   qsub -l sps=1 -P P_cmsf -pe multicores 16 -q mc_long -o $LOG_OUTPUT zee_flow.sh $i $LOG_SOURCE $NB_EVTS $RESULTFOLDER
done

