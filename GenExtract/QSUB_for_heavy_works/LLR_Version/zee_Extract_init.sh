#!/bin/sh
# This file is called ./zee_flow_init.sh

LOG_SOURCE_WORK='/home/llr/info/chiron_u/PYTHON/KS_Tools/GenExtract/'
LOG_SOURCE_START='/home/llr/info/chiron_u/PYTHON/ZEE_Flow/CMSSW_12_1_0_pre5/src/Kolmogorov'

LOG_OUTPUT='/sps/cms/chiron/TEMP/'
RESULTFOLDER='/sps/cms/chiron/9000-test3' # cca
RESULTFOLDER='/data_CMS/cms/chiron/HGCAL/CMSSW_12_2_0_pre2-16c-1/' # polui

echo "LOG_SOURCE_WORK : $LOG_SOURCE_WORK"

cd $LOG_SOURCE_START
#source /afs/cern.ch/cms/cmsset_default.sh
eval `scramv1 runtime -sh`
cd -
qsub -l sps=1 -P P_cmsf -pe multicores 4 -q mc_long -o $LOG_OUTPUT zee_Extract.sh $LOG_SOURCE_WORK $RESULTFOLDER

