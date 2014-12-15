/**=========================================================
 * Module: modals.js
 * Provides a simple way to implement bootstrap modals from templates
 =========================================================*/

App.controller('ModalGmapController', ['$scope', '$modal', 'gmap', function ($scope, $modal, gmap) {

  $scope.open = function (size) {

    var modalInstance = $modal.open({
      templateUrl: '/myModalContent.html',
      controller: ModalInstanceCtrl,
      size: size
    });
  };

  // Please note that $modalInstance represents a modal window (instance) dependency.
  // It is not the same as the $modal service used above.

  var ModalInstanceCtrl = function ($scope, $modalInstance) {

    $modalInstance.opened.then(function () {
      // When modal has been opened 
      // set to true the initialization param
      $scope.initGmap = true;

    });

    $scope.ok = function () {
      $modalInstance.close('closed');
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };

  };

}]);
