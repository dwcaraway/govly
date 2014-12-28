'use strict';

describe('CommonService test', function () {

  // load the application module
  beforeEach(module('CommonService'), function($provide) {
    // Output messages
    $provide.value('$log', console);
  });

  describe('link relation', function(){
      var linkRelation, httpBackend;

      // Initialize the service
      //TODO should we REALLY inject these two dependencies for each test or only once at start?
      beforeEach(inject(function (LinkRelation, $httpBackend) {
          linkRelation = LinkRelation;
          httpBackend = $httpBackend;
      }));

      afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
      });

      it('should retrieve the latest link relations on load', function () {
          var schemas = {'TO':'DO'};
          httpBackend.expectGET('https://api.fogmine.com/rels').respond(schemas);
          httpBackend.flush();

          expect(linkRelation.getSchemas()).toEqual(schemas);
      });

      it('should retrieve the latest link relations on load', function () {
          var schemas = {'TO':'DO'};
          httpBackend.expectGET('https://api.fogmine.com/rels').respond(schemas);
          httpBackend.flush();

          expect(linkRelation.getSchemas()).toEqual(schemas);
      });
  });
});