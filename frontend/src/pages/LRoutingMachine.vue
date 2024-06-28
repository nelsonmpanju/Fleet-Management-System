<template>
  <div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import L from 'leaflet';
import { IRouter, IGeocoder, LineOptions } from 'leaflet-routing-machine';

const props = defineProps({
  mapObject: {
    type: Object,
  },
  visible: {
    type: Boolean,
    default: true,
  },
  waypoints: {
    type: Array,
    required: true,
  },
  router: {
    type: IRouter,
  },
  plan: {
    type: L.Routing.Plan,
  },
  geocoder: {
    type: IGeocoder,
  },
  fitSelectedRoutes: {
    type: [String, Boolean],
    default: "smart",
  },
  lineOptions: {
    type: LineOptions,
  },
  routeLine: {
    type: Function,
  },
  autoRoute: {
    type: Boolean,
    default: true,
  },
  routeWhileDragging: {
    type: Boolean,
    default: false,
  },
  routeDragInterval: {
    type: Number,
    default: 500,
  },
  waypointMode: {
    type: String,
    default: "connect",
  },
  useZoomParameter: {
    type: Boolean,
    default: false,
  },
  showAlternatives: {
    type: Boolean,
    default: false,
  },
  altLineOptions: {
    type: LineOptions,
  },
});

const ready = ref(false);
const map = ref(null);
const layer = ref(null);

const add = () => {
  if (!props.mapObject) return;

  const {
    waypoints,
    fitSelectedRoutes,
    autoRoute,
    routeWhileDragging,
    routeDragInterval,
    waypointMode,
    useZoomParameter,
    showAlternatives,
    lineOptions,
    routeLine,
  } = props;

  const options = {
    waypoints,
    fitSelectedRoutes,
    autoRoute,
    routeWhileDragging,
    routeDragInterval,
    waypointMode,
    useZoomParameter,
    showAlternatives,
  };

  const routingLayer = L.Routing.control(options);
  routingLayer.addTo(props.mapObject);
  layer.value = routingLayer;
  ready.value = true;
};

const customRouteLine = (route, options) => {
  const half = Math.ceil(route.coordinates.length / 2);
  const part1 = L.polyline(route.coordinates.slice(0, half), { color: 'blue', weight: 4 });
  const part2 = L.polyline(route.coordinates.slice(half), { color: 'red', weight: 4 });
  return L.layerGroup([part1, part2]);
};

const customMarker = (i, wp, nWps) => {
  return L.marker(wp.latLng, {
    draggable: true,
    icon: L.icon({
      iconUrl: 'https://static.vecteezy.com/system/resources/previews/000/643/001/original/map-pointer-car-truck-icon-vector.jpg',
      iconSize: [50, 50],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    })
  }).bindPopup(`Waypoint ${i + 1}`);
};

const customSummaryTemplate = (summary) => {
  return `<div class="custom-summary">
            <h3>Route Summary</h3>
            <p>Total distance: ${summary.totalDistance} km</p>
            <p>Estimated time: ${summary.totalTime}</p>
          </div>`;
};

const customInstructionsTemplate = (instructions) => {
  let html = '<ol class="custom-instructions">';
  instructions.forEach(instruction => {
    html += `<li>${instruction.text} (${instruction.distance} m)</li>`;
  });
  html += '</ol>';
  return html;
};

watch(() => props.mapObject, (newValue) => {
  if (newValue) add();
});

onMounted(() => {
  add();
});

onBeforeUnmount(() => {
  if (layer.value) {
    layer.value.remove();
  }
});
</script>

<style scoped>
.custom-summary {
  background-color: white;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
}

.custom-instructions {
  background-color: white;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
}

.custom-instructions li {
  margin-bottom: 5px;
}
</style>
