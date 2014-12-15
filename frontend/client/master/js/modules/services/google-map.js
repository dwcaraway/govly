/**=========================================================
 * Module: google-map.js
 * Services to share gmap functions
 =========================================================*/

App.service('gmap', function() {

  return {
    setStyle: function(style) {
      this.MapStyles = style;
    },
    autocenter: function() {
      var refs = this.gMapRefs;
      if(refs && refs.length) {
        for( var r in refs) {
          var mapRef = refs[r];
          var currMapCenter = mapRef.getCenter();
          if(mapRef && currMapCenter) {
              google.maps.event.trigger(mapRef, 'resize');
              mapRef.setCenter(currMapCenter);
          }
        }
      }
    },
    init: function (element) { //initGmap

      var self      = this,
          $element  = $(element),
          addresses = $element.data('address') && $element.data('address').split(';'),
          titles    = $element.data('title') && $element.data('title').split(';'),
          zoom      = $element.data('zoom') || 14,
          maptype   = $element.data('maptype') || 'ROADMAP', // or 'TERRAIN'
          markers   = [];

      if(addresses) {
        for(var a in addresses)  {
            if(typeof addresses[a] == 'string') {
                markers.push({
                    address:  addresses[a],
                    html:     (titles && titles[a]) || '',
                    popup:    true   /* Always popup */
                  });
            }
        }

        var options = {
            controls: {
                   panControl:         true,
                   zoomControl:        true,
                   mapTypeControl:     true,
                   scaleControl:       true,
                   streetViewControl:  true,
                   overviewMapControl: true
               },
            scrollwheel: false,
            maptype: maptype,
            markers: markers,
            zoom: zoom
            // More options https://github.com/marioestrada/jQuery-gMap
        };

        var gMap = $element.gMap(options);

        var ref = gMap.data('gMap.reference');
        // save in the map references list
        if( ! self.gMapRefs )
          self.gMapRefs = [];
        self.gMapRefs.push(ref);

        // set the styles
        if($element.data('styled') !== undefined) {
          
          ref.setOptions({
            styles: self.MapStyles
          });

        }
      }
    }
  };
});