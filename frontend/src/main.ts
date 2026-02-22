import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

import App from '@/app/App.vue'
import { mealPlannerTheme } from '@/styles/theme'
import '@/styles/main.css'

const vuetify = createVuetify({
  theme: {
    defaultTheme: 'mealPlannerTheme',
    themes: {
      mealPlannerTheme
    }
  }
})

createApp(App).use(vuetify).mount('#app')
