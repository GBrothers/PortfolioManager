<template>
  <v-app-bar clipped-left app color="primary" flat>
    <v-app-bar-nav-icon />
    <v-app-bar-title>
      Portfoliomanager <br />
      V0.1
    </v-app-bar-title>
    <template>
      <v-row justify="center" align="center">
        <v-spacer></v-spacer>
        <v-col cols="auto">
          <InternalStatus />
        </v-col>
      </v-row>
    </template>
  </v-app-bar>
</template>

<script>
import InternalStatus from "@/components/InternalStatus.vue"
export default {
  name: "BarTop",
  components: {
    InternalStatus,
  },

  data() {
    return {}
  },
  computed: {
    Theme() {
      return localStorage.isdark
    },
  },
  methods: {},
}
</script>
