'use strict';

describe('Controller: ConfirmationCtrl', function () {

  // load the controller's module
  beforeEach(module('vitalsApp'));

  var RegisterCtrl,
    scope, httpBackend;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope, $httpBackend) {
    scope = $rootScope.$new();
    RegisterCtrl = $controller('RegisterCtrl', {
      $scope: scope
    });
    httpBackend = $httpBackend;
  }));

  it('should forward a token in the URL to the API', function () {
      httpBackend.expectGET('http://localhost:5000/auth/confirm?token=foo');
  });

});