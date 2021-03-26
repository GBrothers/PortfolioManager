<template>
  <div>
    <SubBar altClass="subBarGradientFundamentals">
      <v-btn @click="showLookup = true">Lookup</v-btn>
      <v-spacer></v-spacer>
      <h2>{{ currentTicker }}</h2>
    </SubBar>
    <TickerLookup
      :showDialog="showLookup"
      @tickerChange="tickerChange"
      @noTickerChange="showLookup = false"
    />
  </div>
</template>

<script>
import TickerLookup from "@/components/TickerLookup.vue"
import SubBar from "@/components/BarSub.vue"
export default {
  components: {
    SubBar,
    TickerLookup,
  },
  data() {
    return {
      showLookup: false,
      currentTicker: "",
    }
  },
  methods: {
    tickerChange(ticker) {
      this.currentTicker = ticker
      this.showLookup = false
    },
  },
}
</script>

<style lang="scss" scoped>
.subBarGradientFundamentals {
  background: linear-gradient(
    178deg,
    var(--vuetify-gradientend) 45%,
    var(--vuetify-gradientbeginfundamental) 100%
  );
}
</style>
