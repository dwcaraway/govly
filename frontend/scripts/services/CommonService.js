'use strict';

angular.module('CommonService', ['config'])
    .factory('LinkRelation', ['$log', '$http', 'ENV', function ($log, $http, ENV) {
        var SCHEMA_URL = ENV.apiEndpoint+'/rels';
        var schemas = {};

        $http.get(SCHEMA_URL).success(function (data) {
            schemas = data;
        }).error(function () {
            $log.warn('could not reach server');
        });

        var getSchemas = function() {
          return schemas;
        };

        return {'getSchemas':getSchemas};
    }])
    .factory('Security', ['$http', 'ENV', function ($http, ENV) {
       var AUTH_BASE_URL = ENV.apiEndpoint + '/auth';

        var register = function(user, success_callback, error_callback){
            return $http.post(AUTH_BASE_URL+'/register', user);
        };

        var confirm = function(token, success_callback, error_callback){
            return $http.get(AUTH_BASE_URL+'/confirm?token='+token);
        };

        var login = function(username, password){
            return $http.post(AUTH_BASE_URL+'/login', {'username':username, 'password':password});
        };

        return {'register': register, 'confirm': confirm, 'login': login};

    }]);