/**=========================================================
 * Module: masked,js
 * Initializes the masked inputs
 =========================================================*/

App.directive('masked', function() {
  return {
    restrict: 'A',
    controller: function($scope, $element) {
      var $elem = $($element);
      if($.fn.inputmask)
        $elem.inputmask();
    }
  };
});
