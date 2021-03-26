<template>
  <v-app-bar clipped-left app flat class="topGradient">
    <v-app-bar-nav-icon />
    <v-app-bar-title>Portfoliomanager<br />V0.01 dev</v-app-bar-title>
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
