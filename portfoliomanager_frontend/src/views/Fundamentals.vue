<template>
  <div>
    <SubBar height="60px" altClass="subBarGradientFundamentals">
      <div v-for="ctxID in ctxIDs" :key="ctxID">
        <StockLogo :contextID="ctxID" />
      </div>
      <v-icon
        v-show="this.ctxIDs.length < maxID"
        @click="addCtxID"
        class="ml-5"
        size="30px"
      >
        mdi-plus-circle
      </v-icon>
      <v-icon
        v-show="this.ctxIDs.length > 1"
        @click="removeCtxID"
        class="ml-5"
        size="30px"
      >
        mdi-minus-circle
      </v-icon>
    </SubBar>
    <v-card v-if="se" class="d-inline-block ma-10">
      <div>{{ se.ticker }}</div>
      <div>{{ se.name }}</div>
      <div>{{ se.exchange }}</div>
      <div>{{ se.isin }}</div>
    </v-card>
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
      showLookup: false,
      maxID: 4,
    }
  },
  computed: {
    se() {
      return this.$store.getters["equityselect/selectedEquity"]
    },
    ctxIDs() {
      return this.$store.state.equityselect.ctxIDs
    },
  },
  methods: {
    addCtxID() {
      this.$store.dispatch("equityselect/addCtxID")
    },
    removeCtxID() {
      this.$store.dispatch("equityselect/removeCtxID")
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
