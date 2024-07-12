
import API_KEY from '../../config/config.js';
function loadGoogleMapsAPI() {
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${API_KEY}`;
    script.defer = true;
    document.head.appendChild(script);
    script.onload = initMap;
}

function initMap() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;

            var map = new google.maps.Map(document.getElementById('map'), {
                center: {lat: latitude, lng: longitude},
                zoom: 15
            });

            var marker = new google.maps.Marker({
                position: {lat: latitude, lng: longitude},
                map: map
            });
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

window.onload = loadGoogleMapsAPI;
