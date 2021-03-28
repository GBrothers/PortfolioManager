<template>
  <v-card
    @click="showLookup = true"
    width="70px"
    height="70px"
    class="ma-3 pa-1 white"
  >
    <v-icon
      v-show="this.$store.state.currentEquity.logopath == ''"
      class="ma-01 primary"
      size="61"
      >mdi-text-box-search</v-icon
    >
    <v-img
      v-show="this.$store.state.currentEquity.logopath != 0"
      :src="this.$store.state.currentEquity.logopath"
    />
    <TickerLookup
      :showDialog="showLookup"
      @tickerChange="tickerChange"
      @noTickerChange="showLookup = false"
    />
  </v-card>
</template>

<script>
import TickerLookup from "@/components/TickerLookup.vue"
import bes from "@/services/backend_service.js"
export default {
  components: {
    TickerLookup,
  },
  props: {
    ticker: String,
  },
  data() {
    return {
      showLookup: false,
    }
  },
  watch: {
    ticker: function () {
      bes
        .getLogoPath(this.ticker)
        .then((response) => {
          this.$store.state.currentEquity.logopath =
            "/img/stocklogos" + response.data
        })
        .catch((err) => {
          console.log("Error API: " + err)
        })
    },
  },
  methods: {
    tickerChange(event) {
      this.showLookup = false
      this.$store.state.currentEquity.ticker = event.ticker
      this.$store.state.currentEquity.name = event.name
    },
  },
}
</script>

<style lang="scss" scoped></style>
