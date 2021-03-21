<template>
  <v-card
    width="50px"
    class="pa-0"
    outlined
    :style="{ border: '1px darken-2 grey' }"
  >
    <v-row class="align-center" no-gutters>
      <div class="minitext">API</div>
      <v-spacer />
      <v-icon
        v-show="apiStatus"
        :color="iconFormat.ok.color"
        :size="iconFormat.ok.size"
        :class="iconFormat.ok.class"
      >
        {{ iconFormat.ok.icon }}
      </v-icon>
      <v-icon
        v-show="!apiStatus"
        :color="iconFormat.error.color"
        :size="iconFormat.error.size"
        :class="iconFormat.ok.class"
      >
        {{ iconFormat.error.icon }}
      </v-icon>
    </v-row>
    <v-divider class="mx-0 darken-2 grey" />
    <v-row class="align-center" no-gutters>
      <div class="minitext">DB</div>
      <v-spacer />
      <v-icon
        v-show="dbStatus"
        :color="iconFormat.ok.color"
        :size="iconFormat.ok.size"
        :class="iconFormat.ok.class"
      >
        {{ iconFormat.ok.icon }}
      </v-icon>
      <v-icon
        v-show="!dbStatus"
        :color="iconFormat.error.color"
        :size="iconFormat.error.size"
        :class="iconFormat.ok.class"
      >
        {{ iconFormat.error.icon }}
      </v-icon>
    </v-row>
    <v-divider class="mx-0 darken-2 grey" />
    <v-row class="align-center" no-gutters>
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
    </v-row>
  </v-card>
</template>

<script>
import bes from "@/services/backend_service.js"
export default {
  name: "InternalStatus",
  data() {
    return {
      apiResponse: null,
      dbResponse: null,
      drlResponse: {
        requests: -1,
        daylimit: -1,
      },
      intervalAPI: null,
      intervalDB: null,
      intervalDRL: null,
      iconFormat: {
        ok: {
          color: "green",
          icon: "mdi-check-bold",
          size: "100%",
          class: "pa-0 mr-02",
        },
        error: {
          color: "red",
          icon: "mdi-alert-circle",
          size: "100%",
          class: "pa-0 mr-02",
        },
      },
    }
  },
  computed: {
    apiStatus() {
      return this.apiResponse == "nok" ? false : true
    },
    dbStatus() {
      return this.dbResponse == "nok" ? false : true
    },
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
    this.updateApiStatus()
    this.updateDBStatus()
    this.intervalAPI = setInterval(() => {
      this.updateApiStatus()
    }, 6000)
    this.intervalDB = setInterval(() => {
      this.updateDBStatus()
    }, 6000)
    this.intervalDRL = setInterval(() => {
      this.updatedrlStatus()
    }, 600000)
  },
  beforeDestroy() {
    clearInterval(this.intervalAPI)
    clearInterval(this.intervalDB)
    clearInterval(this.intervalDRL)
  },
  methods: {
    updateApiStatus() {
      bes
        .checkAPI()
        .then((response) => {
          this.apiResponse = response.data
          if (this.drlResponse.daylimit == -1) {
            this.updatedrlStatus()
          }
        })
        .catch((err) => {
          this.apiResponse = "nok"
          this.drlResponse.daylimit = -1
          console.log("Error API: " + err)
        })
    },
    updateDBStatus() {
      bes
        .checkDB()
        .then((response) => {
          this.dbResponse = response.data
        })
        .catch((err) => {
          this.dbResponse = "nok"
          console.log("Error DB: " + err)
        })
    },
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

<style scoped>
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
