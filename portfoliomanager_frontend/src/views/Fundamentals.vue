<template>
  <div>
    <SubBar height="60px" altClass="subBarGradientFundamentals">
      <StockLogo :ticker="cEquity.ticker" />
      <div v-show="cEquity.ticker != ''">
        <h3>{{ cEquity.name }}</h3>
        <div style="font-size: 80%">
          {{ cEquity.ticker.toUpperCase() }} | {{ cEquity.exchange }} |
          {{ cEquity.isin }}
        </div>
      </div>
    </SubBar>
  </div>
</template>

<script>
import SubBar from "@/components/BarSub.vue"
import StockLogo from "@/components/StockLogo.vue"
import { mapState } from "vuex"
export default {
  components: {
    SubBar,
    StockLogo,
  },
  data() {
    return {
      showLookup: false,
      currentTicker: "",
    }
  },
  computed: mapState({
    cEquity: "currentEquity",
  }),
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
