'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the vitalsApp
 */
angular.module('vitalsApp')
  .controller('MainCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
