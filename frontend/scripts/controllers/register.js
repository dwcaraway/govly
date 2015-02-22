'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:RegisterCtrl
 * @description
 * # RegisterCtrl
 * Controller of the vitalsApp
 */
angular.module('vitalsApp')
    .controller('RegisterCtrl', ['LinkRelation', 'Security', '$scope', '$http', '$log' , function (LinkRelation, $scope, $http, $log) {
        $scope.user = {};
        $scope.alerts = [];

        $scope.register = function (isValid) {
            if (isValid) {
                Security.register($scope.user).success(function () {
                    $scope.alerts = [
                        {type: 'success', msg: 'Registration successful. A confirmation email has been sent.'}
                    ];
                }).error(function (data, status) {
                    $log.debug('data=' + data + ', status= ' + status);
                    if (status === 0) {
                        $scope.alerts = [
                            {type: 'danger', msg: 'No connection!'}
                        ];
                    } else {
                        $scope.alerts = [
                            {type: 'danger', msg: data.message}
                        ];
                    }

                });
            }
        };

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };

    }]);
