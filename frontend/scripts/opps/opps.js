angular.module('angular-login.opps', ['angular-login.grandfather', 'config', 'infinite-scroll', 'searchService', 'truncate'])
    .config(function ($stateProvider) {
        'use strict';
        $stateProvider
            .state('app.opps', {
                url: '/opps',
                templateUrl: 'opps/opps.tpl.html',
                accessLevel: accessLevels.user
            });
    })
    .controller('OppsCtrl', function ($scope, $log, $timeout, searchService) {
        'use strict';

        var currentPage = 1;

        $scope.ss = searchService;

        $scope.infiniteScroll = function () {
            $log.debug('infinite scroll called');

            if (searchService.isLoading){
                $log.debug('ignoring the call, already loading');
                return;
            }

            searchService.isLoading = true;//in the chance that infinite scroll will trigger before the load starts,
            // we're blocking further calls until a value returns

            $scope.$apply(searchService.nextPage);

                //.then(
                //function refreshView() {
                //    $log.debug('opps executed, trying to update the view!');
                //    $scope.$apply();
                //});

            currentPage = currentPage + 1;
        };

        $scope.$watch(
            function () {
                return searchService.opps;
            },
            function () {
                $log.debug('$watch triggered an update to the view! size of docs: '+searchService.opps.length);
            });

        //On page load, get opportunities with no filtering.
        searchService.getOpps();

    });
