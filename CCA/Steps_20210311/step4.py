# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step4 --filetype DQM --mc --conditions auto:run2_mc --era Run2_2016 -s HARVESTING:@standardValidationNoHLT+@standardDQMFakeHLT+@miniAODValidation+@miniAODDQM+@L1TEgamma --io HARVESTUP15_L1TEgDQM.io --python HARVESTUP15_L1TEgDQM.py --conditions=110X_mcRun2_asymptotic_v5 -n 9000 --filein file:step3_inDQM.root --fileout file:step4.root
import FWCore.ParameterSet.Config as cms
import os, sys

from Configuration.Eras.Era_Run2_2016_cff import Run2_2016

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

process = cms.Process('HARVESTING',Run2_2016)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.DQMSaverAtRunEnd_cff')
process.load('Configuration.StandardSequences.Harvesting_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(max_number),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("DQMRootSource",
    #fileNames = cms.untracked.vstring('file:step3_inDQM.root')
    fileNames = cms.untracked.vstring('file:step3_inDQM_' + '%0004d'%max_number + '_' + '%003d'%ind + '.root'),
    #fileNames = cms.untracked.vstring('file:' + path + '/step3_inDQM_' + '%0004d'%max_number + '_' + '%003d'%ind + '.root'),
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring('ProductNotFound'),
    SkipEvent = cms.untracked.vstring(),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(

        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(1)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(1),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step4 nevts:9000'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '110X_mcRun2_asymptotic_v5', '')

# Path and EndPath definitions
process.genHarvesting = cms.Path(process.postValidation_gen)
process.validationHarvestingHI = cms.Path(process.postValidationHI)
process.dqmHarvestingExtraHLT = cms.Path(process.DQMOffline_SecondStep_ExtraHLT+process.DQMOffline_Certification)
process.alcaHarvesting = cms.Path()
process.validationHarvestingFS = cms.Path(process.recoMuonPostProcessors+process.postValidationTracking+process.MuIsoValPostProcessor+process.calotowersPostProcessor+process.hcalSimHitsPostProcessor+process.hcaldigisPostProcessor+process.hcalrechitsPostProcessor+process.electronPostValidationSequence+process.photonPostProcessor+process.pfJetClient+process.pfMETClient+process.pfJetResClient+process.pfElectronClient+process.rpcRecHitPostValidation_step+process.makeBetterPlots+process.bTagCollectorSequenceMCbcl+process.METPostProcessor+process.L1GenPostProcessor+process.bdHadronTrackPostProcessor+process.postValidation_gen)
process.validationpreprodHarvesting = cms.Path(process.postValidation_preprod+process.hltpostvalidation_preprod+process.postValidation_gen)
process.validationprodHarvesting = cms.Path(process.hltpostvalidation_prod+process.postValidation_gen)
process.validationHarvesting = cms.Path(process.postValidation+process.hltpostvalidation+process.postValidation_gen)
process.validationpreprodHarvestingNoHLT = cms.Path(process.postValidation_preprod+process.postValidation_gen)
process.dqmHarvestingPOGMC = cms.Path(process.DQMOffline_SecondStep_PrePOGMC)
process.dqmHarvesting = cms.Path(process.DQMOffline_SecondStep+process.DQMOffline_Certification)
process.DQMHarvestMiniAOD_step = cms.Path(process.DQMHarvestMiniAOD)
process.DQMHarvestL1TEgamma_step = cms.Path(process.DQMHarvestL1TEgamma)
process.dqmSaver.workflow = '/Global/CMSSW_X_Y_Z/RECO_' + '%0004d'%max_number + '_' + '%003d'%ind
process.dqmsave_step = cms.Path(process.DQMSaver)

# Schedule definition
process.schedule = cms.Schedule(process.validationHarvestingNoHLT,process.dqmHarvestingFakeHLT,process.validationHarvestingMiniAOD,process.DQMHarvestMiniAOD_step,process.DQMHarvestL1TEgamma_step,process.dqmsave_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
