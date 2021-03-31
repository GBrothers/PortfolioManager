<template>
  <v-card
    @click="showLookup = true"
    width="50px"
    height="50px"
    class="ma-3 pa-01 white"
  >
    <v-icon v-show="currentEquity.logopath == ''" class="primary" size="48px"
      >mdi-text-box-search</v-icon
    >
    <img
      v-show="currentEquity.logopath != ''"
      :src="currentEquity.logopath"
      class="logo"
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
  computed: { ...mapState(["currentEquity"]) },
  methods: {
    tickerChange(event) {
      this.showLookup = false
      this.$store.dispatch("setCurrentEquity", {
        ticker: event.ticker,
        name: event.name,
        exchange: event.exchange,
        isin: event.isin,
        // logopath is added by the store action
      })
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
