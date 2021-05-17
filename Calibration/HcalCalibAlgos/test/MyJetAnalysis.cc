//
#include "MyJetAnalysis.h"
#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "FWCore/Utilities/interface/EDMException.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Candidate/interface/VertexCompositePtrCandidate.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BTauReco/interface/SecondaryVertexTagInfo.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
//#include "PositionVector3D.h"
#include "TTree.h"
#include "TFile.h"
#include "TH1.h"
#include "TMath.h"
#include "TClonesArray.h"
#include "TObjString.h"
#include <iostream>
#include <numeric>
#include <vector>
#include <set>
#include <map>
#include <boost/regex.hpp>


MyJetAnalysis::MyJetAnalysis(const edm::ParameterSet& iConfig){
  // set parameters
  
  //pfJetCollName_ = iConfig.getParameter<std::string>("pfJetCollName");
  //pfJetCorrName_ = iConfig.getParameter<std::string>("pfJetCorrName");

  patJetCollName_ = iConfig.getParameter<std::string>("patJetCollName");
  genJetCollName_ = iConfig.getParameter<std::string>("genJetCollName");
  
  pvCollName_ = iConfig.getParameter<std::string>("pvCollName");
  pvCollName2_ = iConfig.getParameter<std::string>("pvCollName_2");

  svCollName_ = iConfig.getParameter<std::string>("svCollName");

  lhee_ = iConfig.getParameter<std::string>("lheeCollName");
  genp_ = iConfig.getParameter<std::string>("genParticleCollName");
  genp2_ = iConfig.getParameter<edm::InputTag>("genParticleCollName_2");
  packed_ = iConfig.getParameter<std::string>("packedCandidateCollName");
  
  
  //tok_PFJet_ = consumes<reco::PFJetCollection>(pfJetCollName_);
  tok_PATJet_ = consumes<std::vector<pat::Jet>>(patJetCollName_);
  tok_GenJet_ = consumes<std::vector<reco::GenJet>>(genJetCollName_);
  tok_PV_ = consumes<std::vector<reco::Vertex>>(pvCollName_);
  tok_PV2_ = consumes<std::vector<reco::Vertex>>(pvCollName2_);

  tok_SV_ = consumes<std::vector<reco::VertexCompositePtrCandidate>>(svCollName_);

  lhep_token = consumes< LHEEventProduct >(lhee_);
  genp_token = consumes<std::vector<reco::GenParticle> >(genp_);
  packed_token = consumes< std::vector<pat::PackedCandidate> >(packed_);
  genp_token_2 = consumes< math::XYZPointF >(genp2_);

  
  

  }


MyJetAnalysis::~MyJetAnalysis() {}

//
// member functions
//

// ------------ method called to for each event  ------------
void MyJetAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& evSetup) {

  //int eventNumber = iEvent.id().event();
  //printf("event: %i \n",eventNumber);

  edm::Handle< std::vector<pat::PackedCandidate> > packedCandidate;
  iEvent.getByToken(packed_token, packedCandidate);

  edm::Handle<std::vector<reco::GenParticle> > genParticles;
  iEvent.getByToken(genp_token, genParticles);

  edm::Handle< math::XYZPointF > genParticlesPosition;
  iEvent.getByToken(genp_token_2, genParticlesPosition);

  edm::Handle< LHEEventProduct > EvtHandle ;
  iEvent.getByToken( lhep_token , EvtHandle ) ;

  edm::Handle<std::vector<reco::Vertex>> pv;
  iEvent.getByToken(tok_PV_, pv);

  edm::Handle<std::vector<reco::Vertex>> pv2;  // no-4D vertexes
  iEvent.getByToken(tok_PV2_, pv2);

  edm::Handle<std::vector<reco::VertexCompositePtrCandidate>> sv;
  iEvent.getByToken(tok_SV_, sv);

  edm::Handle<std::vector<reco::GenJet>> genjets;
  iEvent.getByToken(tok_GenJet_, genjets);

  edm::Handle<std::vector<pat::Jet>> patjets;
  iEvent.getByToken(tok_PATJet_, patjets);
  

  int vtx_counter = 0;
  //int vtx_counter2 = 0;

  //float bTaggerThreshold = 0.6321;
  //float bTaggerThreshold = 0.4184;
  std::string bTaggerName = "pfDeepCSVJetTags:probb";

  z_MC = genParticlesPosition->z();

  ///////////////////// POINTING VECTOR PART ////////////////////////////

  std::vector<float> sv_vector;
  bool tag_info_valid = false;

  for(pat::JetCollection::const_iterator it_patjet = patjets->begin(); it_patjet != patjets->end(); ++it_patjet){
    
    //const reco::SecondaryVertexTagInfo &svTagInfo = *it_patjet->tagInfoSecondaryVertex("secondaryVertex");
    //const reco::SecondaryVertexTagInfo &svTagInfo = *it_patjet->tagInfoSecondaryVertex();
    const reco::SecondaryVertexTagInfo *svTagInfo = it_patjet->tagInfoSecondaryVertex();

    if ( svTagInfo != nullptr ){

      tag_info_valid = true;
     
      const reco::Vertex &sv = it_patjet->tagInfoSecondaryVertex()->secondaryVertex(0);
      const GlobalVector &dir = it_patjet->tagInfoSecondaryVertex()->flightDirection(0);
 
      //math::XYZTLorentzVector trackFourVectorSum;

     // loop over all tracks in the vertex
     /*for (reco::Vertex::trackRef_iterator track = sv.tracks_begin(); track != sv.tracks_end(); ++track) {
       
        ROOT::Math::LorentzVector<ROOT::Math::PxPyPzM4D<double> > vec;
        vec.SetPx((*track)->px());
        vec.SetPy((*track)->py());
        vec.SetPz((*track)->pz());
        vec.SetM(0.13957);  // pion mass
        trackFourVectorSum += vec;
     }

      // get the invariant mass: sqrt(E² - px² - py² - pz²)
      double vertexMass = trackFourVectorSum.M();

      cout<<"sv mass: "<<vertexMass<<endl;*/

      float zz_sv = sv.z() - (dir.z()/dir.y())*sv.y() ;
      sv_vector.push_back( zz_sv );

    }

  }


  /*for (std::vector<reco::VertexCompositePtrCandidate>::const_iterator it_sv = sv->begin(); it_sv != sv->end(); ++it_sv){

    float zz_sv = it_sv->vz() - (it_sv->pz()/it_sv->py())*it_sv->vy() ;
    sv_vector.push_back( zz_sv );

  }*/

  int best_PV_matching = 0;
  int best_PV_counter_matching = 0;
  float z_difference_matching = 100. ;

  if(tag_info_valid){
  
    double sv_vector_sum = std::accumulate(sv_vector.begin(), sv_vector.end(), 0.0);
    double sv_vector_mean = sv_vector_sum / sv_vector.size();

    for (std::vector<reco::Vertex>::const_iterator it_pv = pv->begin(); it_pv != pv->end(); ++it_pv) {

      if( fabs( sv_vector_mean - it_pv->z() ) < z_difference_matching ){

        z_difference_matching = fabs( sv_vector_mean - it_pv->z() );
        best_PV_matching = best_PV_counter_matching ;

      }

      best_PV_counter_matching++;

    }

    mc_pointing_difference = z_MC - sv_vector_mean ;
  
  }


   ///////////////////// END OF POINTING VECTOR PART ////////////////////////////

  

  int best_PV = 0;
  int best_PV_counter = 0;
  float z_difference = 100. ;

  for (std::vector<reco::Vertex>::const_iterator it_pv = pv->begin(); it_pv != pv->end(); ++it_pv) {

    if( fabs(z_MC - it_pv->z())<z_difference ){

      z_difference = fabs(z_MC - it_pv->z()) ;
      best_PV = best_PV_counter ; 

    }

    best_PV_counter++ ;

  }

  if(tag_info_valid){
  
    cout<<" "<<endl;
    cout<<"best PV from pointing vector method: "<<best_PV_matching<<endl;
    cout<<"best PV from MC truth: "<<best_PV<<endl;
    cout<<"mc_pointing_difference: "<<mc_pointing_difference<<endl;
    cout<<" "<<endl;
  
  }


  for (std::vector<reco::Vertex>::const_iterator it_pv = pv->begin(); it_pv != pv->end(); ++it_pv) {

    //if(vtx_counter == best_PV){
    if(vtx_counter == 0){

      //z_SV.clear();
      Gen_pt.clear();
      Pat_pt.clear();
      Gen_energy.clear();
      Pat_energy.clear();
      Gen_eta.clear();
      Pat_eta.clear();
      Gen_phi.clear();
      Pat_phi.clear();
      //Pat_bTagger.clear();
      Pat_bScore.clear();
      PF_candTime.clear();
      PF_candTime_error.clear();

      Pruned_pt.clear();
      Pruned_eta.clear();
      Pruned_phi.clear();
      Pruned_partonFlav.clear();
      Pruned_mother_partonFlav.clear();
 
      eventNumber = iEvent.id().event();

      //ntracks = pv2->at(0).nTracks();

      z_4d = it_pv->z();
      vtx_time = it_pv->t();
      vtx_time_error = it_pv->tError();


      if( vtx_time_error > 0 ){


        for(std::vector<reco::GenParticle>::const_iterator genParticle = genParticles->begin(); genParticle != genParticles->end(); ++genParticle){
        //for(reco::GenParticleCollection::const_iterator genParticle = genParticles->begin(); genParticle != genParticles->end(); ++genParticle){

          float pru_ptt = genParticle->pt();
          float pru_eta = genParticle->eta();
          float pru_phi = genParticle->phi();

          Pruned_pt.push_back(pru_ptt);
          Pruned_eta.push_back(pru_eta);
          Pruned_phi.push_back(pru_phi);

          int pru_parton_flav = genParticle->pdgId();
          //cout<<pru_parton_flav<<endl;
          Pruned_partonFlav.push_back(pru_parton_flav);


          //int pru_mother_parton_flav = 0;
          //genParticle->mother(0).pdgId();
          //reco::GenParticle*>(&(*part)) == nullptr
          //if( genParticle->numberOfMothers() != 0 ) pru_mother_parton_flav = genParticle->mother(0)->pdgId();
          //if( std::abs(pru_parton_flav) == 5 ) pru_mother_parton_flav = genParticle->mother()->pdgId();
          //else pru_mother_parton_flav = 50;

          //Pruned_mother_partonFlav.push_back(pru_mother_parton_flav);

        }


        int gen_jet_counter = 0;
        for (std::vector<reco::GenJet>::const_iterator it_genjet = genjets->begin(); it_genjet != genjets->end(); ++it_genjet){

          const reco::GenJet* gjet = &(*it_genjet);
          float gen_energy = gjet->energy();
          float gen_ptt = gjet->pt();
          float gen_eta = gjet->eta();
          float gen_phi = gjet->phi();

          Gen_energy.push_back(gen_energy);
          Gen_pt.push_back(gen_ptt);
          Gen_eta.push_back(gen_eta);
          Gen_phi.push_back(gen_phi);

          gen_jet_counter++ ;

        }

        ngen_jet = genjets->size();
        


        int pat_jet_counter = 0;
        for(pat::JetCollection::const_iterator it_patjet = patjets->begin(); it_patjet != patjets->end(); ++it_patjet){

          
          const pat::Jet* pjet  = &(*it_patjet);
          //double dr = deltaR(gjet, pjet);
          float pat_energy = pjet->energy();
          float pat_ptt = pjet->pt();
          float pat_eta = pjet->eta();
          float pat_phi = pjet->phi();

          float bTagger = pjet->bDiscriminator(bTaggerName) + pjet->bDiscriminator((bTaggerName + "b"));
          //bool isBtagged = bTagger > bTaggerThreshold;

          //if(pat_ptt>20 && pat_jet_counter<15){

            Pat_energy.push_back(pat_energy);
            Pat_pt.push_back(pat_ptt);
            Pat_eta.push_back(pat_eta);
            Pat_phi.push_back(pat_phi);
            Pat_bScore.push_back(bTagger);

            std::vector<float> candidates_time;
            std::vector<float> candidates_time_error;
            //std::vector<float> candidates_pt;
            //std::vector<float> candidates_eta;
            //std::vector<float> candidates_phi;
          

            for (unsigned int id = 0, nd = pjet->numberOfDaughters(); id < nd; ++id) {

              const pat::PackedCandidate &packedC = dynamic_cast<const pat::PackedCandidate &>(*pjet->daughter(id));

              float time = packedC.time();
              float time_error = packedC.timeError();

              if(time_error>0 && time_error<0.025){

                //float packed_pt = packedC.pt();
                //float packed_eta = packedC.eta();
                //float packed_phi = packedC.phi();

                candidates_time.push_back(time);
                candidates_time_error.push_back(time_error);
                //Timediff.push_back(timediff);
                //Sigmat.push_back(sigma_t);
                //candidates_pt.push_back(packed_pt);
                //candidates_eta.push_back(packed_eta);
                //candidates_phi.push_back(packed_phi);
                
              }
            }

            PF_candTime.push_back(candidates_time);
            PF_candTime_error.push_back(candidates_time_error);
            //PF_candPt.push_back(candidates_pt);
            //PF_candEta.push_back(candidates_eta);
            //PF_candPhi.push_back(candidates_phi);

            pat_jet_counter++;

          //}
        }

          npat_jet = patjets->size();

      }

        OutTree->Fill();

    }

      vtx_counter++ ;

  }
}
                  



//double MyJetAnalysis::deltaR(const reco::Jet* j1, const reco::Jet* j2) {
double MyJetAnalysis::deltaR(const pat::Jet* j1, const reco::Jet* j2) {

  double deta = j1->eta() - j2->eta();
  double dphi = std::fabs(j1->phi() - j2->phi());
  if (dphi > 3.1415927)
    dphi = 2 * 3.1415927 - dphi;
  return std::sqrt(deta * deta + dphi * dphi);
}

// ------------ method called once each job just before starting event loop  ------------
void MyJetAnalysis::beginJob() {

  rootfile->cd();

  //OutTree->Branch("runNumber", &runNumber, "runNumber/I");
  //OutTree->Branch("ntracks", &ntracks, "ntracks/I");
  //OutTree->Branch("z_SV", "std::vector<float>", &z_SV);
  OutTree->Branch("eventNumber", &eventNumber, "eventNumber/I");
  OutTree->Branch("z_MC", &z_MC, "z_MC/F");
  OutTree->Branch("z_4d", &z_4d, "z_4d/F");
  OutTree->Branch("PV_number", &PV_number, "PV_number/I");
  OutTree->Branch("ngen_jet", &ngen_jet, "ngen_jet/I");
  OutTree->Branch("npat_jet", &npat_jet, "npat_jet/I");

  OutTree->Branch("vtx_time", &vtx_time, "vtx_time/F");
  OutTree->Branch("vtx_time_error", &vtx_time_error, "vtx_time_error/F");
  
  OutTree->Branch("Gen_energy", "std::vector<float>", &Gen_energy);
  OutTree->Branch("Gen_pt", "std::vector<float>", &Gen_pt);
  OutTree->Branch("Pat_energy", "std::vector<float>", &Pat_energy);
  OutTree->Branch("Pat_pt", "std::vector<float>", &Pat_pt);
  OutTree->Branch("Gen_eta", "std::vector<float>", &Gen_eta);
  OutTree->Branch("Pat_eta", "std::vector<float>", &Pat_eta);
  OutTree->Branch("Gen_phi", "std::vector<float>", &Gen_phi);
  OutTree->Branch("Pat_phi", "std::vector<float>", &Pat_phi);

  //OutTree->Branch("Pat_bTagger", "std::vector<bool>", &Pat_bTagger);

  OutTree->Branch("PF_candTime", "std::vector<std::vector<float>>",  &PF_candTime);
  OutTree->Branch("PF_candTime_error", "std::vector<std::vector<float>>", &PF_candTime_error);
  OutTree->Branch("Pat_bScore", "std::vector<float>", &Pat_bScore);
  //OutTree->Branch("PF_candPt", "std::vector<std::vector<float>>", &PF_candPt);
  //OutTree->Branch("PF_candEta", "std::vector<std::vector<float>>", &PF_candEta);
  //OutTree->Branch("PF_candPhi", "std::vector<std::vector<float>>", &PF_candPhi);

  OutTree->Branch("Pruned_partonFlav", "std::vector<int>", &Pruned_partonFlav);
  //OutTree->Branch("Pruned_mother_partonFlav", "std::vector<int>", &Pruned_mother_partonFlav);
  OutTree->Branch("Pruned_pt", "std::vector<float>", &Pruned_pt);
  OutTree->Branch("Pruned_eta", "std::vector<float>", &Pruned_eta);
  OutTree->Branch("Pruned_phi", "std::vector<float>", &Pruned_phi);
  
  return;

}

void MyJetAnalysis::endJob() {

  OutTree->Write();
  rootfile->Write();
  rootfile->Close(); 

}

DEFINE_FWK_MODULE(MyJetAnalysis);






          