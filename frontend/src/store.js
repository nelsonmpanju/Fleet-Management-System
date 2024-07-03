import { defineStore } from 'pinia';
import router from '@/router';
import { computed, reactive } from 'vue';
import { createResource } from 'frappe-ui';

// Helper function to get session user
function sessionUser() {
  const cookies = new URLSearchParams(document.cookie.split('; ').join('&'));
  let _sessionUser = cookies.get('user_id');
  if (_sessionUser === 'Guest') {
    _sessionUser = null;
  }
  return _sessionUser;
}

// Define the user resource for API interaction
export const userResource = createResource({
  url: 'frappe.auth.get_logged_user',
  cache: 'User',
  onError(error) {
    if (error && error.exc_type === 'AuthenticationError') {
      router.push({ name: 'Login' });
    }
  },
});

// Define the session state and actions
export const session = reactive({
  login: createResource({
    url: 'login',
    makeParams({ email, password }) {
      return {
        usr: email,
        pwd: password,
      };
    },
    onSuccess(data) {
      userResource.reload();
      session.user = sessionUser();
      session.login.reset();
      router.replace(data.default_route || '/');
    },
  }),
  logout: createResource({
    url: 'logout',
    onSuccess() {
      userResource.reset();
      session.user = sessionUser();
      router.replace({ name: 'Login' });
    },
  }),
  user: sessionUser(),
  isLoggedIn: computed(() => !!session.user),
});

// Authentication Store
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: session.user,
    isLoggedIn: computed(() => !!session.user),
  }),
  actions: {
    async login(email, password) {
      try {
        await session.login.run({ email, password });
      } catch (error) {
        throw new Error('Invalid credentials');
      }
    },
    async logout() {
      await session.logout.run();
    },
    checkLogin() {
      this.user = session.user;
      this.isLoggedIn = session.isLoggedIn;
    },
  },
});

// Sidebar Store
export const useSidebarStore = defineStore('sidebar', {
  state: () => ({
    isOpen: true,
    currentTab: null,
    searchQuery: '',
    docTypes: [],
  }),
  actions: {
    toggleSidebar(tab) {
      if (this.currentTab === tab) {
        this.isOpen = !this.isOpen;
      } else {
        this.currentTab = tab;
        this.isOpen = true;
      }
    },
    setSearchQuery(query) {
      this.searchQuery = query;
    },
    setDocTypes(docTypes) {
      this.docTypes = docTypes;
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
