import Vue from "vue"
import Vuetify from "vuetify/lib/framework"

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    dark: true,
    themes: {
      light: {
        primary: "#f5e8ff",
        secondary: "#673ab7",
        accent: "#e91e63",
        error: "#f44336",
        warning: "#cddc39",
        info: "#00bcd4",
        success: "#4caf50",

        // custom properties
        background: "red",
        gradientbegin: "#e7cfff",
        gradientend: "#f5ebff",
        gradientbeginfundamental: "#fffeb9",
        h1: "#6600cc",
      },
      dark: {
        primary: "#303050",
        secondary: "#673007",
        accent: "#e91e63",
        error: "#f44336",
        warning: "#cddc39",
        info: "#00bcd4",
        success: "#4caf50",

        // custom properties
        background: "purple",
        gradientbegin: "#1a1a2d",
        gradientend: "#303050",
        gradientbeginfundamental: "#444303",
        h1: "#bfbfd9",
      },
    },
  },
})
