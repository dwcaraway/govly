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
        'LocalForageModule',
        'CommonService',
        'ngAnimate',
        'templates-app'
    ])
    .config(function ($stateProvider, $urlRouterProvider, $httpProvider, jwtInterceptorProvider) {

        //Configure Jason Web Token support
        jwtInterceptorProvider.tokenGetter = function () {
            return localStorage.getItem('fogmine_token');
        };
        $httpProvider.interceptors.push('jwtInterceptor');

        // For any unmatched url, send to /
        $urlRouterProvider.otherwise('/');

        $stateProvider
            .state('register', {
                url: '/register',
                templateUrl: 'views/register.html',
                controller: 'RegisterCtrl'
            })
            .state('confirm', {
                url: '/confirm?token',
                templateUrl: 'views/confirm.html',
                controller: 'ConfirmationCtrl'
            })
            .state('login', {
                url: '/login',
                templateUrl: 'views/login.html',
                controller: 'LoginCtrl',
                data: {
                    permissions: {
                        only: ['anonymous']
                    }
                }
            })
            .state('logout', {
                url: '/logout',
                templateUrl: 'views/logout.html',
                controller: 'LogoutCtrl'
            })
            .state('main', {
                url: '/',
                templateUrl: 'views/main.html',
                controller: 'MainCtrl'
            });
    });
