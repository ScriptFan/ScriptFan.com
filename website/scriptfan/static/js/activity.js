var xian = new google.maps.LatLng(34.198564,108.895614);
var map, marker, input_address, autocomplete, search;

function initialize() {
    // Initialize map instance
    var map_canvas = document.getElementById('map-canvas');
    var map_options = {
        zoom: 15,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        center: xian
    };
    map = new google.maps.Map(map_canvas, map_options);
 
    // Initialize autocomplete instance
    var ac_options = {
      bounds: map.getBounds()
      // types: ['establishment']
    };
    input_address = document.getElementById('address');
    autocomplete = new google.maps.places.Autocomplete(input_address, ac_options);
    autocomplete.bindTo('bounds', map);
    autocomplete.addListener('place_changed', place_changed);

    // Initialize marker instance
    marker = new google.maps.Marker({
        // map:map,
        draggable: true,
        animation: google.maps.Animation.DROP
        // position: xian
    });
    marker.addListener('dragend', marker_dragend);
    google.maps.event.addListener(marker, 'click', toggle_bounce);
}

function place_changed() {
    var position = autocomplete.getPlace().geometry.location;
    show_position(position);
    marker.setPosition(position);
    marker.setMap(map);
    // map.setCenter(position);
    map.panTo(position);
    return false;
}

function marker_dragend() {
    var position = marker.getPosition();
    show_position(position);
    // map.setCenter(position);
    map.panTo(position); // smoothly
}


function show_position(position) {
    $('#latitude').val(position.lat());
    $('#longitude').val(position.lng());
}

function toggle_bounce() {
    if (marker.getAnimation() != null) {
        marker.setAnimation(null);
    } else {
        marker.setAnimation(google.maps.Animation.BOUNCE);
    }
}

$(function() {
    initialize();
    // 阻止地址输入框回车时提交表单
    $('#address').keydown(function(event) {
        return event.keyCode != 13;
    });
});
