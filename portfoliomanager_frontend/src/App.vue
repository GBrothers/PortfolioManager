<template>
  <v-app>
    <v-main>
      <BarLeft />
      <BarTop />
      <router-view></router-view>
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
  </v-app>
</template>

<script>
import TickerLookup from "@/components/TickerLookup.vue"
import BarTop from "@/components/BarTop.vue"
import BarLeft from "@/components/BarLeft.vue"
export default {
  name: "PortfolioManager",
  components: {
    TickerLookup,
    BarTop,
    BarLeft,
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
  },
}
</script>

<style lang="scss">
html {
  overflow-y: auto;
}
</style>
