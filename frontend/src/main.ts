import { createApp } from "vue";
import { createVuetify } from "vuetify";
import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";

import App from "@/app/App.vue";
import router from "@/router";
import { dark, light } from "@/styles/theme";
import "@/styles/main.css";

const vuetify = createVuetify({
  theme: {
    defaultTheme: "dark",
    themes: {
      dark,
      light
    }
  },
  defaults: {
    VCard: {
      elevation: 0,
      rounded: "lg"
    },
    VTextField: {
      variant: "outlined",
      density: "comfortable"
    },
    VTextarea: {
      variant: "outlined",
      density: "comfortable"
    }
  }
});

const app = createApp(App);

app.use(vuetify);
app.use(router);
app.mount("#app");
