import { defineStore } from 'pinia';

// Authentication Store
export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
  }),
  actions: {
    login(email, password) {
      if (email === 'user@example.com' && password === 'password') {
        this.isLoggedIn = true;
        localStorage.setItem('isLoggedIn', 'true');
      } else {
        throw new Error('Invalid credentials');
      }
    },
    logout() {
      this.isLoggedIn = false;
      localStorage.removeItem('isLoggedIn');
    },
    checkLogin() {
      this.isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    },
  },
});

// Sidebar Store
export const useSidebarStore = defineStore('sidebar', {
  state: () => ({
    isOpen: true,
    searchQuery: '',
  }),
  actions: {
    toggleSidebar() {
      this.isOpen = !this.isOpen;
    },
    setSearchQuery(query) {
      this.searchQuery = query;
    },
  },
});

// Routing Store
export const useRoutingStore = defineStore('routing', {
  state: () => ({
    waypoints: [],
    fitSelectedRoutes: 'smart',
    autoRoute: true,
    routeWhileDragging: false,
    routeDragInterval: 500,
    waypointMode: 'connect',
    useZoomParameter: false,
    showAlternatives: false,
    lineOptions: {},
    routingLayer: null,
    mapObject: null,
  }),
  actions: {
    setWaypoints(waypoints) {
      this.waypoints = waypoints;
    },
    setMapObject(mapObject) {
      this.mapObject = mapObject;
    },
    setRoutingLayer(layer) {
      this.routingLayer = layer;
    },
    clearRoutingLayer() {
      if (this.routingLayer) {
        this.routingLayer.remove();
        this.routingLayer = null;
      }
    },
  },
});
