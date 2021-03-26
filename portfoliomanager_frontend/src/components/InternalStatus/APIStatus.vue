<template>
  <v-card
    :width="width"
    class="d-flex elevation-0"
    color="rgb(0,0,0,0)"
    @click="showAPIDialog = true"
  >
    <div class="minitext">API</div>
    <v-spacer />
    <v-icon
      v-show="apiStatus"
      :color="iconOK.color"
      :size="iconOK.size"
      :class="iconOK.class"
    >
      {{ iconOK.icon }}
    </v-icon>
    <v-icon
      v-show="!apiStatus"
      :color="iconError.color"
      :size="iconError.size"
      :class="iconError.class"
    >
      {{ iconError.icon }}
    </v-icon>
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
  </v-card>
</template>

<script>
import bes from "@/services/backend_service.js"
import dIcon from "./DynIcons.js"
export default {
  props: {
    width: String,
  },
  data() {
    return {
      iconOK: dIcon.iconOK,
      iconError: dIcon.iconError,
      showAPIDialog: false,
      newAPIIP: "",
      apiResponse: null,
      intervalAPI: null,
      rules: [
        (value) => !!value || "Required.",
        (value) => this.isURL(value) || "URL is not valid",
      ],
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
    APIIP() {
      return bes.getAPIUrl()
    },
  },
  created() {
    this.newAPIIP = this.APIIP
    this.updateApiStatus()
    this.intervalAPI = setInterval(() => {
      this.updateApiStatus()
    }, 6000)
  },
  beforeDestroy() {
    clearInterval(this.intervalAPI)
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
        })
        .catch((err) => {
          this.apiResponse = "nok"
          console.log("Error API: " + err)
        })
    },
  },
}
</script>
