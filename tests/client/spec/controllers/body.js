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
        scope;

    // Initialize the controller and a mock scope
    beforeEach(inject(function ($controller, $rootScope, _$httpBackend_, _loginService_) {
        $httpBackend = _$httpBackend_;
        loginService = _loginService_;
        scope = $rootScope.$new();
        BodyController = $controller('BodyController', {
            $scope: scope
        });
    }));

    afterEach(function () {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
    });

    it('should create a loginMe function', function () {
        expect(scope.loginMe).not.toBe(undefined);
    });

    it('should call the loginService with a loginPromise', function () {
        spyOn(loginService, 'loginUser');
        scope.loginMe();
        expect(loginService.loginUser).toHaveBeenCalled();
    });
});
