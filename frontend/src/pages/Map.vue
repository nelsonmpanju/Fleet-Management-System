<template>
  <div>
    <h3>An interactive leaflet map</h3>
    <div id="map" style="height:100vh;"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import "leaflet/dist/leaflet.css";
import * as L from 'leaflet';

const initialMap = ref(null);

onMounted(() => {
  console.log('Map component mounted');
  
  // Check if the map container exists
  const mapContainer = document.getElementById('map');
  if (!mapContainer) {
    console.error('Map container not found');
    return;
  }

  console.log('Map container found');
  
  initialMap.value = L.map('map').setView([23.8041, 90.4152], 6);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
  }).addTo(initialMap.value);

  // Check if the map instance is created successfully
  if (!initialMap.value) {
    console.error('Map initialization failed');
  } else {
    console.log('Map initialized successfully');
  }
});
</script>

<style scoped>
#map {
  width: 100%;
  height: 100vh;
}
</style>
