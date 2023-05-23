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

// Emoji picker
import 'vue3-emoji-picker/css'

// Custom dark theme
import customDarkTheme from './themes/darkTheme'

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
  },
  theme: {
    defaultTheme: 'customDarkTheme',
    themes: {
      customDarkTheme
    }
  }
})

createApp(App).use(vuetify).use(router).mount('#app')
