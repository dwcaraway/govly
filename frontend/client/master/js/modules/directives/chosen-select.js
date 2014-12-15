/**=========================================================
 * Module: chosen-select.js
 * Initializes the chose select plugin
 =========================================================*/

App.directive('chosen', function() {
  return {
    restrict: 'A',
    link: function(scope, element, attr) {

      // update the select when data is loaded
      scope.$watch(attr.chosen, function(oldVal, newVal) {
          element.trigger('chosen:updated');
      });

      // update the select when the model changes
      scope.$watch(attr.ngModel, function() {
          element.trigger('chosen:updated');
      });

      if($.fn.chosen)
        element.chosen();
    }
  };
});