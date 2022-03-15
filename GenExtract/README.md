# KS_Tools
scripts to generate ROOT files for KS study.  
add Generation-Extraction scripts (GenExtract folder)

installing tools with : . installKSTools.sh (WARNING no / between the . and installKSTools.sh).  
### Generation of the ROOT files
When you have downloaded the config (python) files from https://cmsweb.cern.ch/reqmgr2/ site,
you save them into step1,.py, step2.py and so on.
for each file you need to include the part 1 [0] between the line "from configuration ..." and the line
"process = cms.Process(...".
in most of the files you need to replace :  
process.options.numberOfThreads = 1  
with   
process.options.numberOfThreads = 16 (or 8 if you are on polui machine). 
By the end you need to include :
process.dqmSaver.workflow = '/Global/CMSSW_X_Y_Z/RECO_' + '%0004d'%max_number + '_' + '%003d'%ind
into the last step file.

Into most of the files, it is recommended to include :  
fileName = cms.untracked.string('file:step3_inDQM_' + '%0004d'%max_number + '_' + '%003d'%ind + '.root'),  
into the process.DQMoutput part.  
Be careful, sometimes it is difficult on the POLUI computers.  

#### cca.in2p3.fr
#### polui.in2p3.fr

### Extraction of the files
you need to load 2 files more :
the 2 files for the current validation [1] and put them into the DATA folder.  
launch the extraction with : python zeeExtract_1curve.py  
####WARNING : still need of cmsenv!  

####Some point to modify into the zeeExtract_1curve.py file :
the folderName where are located the generated ROOT files,
the folder where the created files were located (into the func_CreateKS() function).

[0] : part 1  
if len(sys.argv) > 1:  
    print "step 1 - arg. 0 :", sys.argv[0]  
    print "step 1 - arg. 1 :", sys.argv[1]  
    print "step 1 - arg. 2 :", sys.argv[2]  
    print "step 1 - arg. 3 :", sys.argv[3]  
    print "step 1 - arg. 4 :", sys.argv[4]   
    ind = int(sys.argv[2])  
    path = str(sys.argv[3])  
    max_number = int(sys.argv[4])  
else:  
    print "step 1 - rien"  
    ind = 0  
    path = ''  
    max_number = 10 # number of events  



[1] : usually into the form : DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_3_0_pre6-113X_mcRunxxxxxxxx-v1__DQMIO.root
