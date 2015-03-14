angular.module('angular-login.opps', ['angular-login.grandfather', 'ngResource', 'config', 'infinite-scroll'])
    .config(function ($stateProvider) {
        'use strict';
        $stateProvider
            .state('app.opps', {
                url: '/opps',
                templateUrl: 'opps/opps.tpl.html',
                accessLevel: accessLevels.user
            });
    })
    .controller('MainCtrl', function ($scope, $http, $resource, $timeout, $log, ENV) {
        'use strict';


        var Opp = $resource(ENV.apiEndpoint+'/opps');
        $scope.currentPage = 1;

        $scope.getOpps = function (filter) {
            $scope.filter = filter || {};
            Opp.get($scope.filter, function (data) {
                if ($scope.currentPage === 1) {
                    $log.debug('reseting data page to 1');
                    $scope.opps = data;
                }else{
                    $log.debug('adding new page of data to result set');
                    $scope.opps.docs = $scope.opps.docs.concat(data.docs);
                }

                $timeout(function () {
                    $scope.$broadcast('dataloaded');
                }, 0, false);
            }, function (data, status) {
                console.log('Request failed:' + status);
            });
        };

        $scope.infiniteScroll = function () {
            if (!$scope.opps) {
                return;
            }
            var size = $scope.filter.limit || 20;

            $scope.currentPage = $scope.currentPage + 1;
            $log.debug('page: ' + $scope.currentPage);
            $scope.filter = $scope.filter || {};
            $scope.filter.start = size * ($scope.currentPage - 1);
            $log.debug('start: ' + $scope.filter.start);
            $scope.getOpps($scope.filter);
        };

        $scope.filterChanged = function () {
            $log.debug('page: ' + $scope.currentPage);
            $scope.currentPage = 1;
            $scope.filter = $scope.filter || {};
            $scope.filter.start = 0;
            $scope.getOpps($scope.filter);
        };


        //On page load, get opportunities with no filtering.
        $scope.getOpps();

    });

//// apply jquery shorten to all div children with class shorten
//    .directive('shorten', ['$timeout', function ($timeout) {
//        return {
//            link: function ($scope, element, attrs) {
//                $scope.$on('dataloaded', function () {
//                    $timeout(function () { // You might need this timeout to be sure its run after DOM render
//                        $('div.shorten').shorten({
//                            'showChars': 255});
//                    }, 0, false);
//                });
//            }
//        };
//    }]);
