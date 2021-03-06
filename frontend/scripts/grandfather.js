angular.module('angular-login.grandfather', ['ui.router', 'templates-app', 'config', 'angulartics',
    'angulartics.google.analytics'])
    .config(function ($stateProvider, $analyticsProvider) {
        'use strict';
        $stateProvider
            .state('app', {
                abstract: true,
                template: '<ui-view></ui-view>',
                resolve: {
                    'login': function (loginService, $q) {
                        var roleDefined = $q.defer();

                        /**
                         * In case there is a pendingStateChange means the user requested a $state,
                         * but we don't know yet user's userRole.
                         *
                         * Calling resolvePendingState makes the loginService retrieve his userRole remotely.
                         */
                        if (loginService.pendingStateChange) {
                            console.log('pendingStateChange is true, so resolvePendingState');
                            return loginService.resolvePendingState();
                        } else {
                            roleDefined.resolve();
                        }
                        return roleDefined.promise;
                    }
                }
            });
    });
