    var map;
    markers = [];
jsondata = [
{
  "type":"Centre, Accepts infants 6 weeks - 18 months",
  "name":"Regina Open Door Society Child Care Centre",
  "address":"1855 Smith Street, Regina, SK, S4P 2N5 (Downtown)",
  "phone":"306-545-3873",
  "lat":50.449499,
  "lng":-104.6148778
},
{
  "type":"Centre",
  "name":"YWCA Child Care Centre",
  "address":"1940 McIntyre Street, Regina, SK, S4P 2R3 (Downtown)",
  "phone":"306-525-2141",
  "lat":50.4480557,
  "lng":-104.6169768
}
]

    function centerAt(i) {
        console.log("trying to center at " + jsondata[i]);
            map.setCenter({ lat: jsondata["lat"], lng: jsondata["lng"] });
    }
    function setupSidebar() {
        myul = document.getElementById("myul");
        for(data in jsondata) {
            jsons = jsondata[data];
            console.log(jsons);
            console.log(jsons["name"]);
            const node = document.createElement("li");
            node.setAttribute("id", "list" + data);
            let testerino = function() { 
                                  
                clicker(jsons);
                                       };
            node.addEventListener("click", testerino);
            node.appendChild(document.createTextNode(jsons["type"]));
            node.appendChild(document.createElement("br"));
            node.appendChild(document.createTextNode(jsons["name"]));
            node.appendChild(document.createElement("br"));
            node.appendChild(document.createTextNode(jsons["address"]));
            node.appendChild(document.createElement("br"));
            node.appendChild(document.createTextNode(jsons["phone"]));
            myul.appendChild(node);
        }
    }

//        document.onmousedown = function (event) {
//          if (!event) {event = window.event;}
//          console.log("mousedown "+event.target, event);
//          // Post the event object here.
//        };
    
          function clicker(jsons) {

//                map.setZoom(13);
//                map.setCenter(this.getPosition());

            console.log(jsons);
            map.setCenter({ lat: jsons["lat"], lng: jsons["lng"] });
              for(var i = 0; i < jsondata.length; i++) {
                elem = document.getElementById("list" + i);
                  elem.style.background = "white";
              }
              elem = document.getElementById("list" + jsons["index"]);
              elem.scrollIntoView();
              elem.style.background = "lightblue";
          }
          function setDaycareMarkers(map) {
    // Adds markers to the map.
    // Marker sizes are expressed as a Size of X,Y where the origin of the image
    // (0,0) is located in the top left of the image.
    // Origins, anchor positions and coordinates of the marker increase in the X
    // direction to the right and in the Y direction down.
    const image = {
      url: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
      // This marker is 20 pixels wide by 32 pixels high.
      size: new google.maps.Size(20, 32),
      // The origin for this image is (0, 0).
      origin: new google.maps.Point(0, 0),
      // The anchor for this image is the base of the flagpole at (0, 32).
      anchor: new google.maps.Point(0, 32),
    };
    // Shapes define the clickable region of the icon. The type defines an HTML
    // <area> element 'poly' which traces out a polygon as a series of X,Y points.
    // The final coordinate closes the poly by connecting to the first coordinate.
    const shape = {
      coords: [1, 1, 1, 20, 18, 20, 18, 1],
      type: "poly",
    };

    for (let i = 0; i < jsondata.length; i++) {
        jsondata[i]["index"] = i;
      const data = jsondata[i];

      marker = new google.maps.Marker({
        position: { lat: data["lat"], lng: data["lng"] },
        map,
        title: data["name"],
        zIndex: i + 1,
      });
        
        marker.addListener("click", () => {
            clicker(data);
        });
        
        markers[i] = marker;
    }
  }

  function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 15,
      center: { lat: 50.4452, lng: -104.6189 },
    });
    
    var marker = new google.maps.Marker({
      position: { lat: 50.4452, lng: -104.6189 },
      map: map,
      icon: 'http://maps.google.com/mapfiles/ms/icons/orange-dot.png'
    });
    
    var searchBox = new google.maps.places.SearchBox(document.getElementById('search'));
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(document.getElementById('search'));
    
    //map.addListener('bounds_changed', function() {
    //  searchBox.setBounds(map.getBounds());
    //});
    
    searchBox.addListener('places_changed', function() {
      var places = searchBox.getPlaces();
      
      if (places.length == 0) {
        return;
      }
      
      var bounds = new google.maps.LatLngBounds();
      places.forEach(function(place) {
        if (!place.geometry) {
          console.log("Returned place contains no geometry");
          return;
        }
        
        if (place.geometry.viewport) {
          bounds.union(place.geometry.viewport);
        } else {
          bounds.extend(place.geometry.location);
        }
      });
      
      map.fitBounds(bounds);
    });
    
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        
        marker.setPosition(pos);
        map.setCenter(pos);
      }, function() {
        handleLocationError(true, marker, map.getCenter());
      });
    } else {
      handleLocationError(false, marker, map.getCenter());
    }
      
      setDaycareMarkers(map);
  }
  
  function handleLocationError(browserHasGeolocation, marker, pos) {
    var infoWindow = new google.maps.InfoWindow({
      map: map
    });
    
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
  }
    function initAll(){
        setupSidebar();
        initMap();
    }

console.log("map.js loaded")
