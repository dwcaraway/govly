angular.module('searchService', ['ngResource', 'ui.router', 'config'])
    .provider('searchService', function () {
        'use strict';

        this.$get = function (ENV, $q, $log, $injector) {

            //TODO replace injector with direct injection of $resource
            var $resource = $injector.get('$resource');
            var Opps = $resource(ENV.apiEndpoint+'/opps');
            var page = 1; //current page of results; 1-based
            var page_size = 20; //number of results to grab

            /**
             * Low-level, private functions.
             */
            var resetFilterStart = function(){
                /**
                 * Resets the filter's starting point
                 */
                wrappedService.filter.start = 0;
                page = 0;
                wrappedService.hasNextPage = true;
            };

            var incrementFilterStart = function(){
                    /**
                     * Updates the filter to grab the next increment of search results
                     */
                    $log.debug('updating the filter to grab the next page');

                    page++;

                    wrappedService.filter.start = page_size * (page - 1);

                    $log.debug('start: ' + wrappedService.filter.start);
            };

            /**
             * High level, public methods
             */
            var wrappedService = {

                getOpps: function (append) {
                    /**
                     * Retrieves the opportunities collection from the remote api and
                     * stores them to the wrappedService.opps public variable.
                     *
                     * append: boolean, truthy if we should add results to previous
                     * results, otherwise will overwrite the previous search's results
                     *
                     * returns: a promise that resolves if the opps may be retrieved from remote, rejects otherwise.
                     */

                    var checkOpps = $q.defer();

                    if(append && !wrappedService.hasNextPage){
                            console.debug('no further search results available. Aborting');
                            return;
                    }

                    if (append) {
                        incrementFilterStart();
                    }else{
                        resetFilterStart();
                    }

                    wrappedService.isLoading = true;

                    Opps.get(wrappedService.filter, function (data) {

                        if (append) {
                            console.debug('scrolling!');
                            //This is for infinite scrolling, we add docs to docs from previous request
                            wrappedService.opps = wrappedService.opps.concat(data.docs);
                        } else {
                            console.debug('resetting the search results');
                            wrappedService.opps = data.docs;
                        }

                        wrappedService.hits = data.numFound || 0;

                        if(data.docs.length < page_size){
                            console.debug('results less than page size, so no further results available');
                            wrappedService.hasNextPage = false;
                        }

                        checkOpps.resolve(data);

                    }, function (data, status) {
                        $log.warn('Request failed:' + status);

                        wrappedService.opps = [];
                        wrappedService.hits = 0;

                        checkOpps.reject(data, status);
                    });

                    //Set a finally block to turn off loading
                    checkOpps.promise.finally(function(){
                       wrappedService.isLoading = false;
                    });

                    return checkOpps.promise;
                },

                /**
                 * Public properties
                 */
                isLoading: false, //truthy if data is loading, false otherwise
                hasNextPage: true, //truthy if there's another page worth (<= page_size) of data available
                hits: 0, //total search results (positive matches). we only look at a subset of the total
                opps: [], //array of opportunity objects. this is a subset of the totalHits number of results. view renders these.
                filter: {limit: page_size, start: page-1} //key-value pairs that become part of the query string for searches
            };

            return wrappedService;
        };
    });
