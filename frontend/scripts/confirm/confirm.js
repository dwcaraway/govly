angular.module('angular-login.confirm', ['angular-login.grandfather'])
    .config(function ($stateProvider) {
        'use strict';
        $stateProvider
            .state('app.confirm', {
                url: '/confirm?token',
                templateUrl: 'confirm/confirm.tpl.html',
                controller: 'ConfirmationController',
                accessLevel: accessLevels.public
            });
    })
    .controller('ConfirmationController', function ($scope, $stateParams, $log, $state, $timeout, loginService) {
        'use strict';
        if (!$stateParams.token) {
            $scope.alert = 'Bad confirmation URL';
            return;
        }

        var init = function() {
            loginService.confirm($stateParams.token).
                then(
                function success() {
                    $scope.confirmed = true;

                    $timeout(function () {
                            $state.go('app.opps');
                        }, 1000
                    );
                },
                function error(data, status) {
                    if (status === 0) {
                        $scope.alert = 'Unable to connect';
                    } else if (data.message) {
                        $scope.alert = data.message;
                    } else {
                        $scope.alert = "Unknown error";
                    }

                }
            );
        };

        init();
    });