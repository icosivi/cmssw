import FWCore.ParameterSet.Config as cms
process = cms.Process('TEST')

from CommonTools.PileupAlgos.customizePuppiTune_cff import UpdatePuppiTuneV15     



process.load('Configuration.StandardSequences.Services_cff')
# Specify IdealMagneticField ESSource (needed for CMSSW 730)
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#from Configuration.AlCa.autoCond import autoCond
#process.GlobalTag.globaltag=autoCond['run1_mc']

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.categories+=cms.untracked.vstring('MyJetAnalysis')
process.MessageLogger.cerr.FwkReport.reportEvery=cms.untracked.int32(1000)
#load the gammaJet analyzer
process.load('Calibration.HcalCalibAlgos.MyJetAnalysis_cfi')
process.load('PhysicsTools.PatAlgos.patSequences_cff')
#process.load('PhysicsTools.HepMCCandAlgos.data.genParticles_cfi')
#process.load('SimGeneral.HepPDTESSource.data.pythiapdt.cfi')

############################################
process.MyJetAnalysis.pvCollName = cms.string('offlineSlimmedPrimaryVertices4D')
process.MyJetAnalysis.pvCollName_2 = cms.string('offlineSlimmedPrimaryVertices')

process.MyJetAnalysis.svCollName = cms.string('slimmedSecondaryVertices')

process.MyJetAnalysis.patJetCollName = cms.string('slimmedJetsPuppi')
#process.MyJetAnalysis.patJetCollName = cms.string('slimmedJets')

process.MyJetAnalysis.pfJetCollName = cms.string('ak4PFJetsPuppi')
#process.MyJetAnalysis.pfJetCollName = cms.string('ak4Jets')

#process.MyJetAnalysis.genJetCollName = cms.string('ak4GenJets')
process.MyJetAnalysis.genJetCollName = cms.string('slimmedGenJets')


process.MyJetAnalysis.lheeCollName = cms.string('externalLHEProducer')
process.MyJetAnalysis.genParticleCollName = cms.string('prunedGenParticles')
process.MyJetAnalysis.packedCandidateCollName = cms.string('packedPFCandidates')

process.MyJetAnalysis.genParticleCollName_2 = cms.InputTag('genParticles:xyz0')
#############################################

process.source = cms.Source("PoolSource", 
                            fileNames = cms.untracked.vstring(
                                  
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/C939136E-2B53-A44C-A1A8-C67076CE063A.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/AE041740-2E70-6943-AD8D-80152DCB0A68.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/2E7CFFBC-FA65-2E4D-BEF3-671089055A8C.root',







  )
)

UpdatePuppiTuneV15(process)

# name of the process that used the GammaJetProd producer
process.MyJetAnalysis.prodProcess = cms.untracked.string('MYGAMMA')
process.p = cms.Path(process.MyJetAnalysis)
