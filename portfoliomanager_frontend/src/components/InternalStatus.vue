<template>
  <v-card width="108px" outlined>
    <!-- First row -->
    <v-row class="align-center" no-gutters>
      <!-- First col -->
      <v-card
        width="45px"
        class="d-flex elevation-0 primary"
        @click="showAPIDialog = true"
      >
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
      </v-card>
      <v-dialog
        width="280px"
        :value="showAPIDialog"
        @click:outside="closeAPIDialog"
      >
        <v-card color="primary">
          <v-card-title primary-title>Backend API URL</v-card-title>
          <v-text-field
            v-model="newAPIIP"
            outlined
            class="mx-4"
            solo-inverted
            append-icon="mdi-send"
            color="success"
            :rules="rules"
            @click:append="updateAPIIP"
            @change="updateAPIIP"
          >
          </v-text-field>
        </v-card>
      </v-dialog>

      <v-divider vertical class="mx-0 darken-2" />

      <!-- Second Col -->
      <v-card
        @click="switchTheme"
        class="d-flex primary elevation-0"
        width="59px"
      >
        <div class="minitext">Theme</div>
        <v-spacer />
        <v-icon
          size="95%"
          :color="
            this.$vuetify.theme.dark ? 'blue darken-1' : 'yellow darken-3'
          "
        >
          {{
            this.$vuetify.theme.dark ? "mdi-weather-night" : "mdi-weather-sunny"
          }}
        </v-icon>
      </v-card>
    </v-row>

    <v-divider class="mx-0" />

    <!-- Second Row -->
    <v-row class="align-center" no-gutters>
      <!-- First Col -->
      <v-card width="45px" class="d-flex primary elevation-0">
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
      </v-card>

      <v-divider vertical class="mx-0" />

      <!-- Second Col -->
      <div class="minitext">-</div>
      <v-spacer />
      <div class="minitext">-</div>
    </v-row>

    <v-divider class="mx-0" />

    <!-- Third Row -->
    <v-row class="align-center" no-gutters>
      <!-- First Col -->
      <v-card width="45px" class="d-flex primary elevation-0">
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
      <v-divider vertical class="mx-0" />

      <!-- Second Col -->
      <div class="minitext">-</div>
      <v-spacer />
      <div class="minitext">-</div>
    </v-row>
  </v-card>
</template>

<script>
import bes from "@/services/backend_service.js"
export default {
  name: "InternalStatus",
  data() {
    return {
      showAPIDialog: false,
      newAPIIP: "",
      apiResponse: null,
      dbResponse: null,
      drlResponse: {
        requests: -1,
        daylimit: -1,
      },
      intervalAPI: null,
      intervalDB: null,
      intervalDRL: null,
      rules: [
        (value) => !!value || "Required.",
        (value) => this.isURL(value) || "URL is not valid",
      ],
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
      if (!this.apiResponse) return false
      else if (this.apiResponse == "") return false
      else if (this.apiResponse.toLowerCase().includes("nok")) return false
      else if (this.apiResponse.toLowerCase().includes("404")) return false
      return true
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
    APIIP() {
      return bes.getAPIUrl()
    },
  },
  created() {
    this.newAPIIP = this.APIIP
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
    closeAPIDialog() {
      this.newAPIIP = this.APIIP
      this.showAPIDialog = false
    },
    updateAPIIP() {
      bes.setAPIUrl(this.newAPIIP)
      this.showAPIDialog = false
    },

    switchTheme() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark
      localStorage.isdark = this.$vuetify.theme.dark
    },
    isURL(str) {
      let url
      try {
        url = new URL(str)
      } catch (_) {
        return false
      }

      return (
        (url.protocol === "http:" || url.protocol === "https:") &&
        url.port != ""
      )
    },
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
