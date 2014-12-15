/**=========================================================
 * Module: access-login.js
 * Demo for login api
 =========================================================*/

App.controller('LoginFormController', ['$scope', '$http', '$state', function($scope, $http, $state) {

  // bind here all data from the form
  $scope.account = {};
  // place the message if something goes wrong
  $scope.authMsg = '';

  $scope.login = function() {
    $scope.authMsg = '';

    $http
      .post('api/account/login', {email: $scope.account.email, password: $scope.account.password})
      .then(function(response) {
        // assumes if ok, response is an object with some data, if not, a string with error
        // customize according to your api
        if ( !response.account ) {
          $scope.authMsg = 'Incorrect credentials.';
        }else{
          $state.go('app.dashboard');
        }
      }, function(x) {
        $scope.authMsg = 'Server Request Error';
      });
  };

}]);
