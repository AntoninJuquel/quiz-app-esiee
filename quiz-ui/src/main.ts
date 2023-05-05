import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

import { VSkeletonLoader } from 'vuetify/labs/VSkeletonLoader'

const vuetify = createVuetify({
  components: {
    ...components,
    VSkeletonLoader
  },
  directives,
  icons: {
    aliases,
    defaultSet: 'mdi',
    sets: {
      mdi
    }
  }
})

createApp(App).use(vuetify).use(router).mount('#app')
