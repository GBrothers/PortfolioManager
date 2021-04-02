<template>
  <div>
    <SubBar height="60px" altClass="subBarGradientFundamentals">
      <div v-for="ctxID in ctxIDs" :key="ctxID">
        <StockLogo :contextID="ctxID" />
      </div>
      <v-icon
        v-show="lastID < maxID"
        @click="addCtxID"
        class="ml-5"
        size="30px"
      >
        mdi-plus-circle
      </v-icon>
      <v-icon v-show="lastID > 1" @click="removeCtxID" class="ml-5" size="30px">
        mdi-minus-circle
      </v-icon>
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
      showLookup: false,
      ctxIDs: ["Fund-1"],
      lastID: 1,
      maxID: 4,
    }
  },
  computed: {
    ce() {
      return this.$store.getters["equityselect/getEquity"]
    },
  },
  methods: {
    addCtxID() {
      this.lastID += 1
      this.ctxIDs.push("Fund-" + this.lastID)
    },
    removeCtxID() {
      this.lastID -= 1
      this.ctxIDs.length = this.ctxIDs.length - 1
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
