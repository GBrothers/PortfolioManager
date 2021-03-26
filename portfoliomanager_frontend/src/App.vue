<template>
  <v-app>
    <v-main>
      <BarTop />
      <BarLeft />
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import BarTop from "@/components/BarTop.vue"
import BarLeft from "@/components/BarLeft.vue"
import Colors from "@/colors.js"
export default {
  name: "PortfolioManager",
  components: {
    BarTop,
    BarLeft,
  },
  created() {
    Colors.init(this.$vuetify)
  },
}
</script>

<style lang="scss">
html {
  overflow-y: auto;
}
.minitext {
  font-size: 0.7em;
  margin-left: 2px;
  margin-top: 1px;
  margin-bottom: 1px;
  padding-bottom: 0px;
  padding-top: 0px;
}

.mr-02 {
  margin-right: 2px;
}

.mr-01 {
  margin-right: 1px;
}

.mt-02 {
  margin-top: 2px;
}

.mt-01 {
  margin-top: 1px;
}
</style>
