<template>
  <v-card color="rgb(0,0,0,0.05)" elevation="2">
    <!-- First row -->
    <v-row class="align-center" no-gutters>
      <!-- First col -->
      <APIStatus width="45px" />
      <v-divider vertical class="mx-0 darken-2" />
      <!-- Second Col -->
      <ThemeChange width="58px" />
    </v-row>
    <v-divider class="mx-0" />

    <!-- Second Row -->
    <v-row class="align-center" no-gutters>
      <!-- First Col -->
      <DBStatus width="45px" />
      <v-divider vertical class="mx-0" />
      <!-- Second Col -->
      <div class="minitext">-</div>
    </v-row>
    <v-divider class="mx-0" />

    <!-- Third Row -->
    <v-row class="align-center" no-gutters>
      <!-- First Col -->
      <DRLStatus width="45px" />
      <v-divider vertical class="mx-0" />
      <!-- Second Col -->
      <div class="minitext">-</div>
    </v-row>
  </v-card>
</template>

<script>
import DBStatus from "./DBStatus.vue"
import APIStatus from "./APIStatus.vue"
import ThemeChange from "./ThemeChange.vue"
import DRLStatus from "./DRLStatus.vue"
export default {
  name: "InternalStatus",
  components: {
    DBStatus,
    APIStatus,
    ThemeChange,
    DRLStatus,
  },
}
</script>
