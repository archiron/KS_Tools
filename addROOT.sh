#!/bin/bash
# This file is called . installKSTools.sh & NOT ./installKSTools.sh
#

cmsrel CMSSW_12_0_0_pre2
cd CMSSW_12_0_0_pre2/src
cmsenv
cd ../..
rm -rf CMSSW_12_0_0_pre2

echo "end"
