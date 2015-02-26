angular.module('angular-login.reset', ['angular-login.grandfather'])
    .config(function ($stateProvider) {
        'use strict';
        $stateProvider
            .state('app.reset', {
                url: '/reset',
                templateUrl: 'reset/reset.tpl.html',
                controller: 'ResetController',
                accessLevel: accessLevels.anon
            }).state('app.reset.update', {
                url: '/:token',
                templateUrl: 'reset/reset.update.tpl.html',
                controller: 'ResetUpdateController'
            });
    })
    .controller('ResetController', function ($scope, $stateParams, $http, $state, $log, loginService) {
        'use strict';
        $scope.xhr = false;

        $scope.submit = function (formInstance) {
            $scope.xhr = true;

            loginService.reset($scope.email)
                .success(function success(data) {
                    $log.info('post success - ', data);
                    $scope.xhr = false;
                    $scope.sent = true;
                }).error(
                function failure(data) {
                    $scope.xhr = false;

                    if (data.status === 409) {
                        formInstance.email.$error.notFound = true;
                    }

                    formInstance.$setPristine();
                    $log.info('post error - ', data);

                });
        };
    })
    .controller('ResetUpdateController', function ($scope, $stateParams, $http, $state, $log, loginService, $timeout) {
        'use strict';
        $scope.xhr = false;
        $scope.redirect = false;
        $scope.inputType = 'password';
        $scope.registerObj = {};

        // Hide & show password function
        $scope.hideShowPassword = function () {
            if ($scope.inputType === 'password') {
                $scope.inputType = 'text';
            } else {
                $scope.inputType = 'password';
            }
        };

        if (!$stateParams.hasOwnProperty('token') || $stateParams.token.length < 1) {
            $scope.alert = 'Bad password reset URL';
        }

        $scope.submit = function (formInstance) {
            $scope.xhr = true;

            loginService.updatePassword($scope.registerObj.password, $stateParams.token)
                .then(function success(data) {
                    $log.info('post success - ', data);
                    $scope.xhr = false;
                    $scope.redirect = true;

                    $timeout(function () {
                            $state.go('app.opps');
                        }, 1000
                    );
                },
                function failure(data) {
                    $scope.xhr = false;

                    $scope.alert = data.message;

                    formInstance.$setPristine();
                    $log.info('post error - ', data);

                });
        };
    });

