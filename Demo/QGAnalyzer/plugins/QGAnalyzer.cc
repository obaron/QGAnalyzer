// -*- C++ -*-
//
// Package:    Demo/QGAnalyzer
// Class:      QGAnalyzer
// 
/**\class QGAnalyzer QGAnalyzer.cc Demo/QGAnalyzer/plugins/QGAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Owen Baron
//         Created:  Fri, 25 Mar 2016 17:54:55 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
//Histogram Headers
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TH2.h"

//Jet Headers 
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/Common/interface/ValueMap.h"
//
// class declaration
//

class QGAnalyzer : public edm::EDAnalyzer {
   public:
      explicit QGAnalyzer(const edm::ParameterSet&);
      ~QGAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
	  
	edm::EDGetTokenT<reco::PFJetCollection> jetsToken;
	edm::EDGetTokenT<edm::ValueMap<float>> qgToken;
	edm::InputTag jetsInputTag;
	TH1D *qgplot;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//
//edm::InputTag jetsInputTag;
//
// constructors and destructor
//
QGAnalyzer::QGAnalyzer(const edm::ParameterSet& iConfig) :
jetsToken(consumes<reco::PFJetCollection>( iConfig.getParameter<edm::InputTag>("jetsInputTag")))
{
  qgToken = consumes<edm::ValueMap<float>>(edm::InputTag("QGTagger", "qgLikelihood"));
  edm::Service<TFileService> fs;
  qgplot = fs->make<TH1D>("qgplot","QG Likelihood",50,0,50);
  
}


QGAnalyzer::~QGAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
QGAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
  edm::Handle<reco::PFJetCollection> jets;    iEvent.getByToken(jetsToken, jets);
  edm::Handle<edm::ValueMap<float>> qgHandle; iEvent.getByToken(qgToken, qgHandle);

  for(auto jet = jets->begin();  jet != jets->end(); ++jet){
     edm::RefToBase<reco::Jet> jetRef(edm::Ref<reco::PFJetCollection>(jets, jet - jets->begin()));
     float qgLikelihood = (*qgHandle)[jetRef];
	 qgplot->Fill(qgLikelihood);
	 
  }

#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
}


// ------------ method called once each job just before starting event loop  ------------
void 
QGAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
QGAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
QGAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
QGAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
QGAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
QGAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
QGAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(QGAnalyzer);
