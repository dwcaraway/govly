angular.module('angular-login.grandfather', ['ui.router', 'templates-app', 'config'])
    .config(function ($stateProvider, ENV) {
        'use strict';
        $stateProvider
            .state('app', {
                abstract: true,
                template: '<ui-view></ui-view>',
                resolve: {
                    'login': function (loginService, $q, $http) {
                        var roleDefined = $q.defer();

                        /**
                         * In case there is a pendingStateChange means the user requested a $state,
                         * but we don't know yet user's userRole.
                         *
                         * Calling resolvePendingState makes the loginService retrieve his userRole remotely.
                         */
                        if (loginService.pendingStateChange) {
                            console.log('pendingStateChange is true, so resolvePendingState');
                            return loginService.resolvePendingState($http.get(ENV.apiEndpoint+'/user'));
                        } else {
                            console.log('roleDefined called to resolve: '+angular.toJson(roleDefined));
                            roleDefined.resolve();
                        }
                        return roleDefined.promise;
                    }
                }
            });
    });
