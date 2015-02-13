angular.module('loginService', ['ui.router', 'config'])
    .config(function ($httpProvider) {
        'use strict';
        //Interceptor to put the Authorization header in requests if user is authenticated
        $httpProvider.interceptors.push('authInterceptor');

    })
    .provider('loginService', function (ENV) {
        'use strict';

        var userToken = localStorage.getItem('userToken'),
            errorState = 'app.error',//State user is directed to when error occurs
            loginState = 'app.opps',//State user is directed to when logging in
            logoutState = 'app.home'; //State user is directed to when logging out

        var AUTH_BASE_URL = ENV.apiEndpoint + '/auth';

        this.$get = function ($rootScope, $http, $q, $state, $log) {

            /**
             * Low-level, private functions.
             */
            var setToken = function (token) {
                if (!token) {
                    //TODO remove the debug console below
                    $log.log('setToken called without token, removing any userToken entries');
                    localStorage.removeItem('userToken');
                } else {
                    localStorage.setItem('userToken', token);
                }
            };

            var setUserRole = function (role) {
                if (role) {
                    //TODO change this to process all roles, not just first one? dwc
                    $log.log('setUserRole called, role is ' + role[0]);
                    wrappedService.userRole = role[0];

                    //Persist the role for reloads
                    localStorage.setItem('userRole', angular.toJson(wrappedService.userRole));
                } else {
                    //if role not in userRoles, then we're done here
                    $log.log('setUserRole called with null: reset to public role');
                    wrappedService.userRole = userRoles.public;
                    localStorage.removeItem('userRole');
                }
            };

            var loadSavedData = function () {
                var userJsonData = localStorage.getItem('userData');

                if (!userToken) {
                    setUserRole();
                    localStorage.removeItem('userData');
                    //wrappedService.isLogged = false;
                    //wrappedService.doneLoading = true;
                }else if(userJsonData){
                    wrappedService.loginHandler(angular.fromJson(userJsonData));
                    wrappedService.doneLoading = true;
                }
            };

            var managePermissions = function () {
                // Register routing function.
                $rootScope.$on('$stateChangeStart', function (event, to, toParams) {

                    /**
                     * $stateChangeStart is a synchronous check to the accessLevels property
                     * if it's not set, it will setup a pendingStateChange and will let
                     * the grandfather resolve do his job.
                     *
                     * In short:
                     * If accessLevels is still undefined, it let the user change the state.
                     * Grandfather.resolve will either let the user in or reject the promise later!
                     */
                    if (wrappedService.userRole === null) {
                        $log.log('statechnage started, but user role is null, so start spinners and tell grandfather to resolve user');
                        wrappedService.doneLoading = false;
                        wrappedService.pendingStateChange = {
                            to: to,
                            toParams: toParams
                        };
                    }

                    // if the state has undefined accessLevel, anyone can access it.
                    // NOTE: if `wrappedService.userRole === undefined` means the service still doesn't know the user role,
                    // we need to rely on grandfather resolve, so we let the stateChange success, for now.
                    else if (to.accessLevel && !(to.accessLevel.bitMask & wrappedService.userRole.bitMask)) {
                        $log.log('Unauthorized: state permission error');
                        event.preventDefault();
                        $rootScope.$emit('$statePermissionError');
                        $state.go(errorState, {error: 'unauthorized'}, {location: false, inherit: false});
                    }
                });

                /**
                 * Gets triggered when a resolve isn't fulfilled
                 * NOTE: when the user doesn't have required permissions for a state, this event
                 *       it's not triggered.
                 *
                 * In order to redirect to the desired state, the $http status code gets parsed.
                 * If it's an HTTP code (ex: 403), could be prefixed with a string (ex: resolvename403),
                 * to handle same status codes for different resolve(s).
                 * This is defined inside $state.redirectMap.
                 */
                $rootScope.$on('$stateChangeError', function (event, to, toParams, from, fromParams, _error_) {
                    /**
                     * This is a very clever way to implement failure redirection.
                     * You can use the value of redirectMap, based on the value of the rejection
                     * So you can setup DIFFERENT redirections based on different promise errors.
                     */
                    var redirectObj;
                    // in case the promise given to resolve function is an $http request
                    // the error is a object containing the error and additional informations
                    var error = (typeof _error_ === 'object') ? _error_.status.toString() : _error_;
                    // in case of a random 4xx/5xx status code from server, user gets loggedout
                    // otherwise it *might* forever loop (look call diagram)
                    $log.log('event ', angular.toJson(event),'to ', to, 'error ',error);
                    if (/^[45]\d{2}$/.test(error) || error === 0 || !error) {
                        //TODO remove debug statement

                        $log.log('$stateChangeError matches 4xx/5xx status code or something weird happened and its 0 or undefined, initiating logout');
                        wrappedService.doneLoading = true;
                        wrappedService.logoutUser();
                    }
                    /**
                     * Generic redirect handling.
                     * If a state transition has been prevented and it's not one of the 2 above errors, means it's a
                     * custom error in your application.
                     *
                     * redirectMap should be defined in the $state(s) that can generate transition errors.
                     */
                    if (angular.isDefined(to.redirectMap) && angular.isDefined(to.redirectMap[error])) {
                        if (typeof to.redirectMap[error] === 'string') {
                            return $state.go(to.redirectMap[error], {error: error}, {location: false, inherit: false});
                        } else if (typeof to.redirectMap[error] === 'object') {
                            redirectObj = to.redirectMap[error];
                            return $state.go(redirectObj.state, {error: redirectObj.prefix + error}, {
                                location: false,
                                inherit: false
                            });
                        }
                    }
                    return $state.go(errorState, {error: error}, {location: false, inherit: false});
                });
            };

            /**
             * High level, public methods
             */
            var wrappedService = {
                loginHandler: function (user) {
                    /**
                     * Custom logic to manually set userRole goes here
                     *
                     * Commented example shows an userObj coming with a 'completed'
                     * property defining if the user has completed his registration process,
                     * validating his/her email or not.
                     *
                     * EXAMPLE:
                     * if (user.hasValidatedEmail) {
         *   wrappedService.userRole = userRoles.registered;
         * } else {
         *   wrappedService.userRole = userRoles.invalidEmail;
         *   $state.go('app.nagscreen');
         * }
                     */
                    $log.log('loginHandler called: '+angular.toJson(user));
                    // setup token
                    setToken(user.token);
                    // update user
                    angular.extend(wrappedService.user, user);
                    // flag true on isLogged
                    wrappedService.isLogged = true;
                    // update userRole
                    setUserRole(user.roles);
                    return user;
                },
                loginUser: function (user) {
                    return $http.post(AUTH_BASE_URL + '/login', {
                        'username': user.email,
                        'password': user.password
                    }).success(function(data) {
                            //Save the last successful login to userData localStorage
                            localStorage.setItem('userData', angular.toJson(data));
                            wrappedService.loginHandler(data);
                            $state.go(loginState);
                    }
                    );
                },
                logoutUser: function () {
                    /**
                     * De-registers the userToken remotely
                     * then clears the loginService as it was on startup
                     */
                    //TODO remove debug statement
                    $log.log('logout called');
                    if(this.isLogged) {
                        $http.get(AUTH_BASE_URL + '/logout');
                    }
                    setToken();
                    setUserRole();
                    this.user = {};
                    this.isLogged = false;
                    $state.go(logoutState);
                },
                resolvePendingState: function (_httpPromise_) {
                    var checkUser = $q.defer(),
                        self = this,
                        pendingState = self.pendingStateChange;

                    var httpPromise = _httpPromise_ ? _httpPromise_ : $http.get(ENV.apiEndpoint+'/user');

                    // When the $http is done, we register the http result into loginHandler, `data` parameter goes into loginService.loginHandler
                    httpPromise.success(function (data) {
                        self.loginHandler(data);
                        self.doneLoading = true;
                        // duplicated logic from $stateChangeStart, slightly different, now we surely have the userRole information.
                        if (pendingState.to.accessLevel === undefined || pendingState.to.accessLevel.bitMask & self.userRole.bitMask) {
                            checkUser.resolve();
                        } else {
                            checkUser.reject('unauthorized');
                        }
                    });

                    httpPromise.error(function (data, status) {
                        setUserRole(); //Set the user roles to public
                        checkUser.reject(status);
                    });

                    /**
                     * I set up the state change inside the promises success/error,
                     * so i can safely assign pendingStateChange back to null.
                     */
                    self.pendingStateChange = null;
                    return checkUser.promise;
                },
                /**
                 * Public properties
                 */
                userRole: null,
                user: {},
                isLogged: false,
                pendingStateChange: null,
                doneLoading: true
            };

            loadSavedData();
            managePermissions();

            return wrappedService;
        };
    }).factory('authInterceptor', function () {
        'use strict';

        return {
            request: function (config, loginService) {
                var userStr= localStorage.getItem('userData'), token;
                if (userStr) {
                   token = angular.fromJson(userStr).token;

                    if (token) {
                        config.headers.Authorization = 'Bearer ' + token;
                    }
                }
                //TODO should check for expired token???
                return config;
            }
        };
    });
