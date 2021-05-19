import FWCore.ParameterSet.Config as cms
from CommonTools.RecoAlgos.sortedPFPrimaryVertices_cfi import sortedPFPrimaryVertices

primaryVertexAssociation = sortedPFPrimaryVertices.clone(
  qualityForPrimary = 2,
  produceSortedVertices = False,
  producePileUpCollection  = False,
  produceNoPileUpCollection = False
)
<<<<<<< HEAD:PhysicsTools/PatAlgos/python/slimming/primaryVertexAssociation_cfi.py

from Configuration.ProcessModifiers.run2_miniAOD_pp_on_AA_103X_cff import run2_miniAOD_pp_on_AA_103X
run2_miniAOD_pp_on_AA_103X.toModify(primaryVertexAssociation,particles = "cleanedParticleFlow")
primaryVertexAssociationCleaned = primaryVertexAssociation.clone(particles = "cleanedParticleFlow:removed")
=======
>>>>>>> c178d8a36c9... remove fromPV:CommonTools/RecoAlgos/python/primaryVertexAssociation_cfi.py
