/**=========================================================
 * Module: gmap.js
 * Init Google Map plugin
 =========================================================*/

App.directive('gmap', ['$window','gmap', function($window, gmap){
  'use strict';

  // Map Style definition
  // Get more styles from http://snazzymaps.com/style/29/light-monochrome
  // - Just replace and assign to 'MapStyles' the new style array
  var MapStyles = [{featureType:'water',stylers:[{visibility:'on'},{color:'#bdd1f9'}]},{featureType:'all',elementType:'labels.text.fill',stylers:[{color:'#334165'}]},{featureType:'landscape',stylers:[{color:'#e9ebf1'}]},{featureType:'road.highway',elementType:'geometry',stylers:[{color:'#c5c6c6'}]},{featureType:'road.arterial',elementType:'geometry',stylers:[{color:'#fff'}]},{featureType:'road.local',elementType:'geometry',stylers:[{color:'#fff'}]},{featureType:'transit',elementType:'geometry',stylers:[{color:'#d8dbe0'}]},{featureType:'poi',elementType:'geometry',stylers:[{color:'#cfd5e0'}]},{featureType:'administrative',stylers:[{visibility:'on'},{lightness:33}]},{featureType:'poi.park',elementType:'labels',stylers:[{visibility:'on'},{lightness:20}]},{featureType:'road',stylers:[{color:'#d8dbe0',lightness:20}]}];
  
  gmap.setStyle( MapStyles );

  // Center Map marker on resolution change

  $($window).resize(function() {

    gmap.autocenter();

  });

  return {
    restrict: 'A',
    link: function (scope, element) {
      
      gmap.init(element);

    }
  };

}]);
