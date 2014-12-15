/**=========================================================
 * Module panel-tools.js
 * Directive tools to control panels. 
 * Allows collapse, refresh and dismiss (remove)
 * Saves panel state in browser storage
 =========================================================*/

App.directive('paneltool', function(){
  var templates = {
    /* jshint multistr: true */
    collapse:"<a href='#' panel-collapse='' data-toggle='tooltip' title='Collapse Panel' ng-click='{{panelId}} = !{{panelId}}' ng-init='{{panelId}}=false'> \
                <em ng-show='{{panelId}}' class='fa fa-plus'></em> \
                <em ng-show='!{{panelId}}' class='fa fa-minus'></em> \
              </a>",
    dismiss: "<a href='#' panel-dismiss='' data-toggle='tooltip' title='Close Panel'>\
               <em class='fa fa-times'></em>\
             </a>",
    refresh: "<a href='#' panel-refresh='' data-toggle='tooltip' data-spinner='{{spinner}}' title='Refresh Panel'>\
               <em class='fa fa-refresh'></em>\
             </a>"
  };
  
  return {
    restrict: 'E',
    template: function( elem, attrs ){
      var temp = '';
      if(attrs.toolCollapse)
        temp += templates.collapse.replace(/{{panelId}}/g, (elem.parent().parent().attr('id')) );
      if(attrs.toolDismiss)
        temp += templates.dismiss;
      if(attrs.toolRefresh)
        temp += templates.refresh.replace(/{{spinner}}/g, attrs.toolRefresh);
      return temp;
    },
    // scope: true,
    // transclude: true,
    link: function (scope, element, attrs) {
      element.addClass('pull-right');
    }
  };
})
/**=========================================================
 * Dismiss panels * [panel-dismiss]
 =========================================================*/
.directive('panelDismiss', function(){
  'use strict';
  return {
    restrict: 'A',
    controller: function ($scope, $element) {
      var removeEvent   = 'panel-remove',
          removedEvent  = 'panel-removed';

      $element.on('click', function () {

        // find the first parent panel
        var parent = $(this).closest('.panel');

        if($.support.animation) {
          parent.animo({animation: 'bounceOut'}, removeElement);
        }
        else removeElement();

        function removeElement() {
          // Trigger the event and finally remove the element
          $.when(parent.trigger(removeEvent, [parent]))
           .done(destroyPanel);
        }

        function destroyPanel() {
          var col = parent.parent();
          parent.remove();
          // remove the parent if it is a row and is empty and not a sortable (portlet)
          col
            .trigger(removedEvent) // An event to catch when the panel has been removed from DOM
            .filter(function() {
            var el = $(this);
            return (el.is('[class*="col-"]:not(.sortable)') && el.children('*').length === 0);
          }).remove();

        }
      });
    }
  };
})
/**=========================================================
 * Collapse panels * [panel-collapse]
 =========================================================*/
.directive('panelCollapse', ['$timeout', function($timeout){
  'use strict';
  
  var storageKeyName = 'panelState',
      storage;
  
  return {
    restrict: 'A',
    // transclude: true,
    controller: function ($scope, $element) {

      // Prepare the panel to be collapsible
      var $elem   = $($element),
          parent  = $elem.closest('.panel'), // find the first parent panel
          panelId = parent.attr('id');

      storage = $scope.$storage;

      // Load the saved state if exists
      var currentState = loadPanelState( panelId );
      if ( typeof currentState !== undefined) {
        $timeout(function(){
            $scope[panelId] = currentState; },
          10);
      }

      // bind events to switch icons
      $element.bind('click', function() {

        savePanelState( panelId, !$scope[panelId] );

      });
    }
  };

  function savePanelState(id, state) {
    if(!id) return false;
    var data = angular.fromJson(storage[storageKeyName]);
    if(!data) { data = {}; }
    data[id] = state;
    storage[storageKeyName] = angular.toJson(data);
  }

  function loadPanelState(id) {
    if(!id) return false;
    var data = angular.fromJson(storage[storageKeyName]);
    if(data) {
      return data[id];
    }
  }

}])
/**=========================================================
 * Refresh panels
 * [panel-refresh] * [data-spinner="standard"]
 =========================================================*/
.directive('panelRefresh', function(){
  'use strict';
  
  return {
    restrict: 'A',
    controller: function ($scope, $element) {
      
      var refreshEvent   = 'panel-refresh',
          csspinnerClass = 'csspinner',
          defaultSpinner = 'standard';

      // method to clear the spinner when done
      function removeSpinner() {
        this.removeClass(csspinnerClass);
      }

      // catch clicks to toggle panel refresh
      $element.on('click', function () {
        var $this   = $(this),
            panel   = $this.parents('.panel').eq(0),
            spinner = $this.data('spinner') || defaultSpinner
            ;

        // start showing the spinner
        panel.addClass(csspinnerClass + ' ' + spinner);

        // attach as public method
        panel.removeSpinner = removeSpinner;

        // Trigger the event and send the panel object
        $this.trigger(refreshEvent, [panel]);

      });

    }
  };
});


  /**
   * This function is only to show a demonstration
   * of how to use the panel refresh system via 
   * custom event. 
   * IMPORTANT: see how to remove the spinner.
   */
(function($, window, document){
  'use strict';

  $(document).on('panel-refresh', '.panel.panel-demo', function(e, panel){
    
    // perform any action when a .panel triggers a the refresh event
    setTimeout(function(){
      // when the action is done, just remove the spinner class
      panel.removeSpinner();
    }, 3000);

  });

}(jQuery, window, document));
