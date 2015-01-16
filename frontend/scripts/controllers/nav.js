'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:NavCtrl
 * @description
 * # RegisterCtrl
 * Controller of the vitalsApp
 */
angular.module('vitalsApp')
    .controller('NavCtrl', ['Security', '$scope', '$state', function (Security, $scope, $state) {
        $scope.user = {};
        $scope.authBtnLink = $state.href('login');
        $scope.authBtnText = 'Logout';

        $scope.$watch(Security.isAuthenticated, function (userIsAuthenticated) {
            $scope.isAuthenticated = userIsAuthenticated;

            if (userIsAuthenticated) {
                $scope.authBtnLink = $state.href('logout');
                $scope.authBtnText = 'Logout';
            }
            else {
                $scope.authBtnLink = $state.href('login');
                $scope.authBtnText = 'Login';
            }
        });

    }]);