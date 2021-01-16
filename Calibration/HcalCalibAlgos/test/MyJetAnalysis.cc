//
#include "MyJetAnalysis.h"
#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "FWCore/Utilities/interface/EDMException.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "TTree.h"
#include "TFile.h"
#include "TH1.h"
#include "TMath.h"
#include "TClonesArray.h"
#include "TObjString.h"
#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <boost/regex.hpp>

/*inline void HERE(const char* msg) {
  if (0 && msg)
    edm::LogWarning("MyJetAnalysis") << msg;
}*/


MyJetAnalysis::MyJetAnalysis(const edm::ParameterSet& iConfig){
  // set parameters
  
  pfJetCollName_ = iConfig.getParameter<std::string>("pfJetCollName");
  //pfJetCorrName_ = iConfig.getParameter<std::string>("pfJetCorrName");
  //genJetCollName_ = iConfig.getParameter<std::string>("genJetCollName");
  pvCollName_ = iConfig.getParameter<std::string>("pvCollName");
  //prodProcess_ = "MYGAMMA";
  //if (iConfig.exists("prodProcess"))
    //prodProcess_ = iConfig.getUntrackedParameter<std::string>("prodProcess");

  //doPFJets_ = iConfig.getParameter<bool>("doPFJets");
  //doGenJets_ = iConfig.getParameter<bool>("doGenJets");
  
  //eventWeight_ = 1.0;
  //eventPtHat_ = 0.;
  //nProcessed_ = 0;

  //Get the tokens
  // FAST FIX
  //if (workOnAOD_ < 2) {  // origin data file
  tok_PFJet_ = consumes<reco::PFJetCollection>(pfJetCollName_);
    //tok_GenJet_ = consumes<std::vector<reco::GenJet>>(genJetCollName_);
  tok_PV_ = consumes<std::vector<reco::Vertex>>(pvCollName_);

  //} else {
    // FAST FIX
    //const char* prod = "GammaJetProd";
    //if (prodProcess_.size() == 0) {
      //edm::LogError("MyJetAnalysis") << "prodProcess needs to be defined";
      //throw edm::Exception(edm::errors::ProductNotFound);
    //}
    //const char* an = prodProcess_.c_str();
    //edm::LogWarning("MyJetAnalysis") << "FAST FIX: changing " << photonCollName_ << " to"
    //                                    << edm::InputTag(prod, photonCollName_, an);
    //tok_PFJet_ = consumes<reco::PFJetCollection>(edm::InputTag(prod, pfJetCollName_, an));
    //tok_GenJet_ = consumes<std::vector<reco::GenJet>>(edm::InputTag(prod, genJetCollName_, an));
    //tok_PV_ = consumes<std::vector<reco::Vertex>>(edm::InputTag(prod, pvCollName_, an));
    //TString HLTlabel = "TriggerResults::HLT";
    //if (prodProcess_.find("reRECO") != std::string::npos)
      //HLTlabel.ReplaceAll("HLT", "reHLT");
    //tok_TrigRes_ = consumes<edm::TriggerResults>(edm::InputTag(prod, HLTlabel.Data(), an));
  }


MyJetAnalysis::~MyJetAnalysis() {}

//
// member functions
//

// ------------ method called to for each event  ------------
void MyJetAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& evSetup) {


  edm::Handle<reco::PFJetCollection> pfjets;
  //iEvent.getByLabel("ak4PFJets", pfjets);
  iEvent.getByToken(tok_PFJet_, pfjets);

  edm::Handle<std::vector<reco::Vertex>> pv;
  iEvent.getByToken(tok_PV_, pv);
  

  TFile *rootfile=new TFile("time_out.root","RECREATE");
  rootfile->cd();

  TH1F *vtxtime_hist = new TH1F("vtxtime_hist","vtxtime_hist",20,-1,1);
  TH1F *pfcand_time_hist = new TH1F("pfcand_time_hist","pfcand_time_hist",80,-1,7);
  TH1F *timediff_hist = new TH1F("timediff_hist","timediff_hist",200,0,200);
  TH1F *sigmat_hist = new TH1F("sigmat_hist","sigmat_hist",40,0,20);

  //int vtx_counter = 0;

  for (std::vector<reco::Vertex>::const_iterator it = pv->begin(); it != pv->end(); ++it) {

    float vtx_time = it->t();
    float vtx_time_error = it->tError();
    vtxtime_hist->Fill(vtx_time);

    if(vtx_time_error > 0){

      for(reco::PFJetCollection::const_iterator it = pfjets->begin(); it != pfjets->end(); ++it){

        const reco::PFJet* jet  = &(*it);
        float ptt = TMath::Sqrt( jet->px()*jet->px() + jet->py()*jet->py() );
        float eta = TMath::Abs( jet->eta() );
        std::vector<reco::PFCandidatePtr> probeconst = jet->getPFConstituents();

        if( ptt>20 && eta<5 ){

          for(std::vector<reco::PFCandidatePtr>::const_iterator itt = probeconst.begin(); itt != probeconst.end(); ++itt){
        
            float pfcand_time = (*itt)->time();
            float pfcand_time_error = (*itt)->timeError();

            float timediff = TMath::Abs(vtx_time - pfcand_time)/pfcand_time_error;
            float sigma_t = TMath::Abs(vtx_time - pfcand_time)/TMath::Sqrt(pfcand_time_error*pfcand_time_error +  vtx_time_error*vtx_time_error) ;

            if( pfcand_time_error>0 && ptt>20 && eta<5 ){

              timediff_hist->Fill(timediff);
              pfcand_time_hist->Fill(pfcand_time); 
              sigmat_hist->Fill(sigma_t);
              //printf("%f", timee);
            }     
          }
        }
      }
    }
  }

  
  /*for (std::vector<reco::Vertex>::const_iterator it = pv->begin(); it != pv->end(); ++it) {

    //if (!it->isFake() ){

      float vtx_time = it->t();
      float vtx_time_error = it->tError();
      if(vtx_time_error > 0) printf("%f", vtx_time);

    //}
      
  }*/

  vtxtime_hist->Write();
  pfcand_time_hist->Write();
  timediff_hist->Write();
  sigmat_hist->Write();
  rootfile->Write();
  rootfile->Close(); 

        
}

// ------------ method called once each job just before starting event loop  ------------
/*void MyJetAnalysis::beginJob() {

return;

}

void MyJetAnalysis::endJob() {
  
}



void MyJetAnalysis::beginRun(const edm::Run& iRun, const edm::EventSetup& setup) {
  
}*/

// ---------------------------------------------------------------------

//define this as a plug-in

DEFINE_FWK_MODULE(MyJetAnalysis);
