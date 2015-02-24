/* jshint -W084 */
angular.module('angular-login.mock', ['ngMockE2E', 'config'])
    .factory('delayHTTP', function ($q, $timeout) {
        'use strict';

        return {
            request: function (request) {
                var delayedResponse = $q.defer();
                $timeout(function () {
                    delayedResponse.resolve(request);
                }, 700);
                return delayedResponse.promise;
            },
            response: function (response) {
                var deferResponse = $q.defer();

                if (response.config.timeout && response.config.timeout.then) {
                    response.config.timeout.then(function () {
                        deferResponse.reject();
                    });
                } else {
                    deferResponse.resolve(response);
                }

                return $timeout(function () {
                    deferResponse.resolve(response);
                    return deferResponse.promise;
                });
            }
        };
    })
// delay HTTP
    .config(['$httpProvider', function ($httpProvider) {
        'use strict';
        $httpProvider.interceptors.push('delayHTTP');
    }])
    .run(function ($httpBackend, $log, $http, ENV) {
            'use strict';
        var userStorage = angular.fromJson(localStorage.getItem('userStorage')),
            emailStorage = angular.fromJson(localStorage.getItem('emailStorage')),
            tokenStorage = angular.fromJson(localStorage.getItem('tokenStorage')) || {},
            oppsExample = angular.fromJson(localStorage.getItem('oppsExample'));

        var AUTH_BASE_URL = ENV.apiEndpoint + '/auth';

        if (userStorage === null || emailStorage === null) {
            userStorage = {
                'john.dott@myemail.com': {
                    name: 'John',
                    username: 'johnm',
                    password: 'hello',
                    email: 'john.dott@myemail.com',
                    userRole: userRoles.user,
                    tokens: []
                },
                'bitter.s@provider.com': {
                    name: 'Sandra',
                    username: 'sandrab',
                    password: 'world',
                    email: 'bitter.s@provider.com',
                    userRoles: userRoles.admin,
                    tokens: []
                }
            };
            emailStorage = {
                'john.dott@myemail.com': 'johnm',
                'bitter.s@provider.com': 'sandrab'
            };
            localStorage.setItem('userStorage', angular.toJson(userStorage));
            localStorage.setItem('emailStorage', angular.toJson(emailStorage));
        }

        if (oppsExample === null){
            $http.get('/data/oppsExample.json').success(function (data){
                $log.debug('loading example opps data into local storage');
                oppsExample = data;
                localStorage.setItem('oppsExample', angular.toJson(data));
            }).error(function (){
                $log.warn('could not resolve example opps data');
            });
        }

        /**
         * Generates random Token
         */
        var randomUUID = function () {
            var charSet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            var randomToken = '';
            for (var i = 0; i < 36; i++) {
                if (i === 8 || i === 13 || i === 18 || i === 23) {
                    randomToken += '';
                    continue;
                }
                var randomPoz = Math.floor(Math.random() * charSet.length);
                randomToken += charSet.substring(randomPoz, randomPoz + 1);
            }

            console.log('generated new token: '+randomToken);
            return randomToken;
        };

        // fakeLogin
        $httpBackend.when('POST', AUTH_BASE_URL+'/login').respond(function (method, url, data) {
            var postData = angular.fromJson(data),
                user = userStorage[postData.username],
                newToken;
            $log.info(method, '->', url, 'user defined? '+angular.isDefined(user));

            if (angular.isDefined(user) && user.password === postData.password) {
                newToken = randomUUID();
                user.tokens = [newToken];
                tokenStorage[newToken] = postData.username;
                localStorage.setItem('userStorage', angular.toJson(userStorage));//Is the update to userStorage necessary?
                localStorage.setItem('tokenStorage', angular.toJson(tokenStorage));

                //TODO remove debug statement below
                console.log('tokenStorage keys'+Object.keys(angular.fromJson(localStorage.getItem('tokenStorage'))));
                return [200, {name: user.name, roles: [user.userRole], token: newToken}, {}];
            } else {
                return [401, 'wrong combination email/password', {}];
            }
        });

        // fakeLogout
        $httpBackend.when('GET', AUTH_BASE_URL+'/logout').respond(function (method, url, data, headers) {
            var queryToken, userTokens;
            $log.info(method, '->', url);

            if (queryToken = localStorage.getItem('userToken')) {
                if (angular.isDefined(tokenStorage[queryToken])) {
                    userTokens = userStorage[tokenStorage[queryToken]].tokens;
                    // Update userStorage AND tokenStorage
                    userTokens.splice(userTokens.indexOf(queryToken));
                    delete tokenStorage[queryToken];

                    //TODO remove debug statements
                    console.log('queryToken ['+queryToken+'] removed, tokenStorage: ['+localStorage.getItem('tokenStorage')+']');

                    localStorage.setItem('userStorage', angular.toJson(userStorage));
                    localStorage.setItem('tokenStorage', angular.toJson(tokenStorage));
                    return [200, {}, {}];
                } else {
                    return [401, 'auth token invalid or expired', {}];
                }
            } else {
                return [401, 'auth token invalid or expired', {}];
            }
        });

        // fakeUser
        $httpBackend.when('GET', '/user').respond(function (method, url, data, headers) {
            var queryToken, userObject;
            $log.info(method, '->', url);

            // if is present in a registered users array.
            if (queryToken = localStorage.getItem('userToken')) {
                if (angular.isDefined(tokenStorage[queryToken])) {
                    userObject = userStorage[tokenStorage[queryToken]];
                    return [200, {token: queryToken, name: userObject.name, roles: [userObject.userRole]}, {}];
                } else {
                    console.log('auth token ['+queryToken+'] not found in tokenStorage');
                    return [401, 'auth token invalid or expired', {}];
                }
            } else {
                console.log('auth token not found in request headers');
                return [401, 'auth token invalid or expired', {}];
            }
        });

        // fakeRegister
        $httpBackend.when('POST', AUTH_BASE_URL+'/register').respond(function (method, url, data) {
            var postData = angular.fromJson(data),
                newUser,
                errors = [];
            $log.info(method, '->', url);

            return [201, {token: 'something', name:postData['firstName']}];
            //if (angular.isDefined(userStorage[postData.username])) {
            //    errors.push({field: 'username', name: 'used'});
            //}
            //
            //if (angular.isDefined(emailStorage[postData.email])) {
            //    errors.push({field: 'email', name: 'used'});
            //}
            //
            //if (errors.length) {
            //    return [409, {
            //        valid: false,
            //        errors: errors
            //    }, {}];
            //} else {
            //    newUser = angular.extend(postData, {roles: [userRoles[postData.role]], tokens: []});
            //    delete newUser.role;
            //
            //    userStorage[newUser.username] = newUser;
            //    emailStorage[newUser.email] = newUser.username;
            //    localStorage.setItem('userStorage', angular.toJson(userStorage));
            //    localStorage.setItem('emailStorage', angular.toJson(emailStorage));
            //    return [201, {valid: true, creationDate: Date.now()}, {}];
            //}
        });

        $httpBackend.when('GET', /data\/.*\.json/).passThrough();

        $httpBackend.when('GET', /http:\/\/localhost:5000\/api\/opps.*/).respond(function (method, url) {
            $log.info(method, '->', url);
            return [200, oppsExample];
        });

        $httpBackend.when('POST', AUTH_BASE_URL+'/confirm').respond(function (method, url) {
            $log.info(method, '->', url);

            var userResp = {name: 'bilbo', roles: [userRoles.user], token: randomUUID()};

            return [200, {user: userResp, status: 200, message: 'foo'}, {}];
        });

    });
