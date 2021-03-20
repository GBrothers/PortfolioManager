<template>
  <v-main>
    <v-app-bar color="primary" dense dark height="70px">
      <v-row justify="center">
        <v-btn
          @click="
            {
              showLookup = true
            }
          "
          >Search Company</v-btn
        >
        <v-switch label="label" @change="switchTheme" />
        <InternalStatus />
      </v-row>
    </v-app-bar>
    <TickerLookup
      :show-dialog="showLookup"
      @tickerChange="tickerChange"
      @noTickerChange="noTickerChange"
    />

    <!-- Snackbar for selected Item -->
    <v-snackbar v-model="snackbar" timeout="3000">
      {{ ticker }}
      <template #action="{ attrs }">
        <v-btn color="green" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-main>
</template>

<script>
import TickerLookup from "@/components/TickerLookup.vue"
import InternalStatus from "@/components/InternalStatus.vue"
export default {
  name: "Test",
  components: {
    TickerLookup,
    InternalStatus,
  },

  data() {
    return {
      snackbar: false,
      ticker: "",
      showLookup: false,
    }
  },
  methods: {
    tickerChange(ticker) {
      this.ticker = ticker
      this.snackbar = true
      this.showLookup = false
    },
    noTickerChange() {
      this.showLookup = false
    },
    switchTheme() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark
    },
  },
}
</script>

<style lang="scss" scoped></style>
