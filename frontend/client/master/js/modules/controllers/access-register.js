/**=========================================================
 * Module: access-register.js
 * Demo for register account api
 =========================================================*/

App.controller('RegisterFormController', ['$scope', '$http', '$state', function($scope, $http, $state) {

  // bind here all data from the form
  $scope.account = {};
  // place the message if something goes wrong
  $scope.authMsg = '';
    
  $scope.register = function() {
    $scope.authMsg = '';

    $http
      .post('api/account/register', {email: $scope.account.email, password: $scope.account.password})
      .then(function(response) {
        // assumes if ok, response is an object with some data, if not, a string with error
        // customize according to your api
        if ( !response.account ) {
          $scope.authMsg = response;
        }else{
          $state.go('app.dashboard');
        }
      }, function(x) {
        $scope.authMsg = 'Server Request Error';
      });
  };

}]);
