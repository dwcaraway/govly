/**
 * Created by DavidWCaraway on 1/18/15.
 */
describe('Provider: login-service', function () {
    'use strict';

    var loginService;

    beforeEach(module('loginService', 'angular-login.grandfather', 'angular-login.home'));

    // Initialize the controller and a mock scope
    beforeEach(inject(function (_loginService_) {
        loginService = _loginService_;
        localStorage.removeItem('userToken');
    }));

    describe('loginHandler', function () {
        it('should create loginService.user with JSON from first argument', function () {
            var user = {foo: 'bar'};

            expect(loginService.user).toEqual({});
            loginService.loginHandler(user);
            expect(loginService.user).toEqual(user);
        });

        it('should extend loginService.user with JSON from subsequent calls', function () {
            var user1 = {foo: 'bar'};
            var user2 = {'baz': 'qux'};
            var combined = {'foo': 'bar', 'baz': 'qux'};

            expect(loginService.user).toEqual({});
            loginService.loginHandler(user1);
            expect(loginService.user).toEqual(user1);
            loginService.loginHandler(user2);
            expect(loginService.user).toEqual(combined);

        });

        it('should set the user as logged in when called', function () {
            //TODO this is not secure!
            var user = {foo: 'bar'};

            expect(loginService.isLogged).toBeFalsy();
            loginService.loginHandler(user);
            expect(loginService.isLogged).toBeTruthy();

        });

        it('should set the user role when called', function () {
            var user = {roles: [userRoles.admin]};

            expect(loginService.userRole).toEqual(userRoles.public);
            loginService.loginHandler(user);
            expect(loginService.userRole).toBe(user.roles[0]);

        });

        it('should set the user in the loginService', function () {
            var user = {roles: [userRoles.admin]};

            expect(loginService.userRole).toEqual(userRoles.public);
            loginService.loginHandler(user);
            expect(loginService.user).toEqual(user);

        });

        it('should set userRole to public if not in user object', function () {
            var user = {foo: 'bar'};

            expect(loginService.userRole).toEqual(userRoles.public);
            loginService.loginHandler(user);
            expect(loginService.userRole).toEqual(userRoles.public);

        });

        it('should set a token', function () {
            var user = {token: 'supersecret'};

            expect(localStorage.getItem('userToken')).toEqual(null);
            loginService.loginHandler(user);
            expect(localStorage.getItem('userToken')).toEqual(user.token);

        });
    });
    describe('authInterceptor', function () {

        it('should add jwt header to requests when authenticated', inject(function ($http, $httpBackend) {
            var user = {token: 'supersecret'};

            $httpBackend.expectGET('/checkheaders', function (headers) {
                expect(headers.Authorization).toEqual('Bearer ' + user.token);

                return true;//Have to return true to match the headers
            }).respond(200);

            //login should set headers
            loginService.loginHandler(user);

            //Make request which httpBackend will intercept and set the expectation
            $http.get('/checkheaders');

            //Flush triggers the intercept and resolves the $http promise
            $httpBackend.flush();
        }));

        it('should NOT add jwt header to requests when NOT authenticated', inject(function ($http, $httpBackend) {

            $httpBackend.expectGET('/checkheaders', function (headers) {
                expect(headers).not.toContain('Authorization');
                return true;//Have to return true to match the headers
            }).respond(200);

            //Make request which httpBackend will intercept and set the expectation
            $http.get('/checkheaders');

            //Flush triggers the intercept and resolves the $http promise
            $httpBackend.flush();
        }));
    });

    describe('managePermissions', function () {

        it('should call logoutUser when a 4xx authorization error occurs', inject(function ($rootScope, $state) {
            spyOn(loginService, 'logoutUser').and.callThrough();
            spyOn($state, 'go').and.returnValue('foo');//stub $state.go since it's called at the end when an error occurred

            //Broadcast the stateChangeError as if we're ui-router. we add a 401 error to trigger the logoutUser cal
            $rootScope.$broadcast('$stateChangeError', {}, {}, {}, {}, 401);
            expect(loginService.logoutUser).toHaveBeenCalled();
        }));

        it('should call logoutUser when a 5xx server error occurs', inject(function ($rootScope, $state) {
            spyOn(loginService, 'logoutUser').and.callThrough();
            spyOn($state, 'go').and.returnValue('foo');//stub $state.go since it's called at the end when an error occurred

            //Broadcast the stateChangeError as if we're ui-router. we add a 401 error to trigger the logoutUser cal
            $rootScope.$broadcast('$stateChangeError', {}, {}, {}, {}, 500);
            expect(loginService.logoutUser).toHaveBeenCalled();
        }));
    });

});