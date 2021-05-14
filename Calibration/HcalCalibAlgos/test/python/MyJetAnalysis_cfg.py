import FWCore.ParameterSet.Config as cms
process = cms.Process('TEST')


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

#process.MyJetAnalysis.svCollName = cms.string('slimmedSecondaryVertices')
process.MyJetAnalysis.svCollName = cms.string('inclusiveSecondaryVertices')
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
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/2BA203FF-32BA-074A-A785-1588ED4B5F9B.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/72C56AE1-D130-1D4D-A492-5B7C69846FE4.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/7FF222C5-8440-C34D-9AEC-683F3DEA412A.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/CF83A4DA-6AE8-EA40-A3B0-901E996CC3ED.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/3D50C4EC-B560-784F-B3F9-639EF9D1D30A.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/7A7D4259-1614-4249-B98F-CE3BB10F5074.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/A2625481-745B-B845-953B-63B64832A465.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/E480E010-110A-FC42-A7B5-790355BAE297.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/DA55841A-E0AB-6A47-9D24-C275EF2F182C.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/180C0E41-CF8A-DA44-B9FF-ACC9611BE479.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/C3B5B040-55B2-8C4B-BF49-52DCDEDE67BB.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/382F732D-8B2E-4041-AC8D-A39AB8D7D120.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/585F6E11-5DD0-8F43-AF87-32F507204008.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/E0047890-EC16-9D43-B34A-4B135127E5CE.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/731A878F-796B-F840-B5B5-ED1C46E2C668.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/C67DB156-B01C-FD4F-875D-D36C25F9AAB6.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/E63D8003-1963-204E-9E0B-9219599DB1EA.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/DDBA87DF-9096-444E-8D58-96D18DC787F4.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/024FA442-9AD0-2848-AB89-9E5F2899D430.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/32A50734-F98E-F541-9C68-BF3CB71CEAB6.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/BE43E726-026E-5243-8D5B-51030F9A8D05.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/27EAD81B-735C-AE44-92D9-0992911432F2.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/B8994F8C-79AA-8E49-B06A-E9C7B0CA3578.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/3D066648-D3B8-B44B-B42F-03D24C16B974.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/924B021B-2E31-634D-AA95-AAFB113E08CF.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/7BD6BB9A-AE0B-D642-848D-D0AC015C44C7.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/30561A4C-03D2-0148-8484-9A23620A56FB.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/EEBF5C56-999E-6346-9D1C-D45A45ACDC66.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/719FCEAB-362F-6543-A8F9-3E1FCCAD011A.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/270000/3C8BC73D-66F0-9F40-BFBA-93E5D22558F1.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/270000/619F8234-DDB6-7148-9293-F14883E71F0C.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/270000/C00DA535-9FE1-644E-B610-43090AE09E69.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/7FF5DD80-CF53-2A42-B349-252D6167BDD6.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/C06E151E-06D5-4F4B-8B7C-E217202D2F6C.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/75EC07BC-8587-0E45-A2B6-893546C0E610.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/6E0861A8-A1A9-3E4C-A265-B070CE510966.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/5911DB02-BBD7-2A48-A88D-73AEB7840BFF.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/CD3BA0AB-0EA0-E842-8B24-01DC9076F3D8.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/F757381B-6651-E341-B3A5-9599DCE62D66.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/73F01E7E-60DB-C048-A82B-9A8F7D079C76.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/2E047667-2311-4E43-BFEA-B737218B63C5.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/6EB00C68-BE01-C14E-AD8A-CF09F2FE1019.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/6572E4F9-4BE7-4143-A1B4-AF69DB8FEAE1.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/5276D3D0-BA0C-3F46-9643-BD5BB7EE7958.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/8250AD58-41A2-0F4E-AC01-AA5D66719A60.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/7025FB73-0083-5C4F-AD1C-E8907DB9F65E.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/20000/6573CB7D-AE92-8B48-8D8F-61404C3C442D.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/270000/45C1EF09-512E-6848-ACAA-BC3DF41B5469.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/270000/EF41BBB4-9926-C141-A1D3-9F6FE3F98813.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/270000/A40E9F03-7FF0-2144-9909-30A050402CF9.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/270000/E055D309-6A4E-7E45-A22B-13ACE6DB6464.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/75F723C7-E79A-C648-9CCE-E636C1DE22B0.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/5C713E40-8FA4-A347-9F03-C3F14F34417E.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/089376B6-A8D0-B94C-AB90-A828044A5E4F.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/95BAEC70-0F5C-4F49-B76C-FC956354D0D8.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/3F305972-9E0B-014E-B87E-DFBC4E23D516.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/5601E7EB-992F-0C4D-B0B6-5D2E0C1F9197.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/31BA5289-5D19-7A4B-9D2B-E8B0C83CF762.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/385264E7-D943-CF47-A38C-4ADBC7DC3D38.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/EEA9C8C6-2796-C543-95C9-5C43767F9C4B.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/C3580066-04D3-BC48-8687-71E25FBC9ED3.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/CB25E7F5-FD99-BC4F-8E41-BD4CE0DCC172.root',
'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20RECOMiniAOD/VBF_HHTo4B_CV_1_C2V_1_C3_1_TuneCP5_PSWeights_14TeV-madgraph-pythia8/MINIAODSIM/PU200_110X_mcRun4_realistic_v3-v2/10000/814653B9-3B0B-8248-A0C9-26885CE7E521.root'




  )
)

# name of the process that used the GammaJetProd producer
process.MyJetAnalysis.prodProcess = cms.untracked.string('MYGAMMA')
process.p = cms.Path(process.MyJetAnalysis)
