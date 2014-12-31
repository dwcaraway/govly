'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:RegisterCtrl
 * @description
 * # RegisterCtrl
 * Controller of the vitalsApp
 */
angular.module('vitalsApp')
    .controller('RegisterCtrl', ['LinkRelation', 'Security', '$scope', '$http','$log' ,function (LinkRelation, Security, $scope, $http, $log) {
        $scope.user = {};
        $scope.alerts = [];

        var alertOnError = function (data, status) {
            var msg;

            if (status === 0) {
                msg = 'No connection';
            } else if (status == 409) {
                msg = 'Email address already registered.';
            } else if (status == 500) {
                msg = 'Internal Server Error';
            } else {
                msg = 'Registration failed!';
            }
            $scope.alerts = [
                {type: 'danger', msg: msg}
            ];
        };

        $scope.register = function(isValid){
            if(isValid){
                Security.register($scope.user, function(data, status){
                $scope.alerts=[{type: 'success', msg:'Registration successful. A confirmation email has been sent.'}];
            }, alertOnError);
            }
        };

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };

    }]);
