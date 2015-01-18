angular.module('angular-login.home', ['angular-login.grandfather'])
.config(function ($stateProvider) {
        'use strict';
  $stateProvider
    .state('app.home', {
      url: '/',
      templateUrl: 'home/home.tpl.html',
      controller: 'HomeController'
    });
})
.controller('HomeController', function ($scope) {
        'use strict';
  $scope.users = angular.fromJson(localStorage.getItem('userStorage'));
});
