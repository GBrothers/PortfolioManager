<template>
  <v-card :width="width" class="d-flex elevation-0" color="rgb(0,0,0,0)">
    <div class="minitext">DB</div>
    <v-spacer />
    <v-icon
      v-show="dbStatus"
      :color="iconOK.color"
      :size="iconOK.size"
      :class="iconOK.class"
    >
      {{ iconOK.icon }}
    </v-icon>
    <v-icon
      v-show="!dbStatus"
      :color="iconError.color"
      :size="iconError.size"
      :class="iconError.class"
    >
      {{ iconError.icon }}
    </v-icon>
  </v-card>
</template>

<script>
import bes from "@/services/backend_service.js"
import dIcons from "./DynIcons.js"
export default {
  props: {
    width: String,
  },
  data() {
    return {
      dbResponse: null,
      intervalDB: null,
      iconOK: dIcons.iconOK,
      iconError: dIcons.iconError,
    }
  },
  computed: {
    dbStatus() {
      return this.dbResponse == "nok" ? false : true
    },
  },
  created() {
    this.updateDBStatus()
    this.intervalDB = setInterval(() => {
      this.updateDBStatus()
    }, 6000)
  },
  beforeDestroy() {
    clearInterval(this.intervalDB)
  },
  methods: {
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

