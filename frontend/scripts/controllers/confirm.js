'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:RegisterCtrl
 * @description
 * # RegisterCtrl
 * Controller of the vitalsApp
 */
angular.module('vitalsApp')
    .controller('ConfirmationCtrl', ['Security', '$scope', '$routeParams','$location', function (Security, $scope, $routeParams, $location) {

        $scope.register = function(){
            Security.confirm($routeParams.token, function(data){
                $log.info('Account confirmed.');
                $scope.alerts=[{type:'success', msg:'Account Confirmed!'}];
                localStorage.setItem('fogmine-token', data.token);
//                scope.$apply(function() { $location.path("/"); });
            }, function(){
                $log.warn('Confirmation failed.');
                $scope.alerts=[{type:'danger', msg:'An Error Occurred'}];
            });
        }
    }]);