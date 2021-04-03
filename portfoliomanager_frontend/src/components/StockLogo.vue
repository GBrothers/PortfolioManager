<template>
  <div class="ml-3">
    <v-row align="center">
      <!-- LOGO -->
      <v-card
        @click="showLookup = true"
        width="50px"
        height="50px"
        class="pa-01 white"
      >
        <v-icon v-show="ce.logopath == ''" class="primary" size="48px">
          mdi-text-box-search
        </v-icon>
        <img v-show="ce.logopath != ''" :src="ce.logopath" class="logo" />
      </v-card>

      <!-- InfoText -->
      <v-card
        v-if="ce.ticker == ''"
        max-width="250px"
        class="ml-02 mr-4 pa-1"
        color="rgb(0,0,0,0)"
        height="50px"
        flat
      >
        <div>
          <h3>No Equity selected</h3>
          <div class="smalltext">click on the search icon...</div>
        </div>
      </v-card>

      <v-card
        v-if="ce.ticker != ''"
        max-width="250px"
        :class="
          isActive
            ? 'ml-02 mr-5 pa-1 elevation-2'
            : 'ml-02 mr-5 pa-1 elevation-0'
        "
        :color="isActive ? 'rgb(255, 255, 255, 0.15)' : 'rgb(0, 0, 0, 0)'"
        :height="isActive ? '52px' : '50px'"
        hover
      >
        <div v-show="ce.ticker != ''" @click="setActiveEquity">
          <h3>{{ ce.name }}</h3>
          <div class="smalltext">
            {{ ce.ticker.toUpperCase() }} | {{ ce.exchange }} |
            {{ ce.isin }}
          </div>
        </div>
      </v-card>
    </v-row>
    <TickerLookup
      :showDialog="showLookup"
      @tickerChange="tickerChange"
      @noTickerChange="showLookup = false"
    />
  </div>
</template>

<script>
import TickerLookup from "@/components/TickerLookup.vue"
export default {
  components: {
    TickerLookup,
  },
  props: {
    ticker: String,
    contextID: String,
  },
  data() {
    return {
      showLookup: false,
    }
  },
  computed: {
    ce() {
      return this.$store.getters["equityselect/getEquityForCtx"](this.contextID)
    },
    isActive() {
      return (
        this.$store.getters["equityselect/getActiveCtxID"] == this.contextID
      )
    },
  },
  methods: {
    tickerChange(event) {
      this.showLookup = false
      this.$store.dispatch("equityselect/addEquity", {
        id: this.contextID,
        ticker: event.ticker,
        name: event.name,
        exchange: event.exchange,
        isin: event.isin,
        // logopath is added by the store action
      })
    },
    setActiveEquity() {
      this.$store.dispatch("equityselect/setActiveEquity", this.contextID)
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
