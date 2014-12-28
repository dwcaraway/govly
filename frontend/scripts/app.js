'use strict';

/**
 * @ngdoc overview
 * @name vitalsApp
 * @description
 * # vitalsApp
 *
 * Main module of the application.
 */
angular
  .module('vitalsApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'angulartics',
    'angulartics.google.analytics',
    'angular-jwt',
    'schemaForm',
    'CommonService'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl'
      })
        .when('/register', {
            templateUrl: 'views/register.html',
            controller: 'RegisterCtrl'
        })
      .otherwise({
        redirectTo: '/'
      });
  });
