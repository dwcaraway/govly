'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:RegisterCtrl
 * @description
 * # RegisterCtrl
 * Controller of the vitalsApp
 */
angular.module('vitalsApp')
    .controller('ConfirmationCtrl', ['Security', '$scope', '$stateParams', '$location', '$log', '$state', function (Security, $scope, $stateParams, $location, $log, $state) {
        var token = $stateParams.token;

        if (token) {
            $log.debug('Contacting server')

            Security.confirm($stateParams.token).
                success(
                function (data) {
                    $log.info('Confirmation successful');
                    $scope.alerts = [
                        {type: 'success', msg: 'Account Confirmed!'}
                    ];
                    localStorage.setItem('fogmine-token', data.token);
                    $state.go('main');
                }).error(
                function (data, status) {
                    $log.warn('Confirmation failed');

                    if (status === 0) {
                        $scope.alerts = [
                            {type: 'danger', msg: "Unable to connect"}
                        ];
                    } else {
                        $scope.alerts = [
                            {type: 'danger', msg: data.message}
                        ];
                    }
                });
        } else {
            $scope.alerts = [
                {type: 'danger', msg: 'Bad confirmation URL'}
            ];
        }

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };
    }]);