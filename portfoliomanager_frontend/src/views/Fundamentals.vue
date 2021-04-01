<template>
  <div>
    <SubBar height="60px" altClass="subBarGradientFundamentals">
      <StockLogo :ticker="ce.ticker" :contextID="ctxID" />
      <div v-show="ce.ticker != ''">
        <h3>{{ ce.name }}</h3>
        <div style="font-size: 80%">
          {{ ce.ticker.toUpperCase() }} | {{ ce.exchange }} |
          {{ ce.isin }}
        </div>
      </div>

      <StockLogo :ticker="ce1.ticker" contextID="Fund2" />
      <div v-show="ce1.ticker != ''">
        <h3>{{ ce1.name }}</h3>
        <div style="font-size: 80%">
          {{ ce1.ticker.toUpperCase() }} | {{ ce1.exchange }} |
          {{ ce1.isin }}
        </div>
      </div>
    </SubBar>
  </div>
</template>

<script>
import SubBar from "@/components/BarSub.vue"
import StockLogo from "@/components/StockLogo.vue"
export default {
  components: {
    SubBar,
    StockLogo,
  },
  data() {
    return {
      ctxID: "Fund",
      showLookup: false,
      currentTicker: "",
    }
  },
  computed: {
    ce() {
      return this.$store.getters["equityselect/getEquity"](this.ctxID)
    },
    ce1() {
      return this.$store.getters["equityselect/getEquity"]("Fund2")
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
