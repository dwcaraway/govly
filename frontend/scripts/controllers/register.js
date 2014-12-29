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

        $scope.register = function(){
            Security.register($scope.user, function(){
                $log.info('Registration successful. A confirmation email has been sent.');
            }, function(){
                $log.info('Registration failed!');
            });

        }

    }]);
