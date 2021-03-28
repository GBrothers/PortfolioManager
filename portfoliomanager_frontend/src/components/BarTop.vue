<template>
  <v-app-bar clipped-left app flat class="topGradient" height="50px">
    <v-app-bar-nav-icon />
    <h1 class="ml-5">Portfoliomanager V0.01 dev</h1>
    <v-spacer />
    <InternalStatus />
  </v-app-bar>
</template>

<script>
import InternalStatus from "@/components/InternalStatus/InternalStatus.vue"
export default {
  name: "BarTop",
  components: {
    InternalStatus,
  },

  data() {
    return {}
  },
  computed: {},
  methods: {},
}
</script>

<style lang="scss" scoped>
.topGradient {
  background: linear-gradient(
    180deg,
    var(--vuetify-gradientbegin) 0%,
    var(--vuetify-gradientend) 100%
  );
}
</style>
