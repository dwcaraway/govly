'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:LogoutCtrl
 * @description
 * Controller of vitalsApp controlling logout
 */
angular.module('vitalsApp')
    .controller('LogoutCtrl', ['Security', '$scope','$state', function (Security, $scope) {
        Security.logout();

        $scope.alerts = [
                {type: 'success', msg: 'You have been logged out.'}
            ];

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };

    }]);
