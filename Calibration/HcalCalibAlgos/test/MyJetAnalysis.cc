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
  
  //PuppiCollName_ = iConfig.getParameter<std::string>("PuppiCollName");
  //PuppiCollName_ = iConfig.getParameter<edm::InputTag>("PuppiCollName");
  //PuppiCollName_ = iConfig.getParameter<edm::InputTag>("patJetsAk4PuppiJets");

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

  Sv_ = iConfig.getParameter<std::string>("svTagInfos");
  
  
  //tok_Puppi_ = consumes<std::vector<pat::Jet>>(PuppiCollName_);

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

  svSrc_ = consumes<std::vector<reco::VertexCompositePtrCandidate>>(Sv_); //--> devo passare da questo a CandSecondaryVertexTagInfo
  

  }


MyJetAnalysis::~MyJetAnalysis() {}

//
// member functions
//

// ------------ method called to for each event  ------------
void MyJetAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& evSetup) {

  //int eventNumber = iEvent.id().event();
  //printf("event: %i \n",eventNumber);

  //edm::Handle<std::vector<pat::Jet>> puppijets;
  //iEvent.getByToken(tok_Puppi_, puppijets);

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

  edm::Handle<std::vector<reco::VertexCompositePtrCandidate>> svTagInfos;
  iEvent.getByToken(svSrc_, svTagInfos);
  

  int vtx_counter = 0;

  //float bTaggerThreshold = 0.6321;
  //float bTaggerThreshold = 0.4184;
  std::string bTaggerName = "pfDeepCSVJetTags:probb";

  std::vector<int> pv_pos ;
  std::vector<float> pv_dist ;

  std::vector<float> xx_vec ;
  std::vector<float> yy_vec ;
  std::vector<float> zz_vec ;

  std::vector<float> px_vec ;
  std::vector<float> py_vec ;
  std::vector<float> pz_vec ;

  std::vector<float> t_vec ;
  

  for(pat::JetCollection::const_iterator it_patjet = patjets->begin(); it_patjet != patjets->end(); ++it_patjet){

    const pat::Jet* pjet  = &(*it_patjet);
    float ptt = pjet->pt();
    float px = pjet->px();
    float py = pjet->py();
    float pz = pjet->pz();
    float pat_eta = pjet->eta();
    float pat_phi = pjet->phi();

    float dr_start = 100000. ;
    float bTagger = pjet->bDiscriminator(bTaggerName) + pjet->bDiscriminator((bTaggerName + "b"));
    
    if( bTagger>0.4184 ){  // && fabs(pat_eta)<2. && ptt>40 

    float x1, y1, z1 ;

    bool sv_found = false ;

    for ( std::vector<reco::VertexCompositePtrCandidate>::const_iterator iterTI = svTagInfos->begin(); iterTI != svTagInfos->end(); ++iterTI) {
          
      const reco::VertexCompositePtrCandidate&  sv = *(iterTI);
      float xx = sv.position().x() ;
      float yy = sv.position().y() ;
      float zz = sv.position().z() ;
      float sv_eta = sv.eta();
      float sv_phi = sv.phi();

      
      float deta = pat_eta - sv_eta;
      float dphi = pat_phi - sv_phi;
      if (dphi > 3.1415927) dphi = 2 * 3.1415927 - dphi;
      float dr = std::sqrt(deta * deta + dphi * dphi);

      if( dr<0.4 && dr < dr_start ){
  
       sv_found = true ;
       dr_start = dr ;
       x1 = xx ;
       y1 = yy ;
       z1 = zz ;

      }
    }
    
      if(sv_found && xx_vec.size()<4 ){ //
      
      xx_vec.push_back(x1) ;
      yy_vec.push_back(y1) ;
      zz_vec.push_back(z1) ;

      px_vec.push_back(px) ;
      py_vec.push_back(py) ;
      pz_vec.push_back(pz) ;

      }

    }

  }


  float x_MC = genParticlesPosition->x();
  float y_MC = genParticlesPosition->y();
  z_MC = genParticlesPosition->z();

  int PV_number = 0;
  int PV_number_reco = 1000;
  int best_PV_counter = 0;

  float z_difference = 1000. ;
  float z_difference_reco = 1000. ;

  for (std::vector<reco::Vertex>::const_iterator it_pv = pv->begin(); it_pv != pv->end(); ++it_pv) {

    float dist_sim = std::sqrt( std::pow( (x_MC-it_pv->x()), 2 ) + std::pow( (y_MC-it_pv->y()), 2 ) + std::pow( (z_MC-it_pv->z()), 2 ) ) ;

    if( dist_sim < z_difference ){

      z_difference = dist_sim ;
      PV_number = best_PV_counter ; 

    }

    float X = 0. ;
    float Y = 0. ;
    float Z = 0. ;
    //float pz_total = 0. ;

    if( xx_vec.size()>0 ){
    for(uint l=0; l<xx_vec.size(); l++){

      float p_square = px_vec.at(l)*px_vec.at(l) + py_vec.at(l)*py_vec.at(l) + pz_vec.at(l)*pz_vec.at(l) ; 
      float p_trans = std::sqrt( px_vec.at(l)*px_vec.at(l) + py_vec.at(l)*py_vec.at(l) + pz_vec.at(l)*pz_vec.at(l) );
      float t = ( px_vec.at(l)*( xx_vec.at(l)-it_pv->x() ) + py_vec.at(l)*( yy_vec.at(l)-it_pv->y() ) + pz_vec.at(l)*( zz_vec.at(l)-it_pv->z() ) )/p_square ;

      X += xx_vec.at(l) - px_vec.at(l)*t ;
      Y += yy_vec.at(l) - py_vec.at(l)*t ;
      Z += zz_vec.at(l) - pz_vec.at(l)*t ;

      //Z += p_trans*(zz_vec.at(l) - pz_vec.at(l)*t) ;
      //pz_total += p_trans ;
    }

    //Z = Z/( pz_total ) ;
    X = X/( zz_vec.size() ) ;
    Y = Y/( zz_vec.size() ) ;
    Z = Z/( zz_vec.size() ) ;

    //float dist = fabs( Z-it_pv->z() ) ;
    float dist = std::sqrt( std::pow( (X-it_pv->x()), 2 ) + std::pow( (Y-it_pv->y()), 2 ) + std::pow( (Z-it_pv->z()), 2 ) ) ;
    
    if( dist < z_difference_reco ){  //  && fabs( dist-z_difference_reco )>0.01   && best_PV_counter<=10       

      z_difference_reco = dist ;
      PV_number_reco = best_PV_counter ; 

    }

    }


    best_PV_counter++ ;

  }


  if( PV_number_reco==1000 ){

   not_valid_counter++ ;
   PV_number_reco = 0 ;

  }

  total_event_counter++ ;
  if( PV_number==PV_number_reco ){

   matched_vtx_event_counter++ ;
   dist_matched = z_difference_reco ;

  }

  if( PV_number!=PV_number_reco ){

   dist_unmatched = z_difference_reco ;

  }


  if(PV_number!=0){

    no_zero_event_counter ++ ;
    if( PV_number==PV_number_reco ) matched_no_zero_event_counter ++ ;


  }


  cout<<"ratio: "<< float(matched_vtx_event_counter)/float(total_event_counter)<<endl;
  //cout<<"inefficiency: "<< float(not_valid_counter)/float(total_event_counter)<<endl;
  //cout<<"non-zero PV matched: "<< float(matched_no_zero_event_counter)/float(no_zero_event_counter)<<endl;
  cout<<"\n\n"<<endl;


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


  if( PV_number == 0 ){
  for (std::vector<reco::Vertex>::const_iterator it_pv = pv->begin(); it_pv != pv->end(); ++it_pv) {

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
      PF_multiplicity.clear();
      PF_puppiWeight.clear();
      PF_candTime.clear();
      PF_candTime_error.clear();
      PF_candPt.clear();
      PF_candCharge.clear();

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
        //for(pat::JetCollection::const_iterator it_patjet = puppijets->begin(); it_patjet != puppijets->end(); ++it_patjet){

          
          const pat::Jet* pjet  = &(*it_patjet);
          float pat_energy = pjet->energy();
          float pat_ptt = pjet->pt();
          float pat_eta = pjet->eta();
          float pat_phi = pjet->phi();

          float bTagger = pjet->bDiscriminator(bTaggerName) + pjet->bDiscriminator((bTaggerName + "b"));

          //if(pat_ptt>20 && pat_jet_counter<15){

            Pat_energy.push_back(pat_energy);
            Pat_pt.push_back(pat_ptt);
            Pat_eta.push_back(pat_eta);
            Pat_phi.push_back(pat_phi);
            Pat_bScore.push_back(bTagger);

            std::vector<float> puppiW;
            std::vector<float> candidates_time;
            std::vector<float> candidates_time_error;
            std::vector<float> candidates_pt;
            std::vector<float> candidates_ch;
            //std::vector<float> candidates_eta;
            //std::vector<float> candidates_phi;

            //PF_multiplicity.push_back( pjet->numberOfDaughters() );
          

            for (unsigned int id = 0, nd = pjet->numberOfDaughters(); id < nd; ++id) {

              const pat::PackedCandidate &packedC = dynamic_cast<const pat::PackedCandidate &>(*pjet->daughter(id));

              float time = packedC.time();
              float time_error = packedC.timeError();

              if( time_error>0 ){
              //if(time_error<0.025){

                float packed_pt = packedC.pt();
                float packed_ch = packedC.charge();
                //float packed_eta = packedC.eta();
                //float packed_phi = packedC.phi();

                puppiW.push_back( packedC.puppiWeight() );
                candidates_time.push_back(time);
                candidates_time_error.push_back(time_error);
                //Timediff.push_back(timediff);
                //Sigmat.push_back(sigma_t);
                candidates_pt.push_back(packed_pt);
                candidates_ch.push_back(packed_ch);
                //candidates_eta.push_back(packed_eta);
                //candidates_phi.push_back(packed_phi);
                
              }
            }

            PF_puppiWeight.push_back( puppiW );
            PF_candTime.push_back( candidates_time );
            PF_candTime_error.push_back( candidates_time_error );
            PF_candPt.push_back(candidates_pt);
            PF_candCharge.push_back(candidates_ch);
            //PF_candEta.push_back(candidates_eta);
            //PF_candPhi.push_back(candidates_phi);

            pat_jet_counter++;

          //}
        }

          npat_jet = patjets->size();

      }

        //OutTree->Fill();

    }

      vtx_counter++ ;

  }
  }
  OutTree->Fill();
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
  OutTree->Branch("z_pv_vector", "std::vector<float>", &z_pv_vector);
  OutTree->Branch("PV_number", &PV_number, "PV_number/I");
  OutTree->Branch("ngen_jet", &ngen_jet, "ngen_jet/I");
  OutTree->Branch("npat_jet", &npat_jet, "npat_jet/I");

  OutTree->Branch("vtx_time", &vtx_time, "vtx_time/F");
  OutTree->Branch("vtx_time_error", &vtx_time_error, "vtx_time_error/F");

  OutTree->Branch("dist_matched", &dist_matched, "dist_matched/F");
  OutTree->Branch("dist_unmatched", &dist_unmatched, "dist_unmatched/F");
  
  OutTree->Branch("Gen_energy", "std::vector<float>", &Gen_energy);
  OutTree->Branch("Gen_pt", "std::vector<float>", &Gen_pt);
  OutTree->Branch("Pat_energy", "std::vector<float>", &Pat_energy);
  OutTree->Branch("Pat_pt", "std::vector<float>", &Pat_pt);
  OutTree->Branch("Gen_eta", "std::vector<float>", &Gen_eta);
  OutTree->Branch("Pat_eta", "std::vector<float>", &Pat_eta);
  OutTree->Branch("Gen_phi", "std::vector<float>", &Gen_phi);
  OutTree->Branch("Pat_phi", "std::vector<float>", &Pat_phi);
  OutTree->Branch("Pat_bScore", "std::vector<float>", &Pat_bScore);
  //OutTree->Branch("Pat_bTagger", "std::vector<bool>", &Pat_bTagger);

  //OutTree->Branch("PF_multiplicity", "std::vector<int>",  &PF_multiplicity);
  OutTree->Branch("PF_puppiWeight", "std::vector<std::vector<float>>",  &PF_puppiWeight);
  OutTree->Branch("PF_candTime", "std::vector<std::vector<float>>",  &PF_candTime);
  OutTree->Branch("PF_candTime_error", "std::vector<std::vector<float>>", &PF_candTime_error);
  OutTree->Branch("PF_candPt", "std::vector<std::vector<float>>", &PF_candPt);
  OutTree->Branch("PF_candCharge", "std::vector<std::vector<float>>", &PF_candCharge);
  //OutTree->Branch("PF_candEta", "std::vector<std::vector<float>>", &PF_candEta);
  //OutTree->Branch("PF_candPhi", "std::vector<std::vector<float>>", &PF_candPhi);

  //OutTree->Branch("Pruned_partonFlav", "std::vector<int>", &Pruned_partonFlav);
  OutTree->Branch("Pruned_mother_partonFlav", "std::vector<int>", &Pruned_mother_partonFlav);
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






          
