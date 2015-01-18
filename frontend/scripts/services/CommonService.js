'use strict';

angular.module('CommonService', ['config'])
    .factory('LinkRelation', ['$log', '$http', 'ENV', function ($log, $http, ENV) {
        var SCHEMA_URL = ENV.apiEndpoint+'/rels';

        var getSchemas = function() {
          return $http.get(SCHEMA_URL);
        };

        return {'getSchemas':getSchemas};
    }])
    .factory('Security', ['$http', 'ENV', '$localForage', function ($http, ENV, $localForage) {
        var AUTH_BASE_URL = ENV.apiEndpoint + '/auth';
        var FOGMINE_TOKEN = 'fogmine_token';

        var register = function(user){
            return $http.post(AUTH_BASE_URL+'/register', user);
        };

        var confirm = function(token){
            return $http.get(AUTH_BASE_URL+'/confirm?token='+token);
        };

        var login = function (username, password) {
            return $http.post(AUTH_BASE_URL + '/login', {
                'username': username,
                'password': password
            }).then(function (data) {
                    return $localForage.setItem(FOGMINE_TOKEN, data.token);
                },
                function (httpError) {
                    console.log('an error happened during login');
                    throw httpError.status;
                });
        };

        var isAuthenticated = function(){
            return $localForage.getItem(FOGMINE_TOKEN);
        };

        var getCurrentUser = function(){
            //TODO get user from JSON token
          return null;
        };

        var logout = function(){
           return $localForage.removeItem(FOGMINE_TOKEN);
        };

        return {'register': register, 'confirm': confirm, 'login': login, 'logout': logout,
            'isAuthenticated': isAuthenticated, 'getCurrentUser':getCurrentUser};

    }]);