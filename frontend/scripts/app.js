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
    'ngResource',
    'ngRoute',
    'ui.router',
    'ngSanitize',
    'ngTouch',
    'angulartics',
    'angulartics.google.analytics',
    'angular-jwt',
    'ui.bootstrap',
    'permission',
    'CommonService'
  ])
  .config(function ($stateProvider, $urlRouterProvider, $httpProvider, jwtInterceptorProvider) {

              //Configure Jason Web Token support
        jwtInterceptorProvider.tokenGetter = function () {
            return localStorage.getItem('fogmine_token');
        };
     $httpProvider.interceptors.push('jwtInterceptor');

      // For any unmatched url, send to /
      $urlRouterProvider.otherwise("/");

      $stateProvider
          .state('register',{
              url: '/register',
              templateUrl: "views/register.html",
              controller: 'RegisterCtrl',
              data:{
                  permissions: {
                      only: ['anonymous']
                  }
              }

          })
          .state('confirm', {
            url: '/confirm',
                templateUrl: 'views/confirm.html',
              controller: 'ConfirmationCtrl'
        })
          .state('main', {
              url: '/',
              templateUrl: "views/main.html",
              controller: 'MainCtrl',
              data: {
              permissions: {
                  except: ['anonymous'],
                  redirectTo: 'register'
              }
              }
          });
  })
    .run(function (Permission) {
      // Define anonymous role
      Permission.defineRole('anonymous', function (stateParams) {
        // If the returned value is *truthy* then the user has the role, otherwise they don't
        return true;
      });
    });
