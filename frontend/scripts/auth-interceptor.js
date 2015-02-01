/**
 * Created by dave on 2/1/15.
 */
angular.module('auth-interceptor', ['loginService'])
    .factory('authInterceptor', function ($q, loginService) {
        return {
            request: function (config) {
                var token;
                if (LocalService.get('auth_token')) {
                    token = angular.fromJson(LocalService.get('auth_token')).token;
                }
                if (token) {
                    config.headers.Authorization = 'Bearer ' + token;
                }
                return config;
            },
            responseError: function (response) {
                if (response.status === 401 || response.status === 403) {
                    LocalService.unset('auth_token');
                    $injector.get('$state').go('anon.login');
                }
                return $q.reject(response);
            }
        };
    });