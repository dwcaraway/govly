'use strict';

describe('Controller: ConfirmationCtrl', function () {

  // load the controller's module
  beforeEach(module('vitalsApp'));

  var confirmationCtrl,
    scope, httpBackend, routeParams;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope, $httpBackend, $routeParams) {
    scope = $rootScope.$new();
    confirmationCtrl = $controller('ConfirmationCtrl', {
      $scope: scope
    });
    httpBackend = $httpBackend;
      routeParams = $routeParams;
  }));

});