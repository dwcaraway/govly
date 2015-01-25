/**
 * Created by dwcaraway on 1/20/15.
 */
'use strict';

describe('Controller: BodyController', function () {

    // load the controller's module
    beforeEach(module('angular-login'));

    var BodyController,
        $httpBackend,
        loginService,
        scope, $q;

    // Initialize the controller and a mock scope
    beforeEach(inject(function ($controller, $rootScope, _$httpBackend_, _loginService_, _$q_) {
        $httpBackend = _$httpBackend_;
        loginService = _loginService_;
        scope = $rootScope.$new();
        BodyController = $controller('BodyController', {
            $scope: scope
        });
        $q = _$q_;
    }));

    afterEach(function () {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
    });

    it('should create a loginMe function', function () {
        expect(scope.loginMe).not.toBe(undefined);
    });

    it('should create a logoutMe function', function () {
        expect(scope.logoutMe).not.toBe(undefined);
    });

    it('should call the loginService.loginUser when loginMe is called', function () {
        spyOn(loginService, 'loginUser').and.callThrough(); //Call through returns $http's promise
        scope.loginMe();
        expect(loginService.loginUser).toHaveBeenCalled();
    });

    it('should call loginService.logoutUser when logoutMe is called', function () {
        spyOn(loginService, 'logoutUser');
        scope.logoutMe();
        expect(loginService.logoutUser).toHaveBeenCalled();
    });
});
