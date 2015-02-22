angular.module('angular-login.register', ['angular-login.grandfather'])
    .config(function ($stateProvider) {
        'use strict';
        $stateProvider
            .state('app.register', {
                url: '/register',
                templateUrl: 'register/register.tpl.html',
                controller: 'RegisterController',
                accessLevel: accessLevels.anon
            });
    })
    .controller('RegisterController', function ($scope, $http, $timeout, $state, $log, loginService) {
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

        $scope.submit = function (formInstance) {
            // xhr is departing
            $scope.xhr = true;
            $scope.inputType = 'password';

            $log.debug('cross domain post!');

            loginService.register($scope.registerObj)
                .then(function success(data) {
                    $log.info('post success - ', data);
                    $scope.xhr = false;
                    $scope.redirect = true;

                    $state.go('app.opps');
                },
                function failure(data) {
                    if(data.status === 409){
                        formInstance.email.$error.used = true;
                    }

                    formInstance.$setPristine();
                    $log.info('post error - ', data);
                    $scope.xhr = false;
                });
        };
    });
