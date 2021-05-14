#ifndef Calibration_HcalCalibAlgos_MyJetAnalysis_H_
#define Calibration_HcalCalibAlgos_MyJetAnalysis_H_

// system include files
#include <memory>
#include <string>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Candidate/interface/VertexCompositePtrCandidate.h"
#include "DataFormats/EgammaCandidates/interface/PhotonFwd.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/HcalRecHit/interface/HBHERecHit.h"
#include "DataFormats/HcalRecHit/interface/HFRecHit.h"
#include "DataFormats/HcalRecHit/interface/HORecHit.h"
#include "DataFormats/METReco/interface/METCollection.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlockFwd.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlock.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowReco/interface/PFCluster.h"
#include "DataFormats/ParticleFlowReco/interface/PFRecHit.h"
#include "DataFormats/ParticleFlowReco/interface/PFRecHitFwd.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BTauReco/interface/SecondaryVertexTagInfo.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/HcalTowerAlgo/interface/HcalGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"

#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

#include "HLTrigger/HLTcore/interface/HLTPrescaleProvider.h"
#include <TTree.h>
//#include "PositionVector3D.h"


// forward declarations
class TH1F;
//class TH2D;
class TFile;
//class TTree;


// --------------------------------------------
// Main class
// --------------------------------------------

class MyJetAnalysis : public edm::EDAnalyzer {
public:
  explicit MyJetAnalysis(const edm::ParameterSet&);
  ~MyJetAnalysis();

private:
  virtual void beginJob();  //(const edm::EventSetup&);
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();
  
  TFile *rootfile = new TFile("VBF_long_pruned_zMC.root","RECREATE");
  TTree *OutTree = new TTree("Analysis","Analysis");

  
  //std::string pfJetCollName_;        // label for the PF jet collection

  std::string patJetCollName_; 
  std::string genJetCollName_;       // label for the genjet collection
  //std::string genParticleCollName_;  // label for the genparticle collection
  std::string pvCollName_;
  std::string pvCollName2_;

  std::string svCollName_;

  std::string lhee_;
  std::string genp_;
  std::string packed_;

  edm::InputTag genp2_;

  //Tokens
  
  edm::EDGetTokenT<std::vector<pat::Jet> > tok_PATJet_;
  
  //edm::EDGetTokenT<reco::PFJetCollection> tok_PFJet_;
  edm::EDGetTokenT<std::vector<reco::GenJet> > tok_GenJet_;
  
  edm::EDGetTokenT<std::vector<reco::Vertex> > tok_PV_;
  edm::EDGetTokenT<std::vector<reco::Vertex> > tok_PV2_;

  edm::EDGetTokenT<std::vector<reco::VertexCompositePtrCandidate> > tok_SV_;

  edm::EDGetTokenT< LHEEventProduct > lhep_token;
  edm::EDGetTokenT< std::vector<reco::GenParticle> > genp_token;
  edm::EDGetTokenT< std::vector<pat::PackedCandidate> > packed_token;

  //edm::EDGetTokenT< ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> > genp_token_2;
  edm::EDGetTokenT< math::XYZPointF > genp_token_2;


  //int runNumber;
  int eventNumber;
  int ngen_jet;
  int npat_jet;
  int PV_number;

  //int ntracks;
  float z_MC;
  float z_4d;
  float mc_pointing_difference;
  float vtx_time;
  float vtx_time_error;

  //std::vector<float> z_SV;

  std::vector<float> Gen_pt;
  std::vector<float> Pat_pt;
  std::vector<float> DeltaR;
  //std::vector<float> Gen_pz;
  //std::vector<float> Pat_pz;
  std::vector<float> Gen_energy;
  std::vector<float> Pat_energy;
  //std::vector<float> PF_pt;
  std::vector<float> Gen_eta;
  std::vector<float> Pat_eta;
  //std::vector<float> PF_eta;
  std::vector<float> Gen_phi;
  std::vector<float> Pat_phi;
  std::vector<bool> Pat_bTagger;
  std::vector<float> Pat_bScore;
  //std::vector<float> PF_phi;
  
  std::vector<float> Pruned_pt;
  std::vector<float> Pruned_eta;
  std::vector<float> Pruned_phi;
  std::vector<int> Pruned_partonFlav;
  std::vector<int> Pruned_mother_partonFlav;

  //std::vector<int> Pat_partonFlav;
  //std::vector<int> Gen_partonFlav;

  std::vector<std::vector<float>> PF_candTime;
  std::vector<std::vector<float>> PF_candTime_error;
  std::vector<std::vector<float>> PF_timediff;
  std::vector<std::vector<float>> PF_sigmat;
  //std::vector<std::vector<float>> PF_candPt;
  //std::vector<std::vector<float>> PF_candEta;
  //std::vector<std::vector<float>> PF_candPhi;

 
  double deltaR(const pat::Jet* j1, const reco::Jet* j2);

};

#endif
