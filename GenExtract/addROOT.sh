#!/bin/bash
# This file is called . installKSTools.sh & NOT ./installKSTools.sh
#

RELEASE="CMSSW_12_1_0_pre5"

echo "create $RELEASE"
cmsrel $RELEASE
cd $RELEASE/src
cmsenv
cd ../..
rm -rf $RELEASE

echo "end"

