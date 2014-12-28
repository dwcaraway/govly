'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:RegisterCtrl
 * @description
 * # RegisterCtrl
 * Controller of the vitalsApp
 */
angular.module('vitalsApp')
    .controller('RegisterCtrl', ['LinkRelation', '$scope', function (LinkRelation, $scope) {

//        $scope.schema = LinkRelation.getSchemas().event;
$scope.schema =  {
            "$schema": "http://json-schema.org/schema#",

            "type": "object",
            "properties": {
                "password": {"type": "string", "minLength":8, "maxLength":120
},
                "email": {"type": "string", "format":"email"}
            },
            "required": ["email", "password"]
        }

        $scope.form = [
            "*",
            {
                type: "submit",
                title: "Save"
            }
        ];

        $scope.model = {};

    }]);
