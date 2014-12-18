var sbhub = angular.module('sbhub', ['ngResource', 'ui.bootstrap']);

sbhub.controller('oppsCtrl', function ($scope, $http, $resource, $timeout){
    $http.defaults.useXDomain = true;
    var Opp = $resource('http://api.data.gov/gsa/fbopen/v0/opps', {'api_key': '8l3xbEmsQMq7AG7mXoSy3IuJAqehmWGRC754Otx7'});
    $scope.currentPage = 1;

    $scope.getOpps = function(filter){
        $scope.filter = filter || {};
        Opp.get($scope.filter, function(data){
            $scope.opps = data;
            $timeout(function(){
                $scope.$broadcast('dataloaded');
            }, 0, false);
        }, function(data, status){
            console.log('Request failed:'+status);
        });
    };

  $scope.pageChanged = function() {
    console.log("page: "+$scope.currentPage);
    $scope.filter = $scope.filter || {};
    $scope.filter['start'] = 10 * ($scope.currentPage-1);
    console.log('start: '+$scope.filter.start);
    $scope.getOpps($scope.filter);
  };

  $scope.filterChanged = function(filter){
    console.log("page: "+$scope.currentPage);
    $scope.currentPage = 1;
    $scope.filter = $scope.filter || {};
    $scope.filter['start'] = 0;
    $scope.getOpps($scope.filter); 
  };


  //On page load, get opportunities with no filtering.
  $scope.getOpps();

});

// apply jquery shorten to all div children with class shorten
sbhub.directive('shorten', ['$timeout', function ($timeout) {
    return {
        link: function ($scope, element, attrs) {
            $scope.$on('dataloaded', function () {
                    $timeout(function () { // You might need this timeout to be sure its run after DOM render
                        $('div.shorten').shorten({
                            "showChars":255}); 
                        }, 0, false);
                })
        }
    };
}]);
