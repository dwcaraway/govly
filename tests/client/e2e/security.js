'use strict';

var HttpBackend = require('http-backend-proxy');

describe('vitals security', function () {

    var httpBackend = new HttpBackend(browser);

    var httpBackendMock = function () {
        angular.module('httpBackendMock', ['ngMockE2E', 'vitalsApp'])

            .run(function ($httpBackend) {
                $httpBackend.whenGET(/.*/).passThrough();
            })
    };

    browser.addMockModule('httpBackendMock', httpBackendMock);

    describe('the registration page', function () {

        beforeEach(function () {

            browser.get('/#/register');
        });

        it('should display a confirmation message when registration succeeds', function () {

            httpBackend.whenPOST('http://localhost:5000/auth/register').respond(200, {'code': 200, 'msg': 'Registration successful!'});

            element(by.model('user.email')).sendKeys('test@test.com');
            element(by.model('user.password')).sendKeys('supersecret');

            element(by.id('registerSubmit')).click();
            expect(element(by.css('div.alert-success')).isPresent()).toBeTruthy();

        });

        it('should display an error message when registration fails.', function () {

            httpBackend.whenPOST('http://localhost:5000/auth/register').respond(409, {'code': 409, 'msg': 'bad stuff happened!'});

            element(by.model('user.email')).sendKeys('test@test.com');
            element(by.model('user.password')).sendKeys('supersecret');
            element(by.css('button')).click();

            expect(element(by.css('div.alert-danger')).isPresent()).toBeTruthy();

        });

    });

    describe('when I follow a link to the account confirmation page', function () {

        afterEach(function () {
            browser.executeScript('window.sessionStorage.clear();');
            browser.executeScript('window.localStorage.clear();');
        });

        it('should forward a token in the URL to the API for validation', function () {
            httpBackend.whenGET('http://localhost:5000/auth/confirm?token=foo').respond(200, {'code': 200, 'token': 'bar'});
            browser.get('/#/confirm?token=foo');
        });

    });
});


