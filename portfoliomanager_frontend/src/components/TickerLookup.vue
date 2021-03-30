<!--
Usage:
      <TickerLookup
        :show-dialog="showLookup"        [Property: Boolean if component is visible]
        @tickerChange="tickerChange"     [Event: ticker selected with ticker symbol as attribute]
        @noTickerChange="noTickerChange" [Event: clicked outside the lookup dialog, no ticker selected]
      />
-->
<template>
  <v-dialog
    v-model="showDialog"
    width="650px"
    transition="dialog-bottom-transition"
    @click:outside="closeDialog"
  >
    <v-card>
      <v-card-title>
        <v-row justify="center"> Search for Company </v-row>
      </v-card-title>
      <v-card-text>
        <v-container py-0>
          <!-- Ticker Input -->
          <v-row justify="center" no-gutters>
            <v-col cols="6">
              <v-text-field
                type="text"
                placeholder="[tcni]:search phrase "
                autofocus
                dense
                outlined
                height="40px"
                class="cursordark"
                :class="{ cursorlight: !this.$vuetify.theme.dark }"
                :value="cEquitySearch.searchPhrase"
                @change="(v) => (searchPhrase = v)"
              ></v-text-field>
            </v-col>
          </v-row>

          <!-- Output Table -->
          <v-row no-gutters>
            <v-col>
              <v-data-table
                class="primary elevation-4"
                height="550px"
                hide-default-footer
                disable-pagination
                fixed-header
                :headers="headers"
                :items="cEquitySearch.results"
                sort-by="ticker"
                no-data-text=""
                @click:row="selectRow"
              >
                <template v-slot:footer>
                  <v-container class="primary">
                    <v-row justify="center" no-gutters>
                      {{
                        cEquitySearch.results.length == 0
                          ? ticker.length == 0
                            ? "Please enter a search phrase "
                            : "No matching companies found"
                          : "Found " +
                            cEquitySearch.results.length +
                            (cEquitySearch.results.length == 1
                              ? " company"
                              : " companies")
                      }}
                    </v-row>
                  </v-container>
                </template>
              </v-data-table>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import bes from "@/services/backend_service.js"
import { mapState } from "vuex"
export default {
  name: "TickerLookup",
  props: {
    showDialog: Boolean,
  },
  data() {
    return {
      searchFields: "",
      snackbar: false,
      searchPhrase: "",
      ticker: "",
      selected: "",
      headers: [
        {
          text: "Ticker",
          value: "ticker",
          width: "90px",
          class: "primary",
        },
        {
          text: "Name",
          value: "name",
          width: "220px",
          class: "primary",
        },
        {
          text: "Exchange",
          value: "exchange",
          width: "110px",
          class: "primary",
        },
        {
          text: "ISIN",
          value: "isin",
          width: "100px",
          class: "primary",
        },
      ],
    }
  },
  computed: mapState({
    cEquitySearch: "currentEquitySearch",
  }),
  watch: {
    searchPhrase: function () {
      this.searchPhrase = this.searchPhrase.trim()
      this.cEquitySearch.searchPhrase = this.searchPhrase
      this.ticker = ""
      this.searchFields = ""

      if (this.searchPhrase != "") {
        let sphrase = this.searchPhrase.split(":")
        if (sphrase.length == 1) {
          this.searchFields = "tn"
          this.ticker = this.searchPhrase
        }
        if (sphrase.length == 2) {
          this.searchFields = ""
          sphrase[0].includes("t") ? (this.searchFields += "t") : ""
          sphrase[0].includes("n") ? (this.searchFields += "n") : ""
          sphrase[0].includes("e") ? (this.searchFields += "e") : ""
          sphrase[0].includes("i") ? (this.searchFields += "i") : ""
          this.ticker = sphrase[1]
        }
      }
      if (this.ticker != "") {
        bes
          .searchTicker(this.ticker, this.searchFields)
          .then((response) => {
            this.cEquitySearch.results = response.data
          })
          .catch((error) => {
            console.log(error)
          })
      }
    },
  },
  methods: {
    selectRow(event) {
      this.$emit("tickerChange", {
        ticker: event.ticker,
        name: event.name,
        exchange: event.exchange,
        isin: event.isin,
      })
    },
    closeDialog() {
      this.$emit("noTickerChange")
    },
  },
}
</script>

<style lang="scss" scoped>
.cursordark {
  caret-color: rgb(204, 150, 255) !important;
}

.cursorlight {
  caret-color: rgb(99, 72, 124) !important;
}
</style>
