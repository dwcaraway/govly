'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:RegisterCtrl
 * @description
 * # RegisterCtrl
 * Controller of the vitalsApp
 */
angular.module('vitalsApp')
    .controller('LoginCtrl', ['Security', '$scope', '$state', function (Security, $scope, $state) {
        $scope.user = {};
        $scope.alerts = [];

        $scope.login = function () {
            Security.login($scope.user.email, $scope.user.password).then(
                function () {
                    $state.go('main');
                }, function (status) {
                    if (status === 0) {
                        $scope.alerts = [
                            {type: 'danger', msg: 'No connection!'}
                        ];
                    } else {
                        $scope.alerts = [
                            {type: 'danger', msg: 'Invalid email and/or password'}
                        ];
                    }
                });
        };

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };

        return {'login': $scope.login};
    }]);
