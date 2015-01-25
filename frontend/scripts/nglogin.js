angular.module('angular-login', [
    //Mock backend replaced by real servers in production
    //Keep the mock login as first dependency! otherwise may leave
    //mock backend attached in production!
    'angular-login.mock',

    // login service
    'loginService',
    'angular-login.directives',
    // different app sections
    'angular-login.home',
    'angular-login.register',
    'angular-login.error',
    'angular-login.opps',
    // components
    'ngAnimate'
])
    .config(function ($urlRouterProvider) {
        'use strict';
        $urlRouterProvider.otherwise('/');
    })
    .run(function ($rootScope) {
        /**
         * $rootScope.doingResolve is a flag useful to display a spinner on changing states.
         * Some states may require remote data so it will take awhile to load.
         */
        'use strict';
        var resolveDone = function () {
            $rootScope.doingResolve = false;
        };
        $rootScope.doingResolve = false;

        $rootScope.$on('$stateChangeStart', function () {
            $rootScope.doingResolve = true;
        });
        $rootScope.$on('$stateChangeSuccess', resolveDone);
        $rootScope.$on('$stateChangeError', resolveDone);
        $rootScope.$on('$statePermissionError', resolveDone);
    })
    .controller('BodyController', function ($scope, $state, $stateParams, loginService, $timeout) {
        'use strict';
        // Expose $state and $stateParams to the <body> tag
        $scope.$state = $state;
        $scope.$stateParams = $stateParams;

        // loginService exposed and a new Object containing login user/pwd
        $scope.ls = loginService;
        $scope.login = {
            working: false,
            wrong: false
        };

        $scope.loginMe = function () {
            // setup promise, and 'working' flag
            $scope.login.working = true;
            $scope.login.wrong = false;

            loginService.loginUser($scope.login)
                .error(function () {
                    $scope.login.wrong = true;
                    $timeout(function () {
                        $scope.login.wrong = false;
                    }, 8000);
                }).finally(function () {
                    $scope.login.working = false;
                });
        };

        $scope.logoutMe = function (){
            loginService.logoutUser();
        };

    });
