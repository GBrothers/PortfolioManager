<template>
  <v-sheet color="primary darken-1" outlined width="55px" height="50px">
    <v-main>
      <v-row class="ma-0 pa-0" no-gutters>
        <v-col cols="auto">
          <v-content> API </v-content>
        </v-col>
        <v-spacer />
        <v-col align="end">
          <v-icon
            v-show="apiStatus"
            :color="iconFormat.ok.color"
            :size="iconFormat.ok.size"
          >
            {{ iconFormat.ok.icon }}
          </v-icon>
          <v-icon
            v-show="!apiStatus"
            :color="iconFormat.error.color"
            :size="iconFormat.error.size"
          >
            {{ iconFormat.error.icon }}
          </v-icon>
        </v-col>
      </v-row>
      <v-row class="ma-0 pa-0" no-gutters>
        <v-col cols="auto">
          <div class="">DB</div>
        </v-col>
        <v-spacer />
        <v-col align="end">
          <v-icon
            v-show="dbStatus"
            :color="iconFormat.ok.color"
            :size="iconFormat.ok.size"
          >
            {{ iconFormat.ok.icon }}
          </v-icon>
          <v-icon
            v-show="!dbStatus"
            :color="iconFormat.error.color"
            :size="iconFormat.error.size"
          >
            {{ iconFormat.error.icon }}
          </v-icon>
        </v-col>
      </v-row>
    </v-main>
  </v-sheet>
</template>

<script>
import bes from "@/services/backend_service.js"
export default {
  name: "InternalStatus",
  data() {
    return {
      apiResponse: null,
      dbResponse: null,
      intervalAPI: null,
      intervalDB: null,
      iconFormat: {
        ok: {
          color: "green",
          icon: "mdi-check-bold",
          size: "130%",
        },
        error: {
          color: "red",
          icon: "mdi-alert-circle",
          size: "140%",
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
  },
  beforeDestroy() {
    clearInterval(this.apiStatus)
    clearInterval(this.dbStatus)
  },
  methods: {
    updateApiStatus() {
      bes
        .checkAPI()
        .then((response) => {
          this.apiResponse = response.data
        })
        .catch((err) => {
          this.apiResponse = "nok"
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
  },
}
</script>
