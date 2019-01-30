var map;

    function getJSON() {
        $(document).ready(function() {
            $("button").click(function() {
                $.getJSON("http://publish.twitter.com/oembed?format=json&url=https://twitter.com/andypiper/status/807811447862468608", function(result) {
                    $.each(result, function(i, field) {
                        $("div").append(field + " ");
                    });
                });
            });
        });
    }

    function initMap() {
        definePopupClass();
        //Random number generator based on array length
        // // var rand = Math.floor(Math.random() * myArray.length);
        var text = '{ "employees" : [' +
            '{ "firstName":"John" , "lastName":"Doe" },' +
            '{ "firstName":"Anna" , "lastName":"Smith" },' +
            '{ "firstName":"Peter" , "lastName":"Jones" } ]}';
        var obj = JSON.parse(text);

        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 4,
            center: {
                lat: -33.865427,
                lng: 151.196123
            },
            mapTypeId: 'terrain'
        });

        //shows fusiontable thingo
        /* var layer = new google.maps.FusionTablesLayer({
             query: {
                 select: 'location',
                 from: '1xWyeuAhIFK_aED1ikkQEGmR8mINSCJO9Vq-BPQ'
             },
             heatmap: {
                 enabled: true
             }
         });
         */

        popup = new Popup(
            new google.maps.LatLng(-33.866, 151.196),
            document.getElementById('content'));
        popup.setMap(map);
        popup = new Popup(
            new google.maps.LatLng(-33.866, 111.196),
            document.getElementById('content2'));
        popup.setMap(map);

        // Create a <script> tag and set the USGS URL as the source.
        var script = document.createElement('script');

        // This example uses a local copy of the GeoJSON stored at
        // http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp
        script.src = 'https://developers.google.com/maps/documentation/javascript/examples/json/earthquake_GeoJSONP.js';
        document.getElementsByTagName('head')[0].appendChild(script);
    }

    function eqfeed_callback(results) {
        var heatmapData = [];
        for (var i = 0; i < results.features.length; i++) {
            var coords = results.features[i].geometry.coordinates;
            var latLng = new google.maps.LatLng(coords[1], coords[0]);
            heatmapData.push(latLng);
        }
        var heatmap = new google.maps.visualization.HeatmapLayer({
            data: heatmapData,
            dissipating: false,
            map: map
        });
    }

    //    http://publish.twitter.com/oembed?format=json&url=https://twitter.com/andypiper/status/807811447862468608
    /** Defines the Popup class. */
    function definePopupClass() {
        /**
         * A customized popup on the map.
         * @param {!google.maps.LatLng} position
         * @param {!Element} content
         * @constructor
         * @extends {google.maps.OverlayView}
         */
        Popup = function(position, content) {
            this.position = position;

            content.classList.add('popup-bubble-content');

            var pixelOffset = document.createElement('div');
            pixelOffset.classList.add('popup-bubble-anchor');
            pixelOffset.appendChild(content);

            this.anchor = document.createElement('div');
            this.anchor.classList.add('popup-tip-anchor');
            this.anchor.appendChild(pixelOffset);

            // Optionally stop clicks, etc., from bubbling up to the map.
            this.stopEventPropagation();
        };
        // NOTE: google.maps.OverlayView is only defined once the Maps API has
        // loaded. That is why Popup is defined inside initMap().
        Popup.prototype = Object.create(google.maps.OverlayView.prototype);

        /** Called when the popup is added to the map. */
        Popup.prototype.onAdd = function() {
            this.getPanes().floatPane.appendChild(this.anchor);
        };

        /** Called when the popup is removed from the map. */
        Popup.prototype.onRemove = function() {
            if (this.anchor.parentElement) {
                this.anchor.parentElement.removeChild(this.anchor);
            }
        };

        /** Called when the popup needs to draw itself. */
        Popup.prototype.draw = function() {
            var divPosition = this.getProjection().fromLatLngToDivPixel(this.position);
            // Hide the popup when it is far out of view.
            var display =
                Math.abs(divPosition.x) < 4000 && Math.abs(divPosition.y) < 4000 ?
                'block' :
                'none';

            if (display === 'block') {
                this.anchor.style.left = divPosition.x + 'px';
                this.anchor.style.top = divPosition.y + 'px';
            }
            if (this.anchor.style.display !== display) {
                this.anchor.style.display = display;
            }
        };

        /** Stops clicks/drags from bubbling up to the map. */
        Popup.prototype.stopEventPropagation = function() {
            var anchor = this.anchor;
            anchor.style.cursor = 'auto';

            ['click', 'dblclick', 'contextmenu', 'wheel', 'mousedown', 'touchstart',
                'pointerdown'
            ]
            .forEach(function(event) {
                anchor.addEventListener(event, function(e) {
                    e.stopPropagation();
                });
            });
        };
    }
