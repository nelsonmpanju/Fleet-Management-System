import './index.css'

import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import VueSidebarMenu from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import { Button, setConfig, frappeRequest, resourcesPlugin } from 'frappe-ui'

let app = createApp(App)

setConfig('resourceFetcher', frappeRequest)

const vuetify = createVuetify({
  components,
  directives
})

app.use(router)
app.use(resourcesPlugin)
app.use(vuetify)
app.component('Button', Button)
app.use(VueSidebarMenu)
app.mount('#app')

