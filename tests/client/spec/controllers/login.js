describe('Controller: LoginCtrl', function () {

    'use strict';

    // load the controller's module
    beforeEach(module('vitalsApp'));

    var scope, $httpBackend, Security;

    // Initialize the controller and a mock scope
    beforeEach(inject(function ($rootScope, _$httpBackend_, _Security_) {
        scope = $rootScope.$new();
        $httpBackend = _$httpBackend_;
        Security = _Security_;
    }));

    afterEach(function () {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
    });

    describe('when I successfully authenticate', function () {
        var user = {'email': 'user@foo.com', 'password': 'supersecret'};
        var response = {'token': 'somerandomtoken'};
        var promise = null;

        beforeEach(function(){
            $httpBackend.expectPOST('http://localhost:5000/auth/login').respond(response);
            $httpBackend.expectGET('views/login.html').respond('');
        });

        it('should store an access token', function () {
            Security.login(user.email, user.password).then(
                function(){
                    expect(localStorage.getItem('fogmine_token')).toBe(response.token);
                }
            );

            $httpBackend.flush();
        });

        it('should indicate that I am authenticated', function () {
            expect(Security.isAuthenticated()).toBe(false);

            Security.login(user.email, user.password).then(
                function(){
                    expect(Security.isAuthenticated()).toBe(true);
                }
            );

            $httpBackend.flush();
        });

    });

    describe('when I log out', function () {

        it('should remove a token from local storage', function () {

            //Setup
            scope.user = {'email': 'user@foo.com', 'password': 'supersecret'};
            var response = {'token': 'somerandomtoken'};

            $httpBackend.expectPOST('http://localhost:5000/auth/login').respond(response);
            $httpBackend.expectGET('views/login.html').respond('');

            Security.login().then(function () {
                    Security.logout().then(
                        function () {
                            expect(localStorage.getItem('fogmine_token')).toBe(null);
                        }
                    );
                }
            );//should remove the token

            $httpBackend.flush();


        });

    });
});
