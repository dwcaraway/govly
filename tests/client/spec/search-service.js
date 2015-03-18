/**
 * Created by DavidWCaraway on 3/17/15.
 * Tests the search service
 */
describe('Provider: search-service', function () {
    'use strict';

    var searchService;

    beforeEach(module('searchService', 'angular-login.grandfather', 'angular-login.home'));

    // Initialize the controller and a mock scope
    beforeEach(inject(function (_searchService_) {
        searchService = _searchService_;
    }));

    describe('getOpps', function () {
        it('should get initial document set if start is not set', inject(function ($httpBackend) {
            var response = {
                docs: [{}],
                numFound: 1
            };

            $httpBackend.expectGET(/.*\/api\/opps.*/).respond(response, 200);

            searchService.getOpps();

            $httpBackend.flush();

            expect(searchService.hits).toBe(response.numFound);
            expect(searchService.opps).toEqual(response.docs);

        }));

    });
});