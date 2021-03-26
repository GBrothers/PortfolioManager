<template>
  <v-card
    @click="switchTheme"
    class="d-flex elevation-0"
    :width="width"
    color="rgb(0,0,0,0)"
  >
    <div class="minitext">Theme</div>
    <v-spacer />
    <v-icon
      size="95%"
      :color="this.$vuetify.theme.dark ? 'blue darken-1' : 'yellow darken-3'"
    >
      {{ this.$vuetify.theme.dark ? "mdi-weather-night" : "mdi-weather-sunny" }}
    </v-icon>
  </v-card>
</template>

<script>
import colors from "@/colors.js"
export default {
  props: {
    width: String,
  },
  methods: {
    switchTheme() {
      colors.switchTheme()
    },
  },
}
</script>
