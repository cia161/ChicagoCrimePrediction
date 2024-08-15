import API_KEY from './config.js';

function loadGoogleMapsAPI() {
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${API_KEY}&libraries=places`;
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

            var geocoder = new google.maps.Geocoder();
            var latlng = {lat: latitude, lng: longitude};
            geocoder.geocode({'location': latlng}, function (results, status) {
                if (status === 'OK') {
                    if (results[0]) {
                        var address = results[0].formatted_address;
                        document.getElementById('address').textContent = address;
                        
                        // Check if the location is in Chicago
                        var inChicago = false;
                        for (var i = 0; i < results[0].address_components.length; i++) {
                            if (results[0].address_components[i].types.includes("locality") &&
                                results[0].address_components[i].long_name === "Chicago") {
                                inChicago = true;
                                break;
                            }
                        }
                        
                        if (inChicago) {
                            // Fetch crime predictions for the user's location
                            fetchPredictions(latitude, longitude);
                        } else {
                            // Show a notification and update results
                            alert("You are not in Chicago!");
                            document.getElementById('results').innerHTML = '<h2>No probabilities available for your location</h2>';
                        }
                    } else {
                        document.getElementById('address').textContent = 'No results found';
                    }
                } else {
                    document.getElementById('address').textContent = 'Geocoder failed due to: ' + status;
                }
            });
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

// Function to fetch crime predictions from the server
function fetchPredictions(lat, lon) {
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ latitude: lat, longitude: lon })
    })
    .then(response => response.json())
    .then(data => {
        let predictionList = document.getElementById('predicted-crimes');
        
        // Clear the existing list items
        predictionList.innerHTML = '';

        // Add new list items for each predicted crime
        data.forEach(crime => {
            let listItem = document.createElement('li');
            listItem.textContent = `${crime[0].toLowerCase().replace(/\b\w/g, c => c.toUpperCase())}: ${crime[1].toFixed(2)}`;
            predictionList.appendChild(listItem);
        });
    })
    .catch(error => {
        console.error('Error fetching predictions:', error);
    });
}

// Load Google Maps API and initialize the map
window.onload = loadGoogleMapsAPI;
