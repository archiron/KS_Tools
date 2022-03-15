#!/bin/bash

#RESULTFOLDER='/sps/cms/chiron/CMSSW_12_1_0_pre5-16c-1'
RESULTFOLDER='/sps/cms/chiron/9000-test3'
number=1000

for value in $(seq -f "%03g" 750 949)
do
newValue=$[$value-250]
echo "newValue : $newValue"
#name=$RESULTFOLDER'/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO_'$number'_'$value'b.root'
newName=$RESULTFOLDER'/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO_'$number'_'$newValue'.root'
echo "newName : $newName"

if [ ! -f "$name" ]; then
    echo "$name does not exist."
    echo "$value"
else
    mv $name $newName
fi
done
echo All done

