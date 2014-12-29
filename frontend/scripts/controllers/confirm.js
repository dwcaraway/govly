'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:RegisterCtrl
 * @description
 * # RegisterCtrl
 * Controller of the vitalsApp
 */
angular.module('vitalsApp')
    .controller('ConfirmationCtrl', ['Security', '$scope', '$routeParams', function (Security, $scope, $routeParams) {


        $scope.register = function(){
            Security.confirm($routeParams.token, function(){
                $log.info('Account confirmed.');
            }, function(){
                $log.warn('Confirmation failed.');
            });

        }

    }]);