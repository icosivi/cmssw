import FWCore.ParameterSet.Config as cms
#process = cms.Process('TEST')
task = cms.Task()

from Configuration.StandardSequences.Eras import eras
process = cms.Process("USER", eras.Phase2C11)

from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection

#from Configuration.StandardSequences.Eras import eras
#process = cms.Process("USER", eras.Phase2C11)

#############################################
process.load('Configuration.StandardSequences.Services_cff')
#process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.Geometry.GeometryDD4hepExtended2026D76_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = "113X_mcRun4_realistic_v7"
process.load('FWCore.MessageService.MessageLogger_cfi')
#process.MessageLogger.categories+=cms.untracked.vstring('MyJetAnalysis')
process.MessageLogger.cerr.FwkReport.reportEvery=cms.untracked.int32(10000)
process.load('Calibration.HcalCalibAlgos.MyJetAnalysis_cfi')
process.load('PhysicsTools.PatAlgos.patSequences_cff')

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
from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask, addToProcessAndTask
task_puppi = getPatAlgosToolsTask(process)
from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD
makePuppiesFromMiniAOD(process,True)
process.puppi.useExistingWeights = False
process.puppiNoLep.useExistingWeights = False
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

runMetCorAndUncFromMiniAOD(process,isData=False,metType="Puppi",postfix="Puppi",jetFlavor="AK4PFPuppi",recoMetFromPFCs=True)
from PhysicsTools.PatAlgos.patPuppiJetSpecificProducer_cfi import patPuppiJetSpecificProducer
addToProcessAndTask('patPuppiJetSpecificProducer', patPuppiJetSpecificProducer.clone(src=cms.InputTag("patJetsPuppi")), process, task_puppi)

#process.MyJetAnalysis.patJetCollName = cms.string('slimmedJetsPuppi')

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
updateJetCollection(process, labelName = 'PuppiJetSpecific', jetSource = cms.InputTag('patJetsPuppi'),)
process.updatedPatJetsPuppiJetSpecific.userData.userFloats.src = ['patPuppiJetSpecificProducer:puppiMultiplicity',
                                                                  'patPuppiJetSpecificProducer:neutralPuppiMultiplicity', 
                                                                  'patPuppiJetSpecificProducer:neutralHadronPuppiMultiplicity',
                                                                  'patPuppiJetSpecificProducer:photonPuppiMultiplicity',
                                                                  'patPuppiJetSpecificProducer:HFHadronPuppiMultiplicity',
                                                                  'patPuppiJetSpecificProducer:HFEMPuppiMultiplicity' ]
addToProcessAndTask('slimmedJetsPuppi', process.updatedPatJetsPuppiJetSpecific.clone(), process, task_puppi)
del process.updatedPatJetsPuppiJetSpecific
process.puppiSequence = cms.Sequence(process.puppiMETSequence+process.fullPatMetSequencePuppi+process.patPuppiJetSpecificProducer+process.slimmedJetsPuppi)

#This following part allows you to adjust the cuts made for dz and timing to assign a particle to a vertex:
process.packedPrimaryVertexAssociationJME.assignment.useVertexFit = False
process.packedPrimaryVertexAssociationJME.assignment.maxDzSigForPrimaryAssignment = 5
process.packedPrimaryVertexAssociationJME.assignment.maxDzForPrimaryAssignment = 0.1
process.packedPrimaryVertexAssociationJME.assignment.maxDzErrorForPrimaryAssignment = 0.05 
process.packedPrimaryVertexAssociationJME.assignment.OnlyUseFirstDz = True
process.pfCHS.vertexAssociationQuality = 6

#For adding also timing information:
#process.puppi.vertexName = cms.InputTag('offlineSlimmedPrimaryVertices4D')  #if dz+timing
process.puppi.vertexName = cms.InputTag('offlineSlimmedPrimaryVertices')  # only if dz used (and not timing) because comparison with PUPPIv15 is more fair
process.packedPrimaryVertexAssociationJME.assignment.useTiming = False
process.packedPrimaryVertexAssociationJME.assignment.maxDtSigForPrimaryAssignment = 5
process.packedPrimaryVertexAssociationJME.vertices = cms.InputTag('offlineSlimmedPrimaryVertices4D')

#############################################
#process.load('Configuration.StandardSequences.Services_cff')
#process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
#process.load("Configuration.Geometry.GeometryDD4hepExtended2026D76_cff")
#process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
#process.GlobalTag.globaltag = "113X_mcRun4_realistic_v7"
#process.load('FWCore.MessageService.MessageLogger_cfi')
#process.MessageLogger.categories+=cms.untracked.vstring('MyJetAnalysis')
#process.MessageLogger.cerr.FwkReport.reportEvery=cms.untracked.int32(10000)
#process.load('Calibration.HcalCalibAlgos.MyJetAnalysis_cfi')
#process.load('PhysicsTools.PatAlgos.patSequences_cff')

############################################
#process.MyJetAnalysis.pvCollName = cms.string('offlineSlimmedPrimaryVertices4D')
#process.MyJetAnalysis.pvCollName_2 = cms.string('offlineSlimmedPrimaryVertices')

#process.MyJetAnalysis.svCollName = cms.string('slimmedSecondaryVertices')

#process.MyJetAnalysis.patJetCollName = cms.string('slimmedJetsPuppi')
#process.MyJetAnalysis.patJetCollName = cms.string('slimmedJets')

#process.MyJetAnalysis.pfJetCollName = cms.string('ak4PFJetsPuppi')
#process.MyJetAnalysis.pfJetCollName = cms.string('ak4Jets')

#process.MyJetAnalysis.genJetCollName = cms.string('ak4GenJets')
#process.MyJetAnalysis.genJetCollName = cms.string('slimmedGenJets')


#process.MyJetAnalysis.lheeCollName = cms.string('externalLHEProducer')
#process.MyJetAnalysis.genParticleCollName = cms.string('prunedGenParticles')
#process.MyJetAnalysis.packedCandidateCollName = cms.string('packedPFCandidates')

#process.MyJetAnalysis.genParticleCollName_2 = cms.InputTag('genParticles:xyz0')

############################################
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
# comment out the lines below to get back to default PUPPI v11
process.p.associate(task)
#process.p.associate(task_puppi)
process.p.associate(process.patAlgosToolsTask)
