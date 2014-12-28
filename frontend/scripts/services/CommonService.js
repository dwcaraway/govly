'use strict'

angular.module('CommonService', [])
    .factory('LinkRelation', ['$log', '$http', function ($log, $http) {
        var SCHEMA_URL = 'https://api.fogmine.com/rels';
        var schemas = {};

        $http.get(SCHEMA_URL).success(function (data) {
            $log.debug('schemas: ' + JSON.stringify(data));
            schemas = data;
        }).error(function (status) {
            $log.debug('could not reach server');
        });

        var getSchemas = function() {
          return schemas;
        };

        return {'getSchemas':getSchemas};
    }]);