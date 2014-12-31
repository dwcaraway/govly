'use strict';

var HttpBackend = require('http-backend-proxy');

describe('the registration page', function() {
var httpBackend = new HttpBackend(browser);

  var httpBackendMock = function() {
    angular.module('httpBackendMock', ['ngMockE2E', 'vitalsApp'])

      .run(function($httpBackend) {
//        var authenticated = false;
//        var testAccount = {
//          email: 'test@example.com'
//        };
//
//        $httpBackend.whenGET('/api/auth').respond(function(method, url, data, headers) {
//          return authenticated ? [200, testAccount, {}] : [401, {}, {}];
//        });
//
//            $httpBackend.whenPOST('http://localhost:5000/auth/register').respond(function (method, url, data, headers) {
//                return [200, {
//                    msg: "You called /auth/register"
//                }, {'test-header': 'remote success'}];
//            });
//
//        $httpBackend.whenDELETE('/api/auth').respond(function(method, url, data, headers) {
//          authenticated = false;
//          return [204, {}, {}];
//        });

        $httpBackend.whenGET(/.*/).passThrough();
      })
  };
  browser.addMockModule('httpBackendMock', httpBackendMock);

  beforeEach(function(){

    browser.get('/#/register');
//    browser.wait(element(by.model('user.email')).isPresent);
  });


  it('should display a confirmation message when registration succeeds', function() {

    httpBackend.whenPOST('http://localhost:5000/auth/register').respond(200, {'code':200, 'msg':'Registration successful!'});

    element(by.model('user.email')).sendKeys('test@test.com');
    element(by.model('user.password')).sendKeys('supersecret');

    element(by.id('registerSubmit')).click();
    expect(element(by.css('div.alert-success')).isPresent()).toBeTruthy();

  });

  it('should display an error message when registration fails.', function() {

    httpBackend.whenPOST('http://localhost:5000/auth/register').respond(409, {'code':409, 'msg':'bad stuff happened!'});

    element(by.model('user.email')).sendKeys('test@test.com');
    element(by.model('user.password')).sendKeys('supersecret');
    element(by.css('button')).click();

    expect(element(by.css('div.alert-danger')).isPresent()).toBeTruthy();

  });

});