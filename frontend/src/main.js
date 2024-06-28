import './index.css';

import { createApp } from 'vue';
import router from './router';
import App from './App.vue';
import { createPinia } from 'pinia';
import { Button, setConfig, frappeRequest, resourcesPlugin } from 'frappe-ui';

const app = createApp(App);
const pinia = createPinia();

setConfig('resourceFetcher', frappeRequest);

app.use(router);
app.use(pinia);
app.use(resourcesPlugin);

app.component('Button', Button);
app.mount('#app');
