<template>
  <v-card :width="width" class="d-flex elevation-0" color="rgb(0,0,0,0)">
    <div class="minitext">ext</div>
    <v-spacer />
    <v-progress-circular
      v-show="hasRequestData"
      :rotate="-90"
      :value="requestUsage"
      :size="15"
      :color="requestUsageColor"
      class="mr-02 mt-02"
    >
    </v-progress-circular>
    <v-progress-circular
      indeterminate
      v-show="!hasRequestData"
      :size="15"
      color="grey darken-1"
      class="mr-02 mt-03"
    >
    </v-progress-circular>
  </v-card>
</template>

<script>
import bes from "@/services/backend_service.js"
export default {
  props: {
    width: String,
  },
  data() {
    return {
      drlResponse: {
        requests: -1,
        daylimit: -1,
      },
      intervalDRL: null,
    }
  },
  computed: {
    requestUsage() {
      let usage = (this.drlResponse.requests / this.drlResponse.daylimit) * 100
      return usage < 5 ? 5 : usage
    },
    requestUsageColor() {
      let usage = (this.drlResponse.requests / this.drlResponse.daylimit) * 100
      if (usage < 75) return "green"
      if (usage < 90) return "yellow darken-3"
      return "red darken-1"
    },
    hasRequestData() {
      if (this.drlResponse.daylimit == -1) return false
      return true
    },
  },
  created() {
    this.updatedrlStatus()
    this.intervalDRL = setInterval(() => {
      this.updatedrlStatus()
    }, 600000)
  },
  beforeDestroy() {
    clearInterval(this.intervalDRL)
  },
  methods: {
    updatedrlStatus() {
      bes
        .eodReqLimit()
        .then((response) => {
          this.drlResponse.requests = response.data.dayrequests
          this.drlResponse.daylimit = response.data.daylimit
        })
        .catch((err) => {
          console.log("Error Daily Request Limit: " + err)
        })
    },
  },
}
</script>
