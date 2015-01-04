'use strict';

var HttpBackend = require('http-backend-proxy');

describe('vitals security', function () {

    var  httpBackend = new HttpBackend(browser);

    var httpBackendMock = function () {
        angular.module('httpBackendMock', ['ngMockE2E', 'vitalsApp'])

            .run(function ($httpBackend) {
                $httpBackend.whenGET('http://localhost:5000/rels').respond(200, {});
                $httpBackend.whenGET('http://localhost:5000/auth/confirm?token=foo').respond(200, {'code': 200, 'token': 'bar', 'message':'yay!'});
                $httpBackend.whenGET(/views.*/i).passThrough();
            });
    };

    beforeEach(function(){
        browser.addMockModule('httpBackendMock', httpBackendMock);
    });

    afterEach(function () {
        browser.executeScript('window.localStorage.clear();');
        browser.removeMockModule('httpBackendMock');
    });

    describe('the registration page', function () {

        beforeEach(function () {

            browser.get('/#/register');
        });

        it('should display a confirmation message when registration succeeds', function () {

            httpBackend.whenPOST('http://localhost:5000/auth/register').respond(200, {'code': 200, 'message': 'Registration successful!'});

            element(by.model('user.email')).sendKeys('test@test.com');
            element(by.model('user.password')).sendKeys('supersecret');

            element(by.id('registerSubmit')).click();
            expect(element(by.css('div.alert-success')).isPresent()).toBeTruthy();

        });

        it('should display an error message when registration fails.', function () {

            httpBackend.whenPOST('http://localhost:5000/auth/register').respond(409, {'code': 409, 'message': 'bad stuff happened!'});

            element(by.model('user.email')).sendKeys('test@test.com');
            element(by.model('user.password')).sendKeys('supersecret');
            element(by.css('button')).click();

            expect(element(by.css('div.alert-danger')).isPresent()).toBeTruthy();

        });

    });

    describe('as an anonymous user, when I navigate to the confirmation page', function () {

       beforeEach(function () {
            browser.get('/#/confirm?token=foo');
        });

        it('should notify the user of success when token is valid', function () {
            expect(element(by.css('div.alert-success')).isPresent()).toBeTruthy();
        });

    });
});


