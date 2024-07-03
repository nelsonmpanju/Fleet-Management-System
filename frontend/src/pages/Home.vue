<template>
  <nav class="fixed top-0 z-50 w-full bg-white border-b border-gray-200" style="height: 56px;">
    <div class="px-3 py-3 lg:px-5 lg:pl-3">
      <div class="flex items-center justify-between">
        <div class="flex items-center justify-start rtl:justify-end">
          <button @click="toggleSidebar" aria-controls="logo-sidebar" type="button" class="inline-flex items-center p-2 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200">
            <span class="sr-only">Open sidebar</span>
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z" clip-rule="evenodd"></path>
            </svg>
          </button>
          <a href="#" class="flex ms-2 md:me-24">
            <img src="https://i.pinimg.com/originals/13/8b/9b/138b9b22dbc85be57c3898716fcdfd4c.jpg" class="h-11 me-2" alt="Logo">
            <span class="self-center text-xl font-semibold whitespace-nowrap">Fleet Map</span>
          </a>
        </div>
        <div class="flex items-center ms-3">
          <button type="button" class="flex text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300">
            <span class="sr-only">Open user menu</span>
            <img class="w-8 h-8 rounded-full" src="https://static-00.iconduck.com/assets.00/user-icon-2048x2048-ihoxz4vq.png" alt="User photo">
          </button>
        </div>
      </div>
    </div>
  </nav>
  <Sidebar />
    <div class="map-container">
      <div id="map" class="map"></div>
      <LRoutingMachine :mapObject="mapObject" :waypoints="waypoints" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import LRoutingMachine from "./LRoutingMachine.vue";
import 'leaflet/dist/leaflet.css';
import * as L from 'leaflet';
import Sidebar from './Sidebar.vue';
import { useSidebarStore } from '@/store';

const sidebarStore = useSidebarStore();

const mapObject = ref(null);
const waypoints = ref([
  { lat: 50.7436056, lng: -9.2304153 },
  { lat: 38.7436056, lng: -0.131281 },
]);

const toggleSidebar = () => {
  sidebarStore.toggleSidebar();
};

onMounted(() => {
  mapObject.value = L.map('map').setView([38.7436056, -2.2304153], 6);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
  }).addTo(mapObject.value);
});
</script>

<style scoped>
.sidebar {
  width: 450px;
}
.flex {
  display: flex;
}
.map-container {
  flex-grow: 1;
  position: sticky;
}
.map {
  width: 100%;
  height: calc(100vh - 56px);
  position: absolute;
  top: 0;
  bottom: 0;
}
</style>