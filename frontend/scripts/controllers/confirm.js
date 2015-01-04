'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:RegisterCtrl
 * @description
 * # RegisterCtrl
 * Controller of the vitalsApp
 */
angular.module('vitalsApp')
    .controller('ConfirmationCtrl', ['Security', '$scope', '$stateParams', '$location', '$log', '$http', function (Security, $scope, $stateParams, $location, $log, $http) {

        $log.info('Verifying token with server');

        var token = $stateParams.token;

        if (token) {
            $scope.alertss = [{type: 'warning', msg: 'Contacting server...'}]
            ;
            $log.debug('token=' + $stateParams.token);

            $http.get('http://localhost:5000/auth/confirm?token=' + $stateParams.token).
                success(

//        Security.confirm($stateParams.token,
                function (data) {
                    $log.info('Confirmation successful');
                    $scope.alerts = [{type: 'success', msg: 'Account Confirmed!'}];
                    localStorage.setItem('fogmine-token', data.token);
//                scope.$apply(function() { $location.path("/"); });
                }).error(
//            ,
                function (data, status) {
                    $log.warn('Confirmation failed');

                    if (status === 0) {
                        $scope.alerts = [{type: 'danger', msg: "Unable to connect"}];
                    } else {
                        $scope.alerts = [{type: 'danger', msg: data.message}];
                    }
                });
        } else {
            $scope.alerts = [{type: 'danger', msg: 'No token defined!'}];
        }

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };
    }]);