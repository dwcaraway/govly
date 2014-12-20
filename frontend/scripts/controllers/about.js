'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the vitalsApp
 */
angular.module('vitalsApp')
  .controller('AboutCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
