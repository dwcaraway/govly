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
        'config',
    'ngAnimate',
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
        .when('/register', {
            templateUrl: 'views/register.html',
            controller: 'RegisterCtrl'
        })
      .otherwise({
        redirectTo: '/'
      });

  });
