describe('the registration page', function() {
  it('should display a confirmation message when registration succeeds', function() {
    browser.get('/#/register');

    element(by.model('user.email')).sendKeys('test@test.com');
    element(by.model('user.password')).sendKeys('supersecret');

    //Stub the $HTTPBackend now for a positive 200 response
    var HttpBackend = require('http-backend-proxy');
    var proxy = new HttpBackend(browser);
    proxy.whenPOST('http://localhost:5000/auth/register').respond(200);

    element(by.id('registerSubmit')).click();

    expect(false).toEqual(true);
  });
});