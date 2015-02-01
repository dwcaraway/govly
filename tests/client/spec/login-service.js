/**
 * Created by DavidWCaraway on 1/18/15.
 */
describe('Provider: login-service', function () {
    'use strict';

    var loginService;

    beforeEach(module('loginService'));

    // Initialize the controller and a mock scope
    beforeEach(inject(function (_loginService_) {
        loginService = _loginService_;
        localStorage.removeItem('userToken');
    }));

    describe('loginHandler', function () {
        it('should create loginService.user with JSON from first argument', function () {
            var user  = {foo:'bar'};

            expect(loginService.user).toEqual({});
            loginService.loginHandler(user);
            expect(loginService.user).toEqual(user);
        });

        it('should extend loginService.user with JSON from subsequent calls', function () {
            var user1  = {foo:'bar'};
            var user2  = {'baz':'qux'};
            var combined = {'foo':'bar', 'baz':'qux'};

            expect(loginService.user).toEqual({});
            loginService.loginHandler(user1);
            expect(loginService.user).toEqual(user1);
            loginService.loginHandler(user2);
            expect(loginService.user).toEqual(combined);

        });

        it('should set the user as logged in when called', function () {
            //TODO this is not secure!
            var user  = {foo:'bar'};

            expect(loginService.isLogged).toBeFalsy();
            loginService.loginHandler(user);
            expect(loginService.isLogged).toBeTruthy();

        });

        it('should set the user role when called', function () {
            var user  = {roles: [userRoles.admin]};

            expect(loginService.userRole).toEqual(userRoles.public);
            loginService.loginHandler(user);
            expect(loginService.userRole).toBe(user.roles[0]);

        });

        it('should set the user in the loginService', function () {
            var user  = {roles: [userRoles.admin]};

            expect(loginService.userRole).toEqual(userRoles.public);
            loginService.loginHandler(user);
            expect(loginService.user).toEqual(user);

        });

        it('should set userRole to public if not in user object', function () {
            var user  = {foo: 'bar'};

            expect(loginService.userRole).toEqual(userRoles.public);
            loginService.loginHandler(user);
            expect(loginService.userRole).toEqual(userRoles.public);

        });

        it('should set a token', function () {
            var user  = {token: 'supersecret'};

            expect(localStorage.getItem('userToken')).toEqual(null);
            loginService.loginHandler(user);
            expect(localStorage.getItem('userToken')).toEqual(user.token);

        });

        it('should maintain token in localStorage over window refresh', inject(function($window){
            var user = {token: 'supersecret'};

            loginService.loginHandler(user);
            expect(localStorage.getItem('userToken')).toEqual(user.token);

            $window.location.reload();
            expect(localStorage.getItem('userToken')).toEqual(user.token);
        }));

        it('should add jwt header to requests', inject(function($http, $httpBackend){
            var user = {token: 'supersecret'};

            $httpBackend.expectGET('/checkheaders').respond(200);

            //login should set headers
            loginService.loginHandler(user);

            //Make request which httpBackend will intercept and set the expectation
            $http.get('/checkheaders');

            //Flush triggers the intercept and resolves the $http promise
            $httpBackend.flush();
            expect($http.defaults.headers.common['Authorization']).toEqual('Bearer '+user.token);
        }));
    });
});