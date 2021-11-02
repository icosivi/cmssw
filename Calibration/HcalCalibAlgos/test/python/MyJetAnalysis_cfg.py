import FWCore.ParameterSet.Config as cms
#process = cms.Process('TEST')
task = cms.Task()

from Configuration.StandardSequences.Eras import eras
process = cms.Process("USER", eras.Phase2C11)

from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
#from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
#from CommonTools.PileupAlgos.customizePuppiTune_cff import UpdatePuppiTuneV15 

#from Configuration.StandardSequences.Eras import eras
#useData = False   
#process = cms.Process("USER", eras.Phase2C11)

#############################################
process.load('Configuration.StandardSequences.Services_cff')
#process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.Geometry.GeometryDD4hepExtended2026D76_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = "113X_mcRun4_realistic_v7"  # "112X_mcRun3_2021_realistic_v16"   "111X_mcRun4_realistic_T15_v1"
process.load('FWCore.MessageService.MessageLogger_cfi')
#process.MessageLogger.categories+=cms.untracked.vstring('MyJetAnalysis')
process.MessageLogger.cerr.FwkReport.reportEvery=cms.untracked.int32(10000)
process.load('Calibration.HcalCalibAlgos.MyJetAnalysis_cfi')
#process.load('PhysicsTools.PatAlgos.patSequences_cff')

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

#process.MyJetAnalysis.svTagInfos = cms.InputTag('slimmedSecondaryVertices')
process.MyJetAnalysis.svTagInfos = cms.string('slimmedSecondaryVertices')

############################################
#process.load('CommonTools/PileupAlgos/Puppi_cff')
# recreate PUPPI candidates for MiniAOD                                                                                                                      
# unpack stored weights to save time recalculating it                                                                                                        
#process.puppi.candName = cms.InputTag('packedPFCandidates')
#process.puppi.vertexName = cms.InputTag('offlineSlimmedPrimaryVertices')
#process.puppi.clonePackedCands = cms.bool(True)
#process.puppi.puppiDiagnostics = cms.bool(False)

#default                                                                                       
#process.puppi.useExistingWeights = cms.bool(True)
# v15: changed to false since we want to recalculate PUPPI and also weights
#process.puppi.useExistingWeights = cms.bool(False)
#UpdatePuppiTuneV15(process, not useData)

#task.add(process.puppi)


#############################################
#process.ak4PuppiJets  = ak4PFJets.clone (src = 'puppi', doAreaFastjet = True, jetPtMin = 2.)
#task.add(process.ak4PuppiJets)

#addJetCollection(process,labelName = 'Ak4PuppiJets', jetSource = cms.InputTag('ak4PuppiJets'), algo = 'AK', rParam=0.4, 
#	             genJetCollection=cms.InputTag('slimmedGenJets'), jetCorrections =('AK4PFPuppi', ['L1FastJet', 'L2Relative', 'L3Absolute'],'None'),#
#	             pfCandidates = cms.InputTag('packedPFCandidates'),
#                 pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
#                 svSource = cms.InputTag('slimmedSecondaryVertices'),
#                 muSource =cms.InputTag( 'slimmedMuons'),
#                 elSource = cms.InputTag('slimmedElectrons')
#                     )

#process.MyJetAnalysis.PuppiCollName = cms.InputTag('patJetsAk4PuppiJets')

#############################################
process.source = cms.Source("PoolSource", 
                            fileNames = cms.untracked.vstring(
  
'/store/mc/Phase2Spring21DRMiniAOD/VBFHHTo4B_CV_1_C2V_2_C3_1_TuneCP5_14TeV-madgraph-pythia8/MINIAODSIM/PU200Phase2D76_WMLHE_113X_mcRun4_realistic_v7_ext1-v1/280000/5d302ffb-0b04-448b-b617-f62f0f696cb2.root',
#'/store/mc/Phase2Spring21DRMiniAOD/VBFHHTo4B_CV_1_C2V_2_C3_1_TuneCP5_14TeV-madgraph-pythia8/MINIAODSIM/PU200Phase2D76_WMLHE_113X_mcRun4_realistic_v7_ext1-v1/280000/c87dfc0b-1fe2-46db-b876-dfdff2ce433b.root',
#'/store/mc/Phase2Spring21DRMiniAOD/VBFHHTo4B_CV_1_C2V_2_C3_1_TuneCP5_14TeV-madgraph-pythia8/MINIAODSIM/PU200Phase2D76_WMLHE_113X_mcRun4_realistic_v7_ext1-v1/280000/143f7244-5d33-4792-8f95-c4467c53fbe5.root',
#'/store/mc/Phase2Spring21DRMiniAOD/VBFHHTo4B_CV_1_C2V_2_C3_1_TuneCP5_14TeV-madgraph-pythia8/MINIAODSIM/PU200Phase2D76_WMLHE_113X_mcRun4_realistic_v7_ext1-v1/280000/25f5d357-9910-4e26-9641-b2938ac1197c.root',
#'/store/mc/Phase2Spring21DRMiniAOD/VBFHHTo4B_CV_1_C2V_2_C3_1_TuneCP5_14TeV-madgraph-pythia8/MINIAODSIM/PU200Phase2D76_WMLHE_113X_mcRun4_realistic_v7_ext1-v1/280000/5fd7a9c1-ad73-457b-a10f-44a1b6f4248d.root',
#'/store/mc/Phase2Spring21DRMiniAOD/VBFHHTo4B_CV_1_C2V_2_C3_1_TuneCP5_14TeV-madgraph-pythia8/MINIAODSIM/PU200Phase2D76_WMLHE_113X_mcRun4_realistic_v7_ext1-v1/280000/cace1549-7b8f-4b1b-9900-1c22cb221201.root',
#'/store/mc/Phase2Spring21DRMiniAOD/VBFHHTo4B_CV_1_C2V_2_C3_1_TuneCP5_14TeV-madgraph-pythia8/MINIAODSIM/PU200Phase2D76_WMLHE_113X_mcRun4_realistic_v7_ext1-v1/280000/301d6d82-e868-4575-b4b7-8428579bd444.root',
#'/store/mc/Phase2Spring21DRMiniAOD/VBFHHTo4B_CV_1_C2V_2_C3_1_TuneCP5_14TeV-madgraph-pythia8/MINIAODSIM/PU200Phase2D76_WMLHE_113X_mcRun4_realistic_v7_ext1-v1/280000/5613365f-3a73-4d61-a1f7-43b66062094f.root',
#'/store/mc/Phase2Spring21DRMiniAOD/VBFHHTo4B_CV_1_C2V_2_C3_1_TuneCP5_14TeV-madgraph-pythia8/MINIAODSIM/PU200Phase2D76_WMLHE_113X_mcRun4_realistic_v7_ext1-v1/280000/93b6162b-1cbe-4d91-b1fc-75503ed79650.root',
                                
  )
)

# name of the process that used the GammaJetProd producer
process.MyJetAnalysis.prodProcess = cms.untracked.string('MYGAMMA')
process.p = cms.Path(process.MyJetAnalysis)
process.p.associate(task)
#process.p.associate(process.patAlgosToolsTask)
