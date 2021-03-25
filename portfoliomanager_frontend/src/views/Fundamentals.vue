<template>
  <div>
    <v-system-bar height="60px" color="primary darken-1">
      <v-btn @click="showLookup = true">Lookup</v-btn>
    </v-system-bar>
    <TickerLookup
      :showDialog="showLookup"
      @tickerChange="showLookup = false"
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
  data() {
    return {
      showLookup: false,
    }
  },
}
</script>

<style lang="scss" scoped></style>
