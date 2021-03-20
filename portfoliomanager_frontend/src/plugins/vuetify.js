import Vue from "vue"
import Vuetify from "vuetify/lib/framework"

// eslint-disable-next-line no-unused-vars
import colors from "vuetify/lib/util/colors"

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: "#9c2740",
        secondary: "#673ab7",
        accent: "#e91e63",
        error: "#f44336",
        warning: "#cddc39",
        info: "#00bcd4",
        success: "#4caf50",
      },
      dark: {
        primary: "#9c27b0",
        secondary: "#673ab7",
        accent: "#e91e63",
        error: "#f44336",
        warning: "#cddc39",
        info: "#00bcd4",
        success: "#4caf50",
      },
    },
  },
})
