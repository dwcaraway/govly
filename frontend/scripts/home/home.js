angular.module('angular-login.home', ['angular-login.grandfather'])
    .config(function ($stateProvider) {
        'use strict';
        $stateProvider
            .state('app.home', {
                url: '/',
                templateUrl: 'home/home.tpl.html',
                controller: 'HomeController',
                accessLevel: accessLevels.public
            });
    })
    .controller('HomeController', function (loginService, $state) {
        'use strict';

        if(loginService.isLogged){
            $state.go('app.opps');
        }

    });
