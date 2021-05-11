# KS_Tools
scripts to generate ROOT files for KS study.  
add Generation-Extraction scripts (GenExtract folder)

installing tools with : . installKSTools.sh (WARNING no / between the . and installKSTools.sh).  
### Generation of the ROOT files
#### cca.in2p3.fr
#### polui.in2p3.fr

### Extraction of the files
you need to load 2 files more :
the 2 files for the current validation [1] and put them into the DATA folder.  
launch the extraction with : python zeeExtract_1curve.py

####Some point to modify into the zeeExtract_1curve.py file :
the folderName where are located the generated ROOT files,
the folder where the created files were located (into the func_CreateKS() function).



[1] : usually into the form : DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_3_0_pre6-113X_mcRunxxxxxxxx-v1__DQMIO.root
