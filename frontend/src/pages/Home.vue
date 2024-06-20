<template>
  <div class="relative">
    <login-modal v-if="isUserLoggedIn" />
    <sidebar />
    <div class="content" style="margin-left: 272px; margin-top:61px;"> <!-- Adjust margin to account for sidebar width -->
      <div id="map" class="map-container"></div>
    </div>
   
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import "leaflet/dist/leaflet.css";
import * as L from 'leaflet';
import sidebar from './Sidebar.vue';
import loginModal from './Login.vue';

const initialMap = ref(null);
const isUserLoggedIn = ref(false); // This should ideally be managed globally or via a store

onMounted(() => {
  console.log('Home component mounted');
  
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
.map-container {
  width: calc(100% - 5px); /* Adjust width to account for sidebar width */
  height: 100vh;
}

.sidebar {
  width: 64px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  z-index: 2;
}

.login-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  z-index: 3;
}
</style>
