<template>
  <div>
    <SubBar height="60px" altClass="subBarGradientFundamentals">
      <StockLogo :ticker="currentEquity.ticker" />
      <div v-show="currentEquity.ticker != ''">
        <h3>{{ currentEquity.name }}</h3>
        <div style="font-size: 80%">
          {{ currentEquity.ticker.toUpperCase() }} |
          {{ currentEquity.exchange }} |
          {{ currentEquity.isin }}
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
  computed: {
    ...mapState(["currentEquity"]),
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
