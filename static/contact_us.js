    // Initialize and add the map
    function initMap() {
        const office_location = { lat: 49.20420226369159, lng: -123.1327178404073 };
        const map = new google.maps.Map(document.getElementById("google-map"), {
            zoom: 15,
            center: office_location,
        });
        const marker = new google.maps.Marker({
            position: office_location,
            map: map,
        });
    }

    document.addEventListener('DOMContentLoaded', e => {});
    