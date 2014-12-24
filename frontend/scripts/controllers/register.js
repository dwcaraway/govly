'use strict';

/**
 * @ngdoc function
 * @name vitalsApp.controller:RegisterCtrl
 * @description
 * # RegisterCtrl
 * Controller of the vitalsApp
 */
angular.module('vitalsApp')
    .controller('RegisterCtrl', function ($http) {


        // Simple POST request example (passing data) :
        $http.post('http://localhost:5000/register', {email: 'hello word!', password: 'foofoofoo'}).
            success(function (data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                console.log('status'+status)
                console.log('data'+ data)
            }).
            error(function (data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                console.log('something bad happened')
            });


    });
