'use strict';

describe('Controller: MainCtrl', function () {

  // load the controller's module
  beforeEach(module('vitalsApp'));

  var MainCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    MainCtrl = $controller('MainCtrl', {
      $scope: scope
    });
  }));

  it('should have a real test instead of this placeholder', function () {
    expect(true).toBe(true);
  });
});
