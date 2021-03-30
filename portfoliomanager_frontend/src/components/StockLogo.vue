<template>
  <v-card
    @click="showLookup = true"
    width="50px"
    height="50px"
    class="ma-3 pa-01 white"
  >
    <v-icon v-show="cEquity.logopath == ''" class="primary" size="48px"
      >mdi-text-box-search</v-icon
    >
    <img v-show="cEquity.logopath != ''" :src="cEquity.logopath" class="logo" />
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
import { mapState } from "vuex"
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
          this.cEquity.logopath = "/img/stocklogos" + response.data
        })
        .catch((err) => {
          console.log("Error API: " + err)
        })
    },
  },
  computed: mapState({
    cEquity: "currentEquity",
  }),
  methods: {
    tickerChange(event) {
      this.showLookup = false
      this.cEquity.ticker = event.ticker
      this.cEquity.name = event.name
      this.cEquity.exchange = event.exchange
      this.cEquity.isin = event.isin
    },
  },
}
</script>

<style lang="scss" scoped>
.logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>
