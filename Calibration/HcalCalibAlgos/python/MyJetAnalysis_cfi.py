import FWCore.ParameterSet.Config as cms
#from RecoJets.Configuration.RecoJets_cff import *
#from RecoJets.Configuration.RecoPFJets_cff import *
from CommonTools.ParticleFlow.pfNoPileUp_cff import *

MyJetAnalysis = cms.EDAnalyzer('MyJetAnalysis',
				  #patJetCollName      = cms.string('slimmedJetsAK8PFPuppiSoftDropPacked'),
				  patJetCollName      = cms.string('slimmedJetsPuppi'),
                                  #patJetCollName      = cms.string('slimmedJets'),
                                  pfJetCollName       = cms.string('ak4PFJetsPuppi'),
                                  #pfJetCollName       = cms.string('ak4PFJets'),
                                  #genJetCollName      = cms.string('ak4GenJets'),
				  genJetCollName      = cms.string('slimmedGenJets'),                                  
				  lheeCollName        = cms.string('externalLHEProducer'),
                                  genParticleCollName = cms.string('prunedGenParticles'),
				  genParticleCollName_2 = cms.InputTag('genParticles:xyz0'),
				  packedCandidateCollName = cms.string('packedPFCandidates'),
                                  pvCollName = cms.string('offlineSlimmedPrimaryVertices4D'),
			          pvCollName_2 = cms.string('offlineSlimmedPrimaryVertices'),
                                  #pvCollName = cms.string('offlinePrimaryVertices'),
                                  #svCollName = cms.string('slimmedSecondaryVertices'),
				  svCollName = cms.string('inclusiveSecondaryVertices'),
				  prodProcess = cms.untracked.string('reRECO'),
                                  doPFJets            = cms.bool(True),
                                  doGenJets           = cms.bool(True),                                                                                                    
                                  )
from Configuration.Eras.Modifier_stage2L1Trigger_cff import stage2L1Trigger
#stage2L1Trigger.toModify(MyJetAnalysis, stageL1Trigger = 2)
