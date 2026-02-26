/**
 * Real-Time GPS Search Script
 * Handles geolocation, AJAX requests, and map rendering.
 */

let map;
let markers = [];
let userMarker;

document.addEventListener('DOMContentLoaded', function () {
    // Check if map container exists
    const mapContainer = document.getElementById('map-container');
    if (mapContainer) {
        initMap();
    }

    // Geolocation button handler
    const geoBtn = document.getElementById('get-location-btn');
    if (geoBtn) {
        geoBtn.addEventListener('click', detectLocation);
    }

    // Explicit Search button
    const searchBtn = document.getElementById('search-btn');
    if (searchBtn) {
        searchBtn.addEventListener('click', updateResults);
    }

    // Radius and Category change handlers
    const radiusInput = document.getElementById('radius-input');
    const categorySelect = document.getElementById('category-select');

    if (radiusInput) {
        radiusInput.addEventListener('input', () => {
            document.getElementById('radius-val').textContent = radiusInput.value;
        });
    }
});

function initMap() {
    // Initial view set to a general center (e.g., India)
    map = L.map('map-container').setView([20.5937, 78.9629], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

function detectLocation() {
    const statusText = document.getElementById('status-text');

    if (!navigator.geolocation) {
        showError("Geolocation is not supported by your browser.");
        return;
    }

    statusText.textContent = "🔍 Detecting your location...";

    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            document.getElementById('lat-input').value = lat;
            document.getElementById('lng-input').value = lng;

            statusText.textContent = `📍 Location detected: ${lat.toFixed(4)}, ${lng.toFixed(4)}. Now click 'Search Nearby' to see results!`;

            // Update map view
            map.setView([lat, lng], 13);

            // Add user marker
            if (userMarker) map.removeLayer(userMarker);
            userMarker = L.circleMarker([lat, lng], {
                radius: 10,
                fillColor: "#3b82f6",
                color: "#fff",
                weight: 2,
                opacity: 1,
                fillOpacity: 0.8
            }).addTo(map).bindPopup("You are here").openPopup();
        },
        (error) => {
            let errorMsg = "Unable to retrieve your location.";
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    errorMsg = "GPS Permission denied. Please enable location access in settings.";
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMsg = "Location information is unavailable.";
                    break;
                case error.TIMEOUT:
                    errorMsg = "The request to get user location timed out.";
                    break;
            }
            showError(errorMsg);
        }
    );
}

function updateResults() {
    const lat = document.getElementById('lat-input').value;
    const lng = document.getElementById('lng-input').value;
    const statusText = document.getElementById('status-text');

    if (!lat || !lng) {
        showError("Please click 'Detect My Location' first so we know where you are!");
        return;
    }

    statusText.textContent = "🔍 Searching nearby...";
    fetchNearbyPlaces(lat, lng);
}

async function fetchNearbyPlaces(lat, lng) {
    const radius = document.getElementById('radius-input').value || 2;
    const category = document.getElementById('category-select').value || 'ATTRACTION';
    const resultsContainer = document.getElementById('results-list');

    resultsContainer.innerHTML = '<div class="loader">Loading nearby places...</div>';
    clearMarkers();

    try {
        const response = await fetch(`/explorer/api/nearby-places/?lat=${lat}&lng=${lng}&radius=${radius}&category=${category}`);
        const data = await response.json();

        if (data.error) {
            showError(data.error);
            resultsContainer.innerHTML = '';
            return;
        }

        renderResults(data.results);

        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });

        document.getElementById('status-text').textContent = `✅ Found ${data.results.length} results!`;
    } catch (error) {
        showError("Failed to fetch data from server.");
        resultsContainer.innerHTML = '';
    }
}

function renderResults(results) {
    const container = document.getElementById('results-list');
    container.innerHTML = '';

    if (!results || results.length === 0) {
        container.innerHTML = '<div class="no-results">No places found in this radius. Try increasing the distance.</div>';
        return;
    }

    results.forEach(place => {
        // Create marker
        const marker = L.marker([place.lat, place.lng]).addTo(map);
        marker.bindPopup(`<strong>${place.name}</strong><br>${place.address}`);
        markers.push(marker);

        // Create list item
        const item = document.createElement('div');
        item.className = 'place-card glass';
        item.innerHTML = `
            <h3>${place.name}</h3>
            <p>📍 ${place.address}</p>
            ${place.rating ? `<p class="rating">⭐ ${place.rating}</p>` : ''}
            <div class="card-footer">
                <span class="source-badge">${place.source}</span>
                <a href="https://www.google.com/maps/dir/?api=1&destination=${place.lat},${place.lng}" target="_blank" class="nav-link">Navigate</a>
            </div>
        `;
        item.addEventListener('click', () => {
            map.setView([place.lat, place.lng], 15);
            marker.openPopup();
        });
        container.appendChild(item);
    });

    // Fit map to markers
    const group = new L.featureGroup([...markers, userMarker]);
    map.fitBounds(group.getBounds().pad(0.1));
}

function clearMarkers() {
    markers.forEach(m => map.removeLayer(m));
    markers = [];
}

function showError(msg) {
    const statusText = document.getElementById('status-text');
    statusText.innerHTML = `<span style="color: #ef4444;">❌ ${msg}</span>`;
    console.error(msg);
}
