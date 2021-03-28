<template>
  <div>
    <SubBar altClass="subBarGradientFundamentals">
      <h3>
        {{ cEquity.name }} -
        {{ cEquity.ticker }}
      </h3>
    </SubBar>
    <StockLogo :ticker="cEquity.ticker" />
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
