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
                :value="ces.searchPhrase"
                @change="(v) => (inputPhrase = v)"
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
                :items="ces.results"
                sort-by="ticker"
                no-data-text=""
                @click:row="selectRow"
              >
                <template v-slot:footer>
                  <v-container class="primary">
                    <v-row justify="center" no-gutters>
                      {{
                        resultLength == 0
                          ? ticker.length == 0
                            ? "Please enter a search phrase "
                            : "No matching companies found"
                          : "Found " +
                            resultLength +
                            (resultLength == 1 ? " company" : " companies")
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
import { mapState, mapGetters } from "vuex"
export default {
  name: "TickerLookup",
  props: {
    showDialog: Boolean,
  },
  data() {
    return {
      inputPhrase: "",
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
  computed: {
    ...mapState({
      ces: (state) => state.tickerlookup.currentEquitySearch,
    }),
    ...mapGetters({
      resultLength: "tickerlookup/currentEquitySearchResultLength",
    }),
    ticker() {
      let sphrase = this.inputPhrase.split(":")
      return sphrase.length == 1 ? sphrase[0].trim() : sphrase[1].trim()
    },
    searchFields() {
      let searchFields = ""
      if (this.inputPhrase != "") {
        let sphrase = this.inputPhrase.split(":")
        if (sphrase.length == 1) {
          searchFields = "tn"
        } else {
          sphrase[0].includes("t") ? (searchFields += "t") : ""
          sphrase[0].includes("n") ? (searchFields += "n") : ""
          sphrase[0].includes("e") ? (searchFields += "e") : ""
          sphrase[0].includes("i") ? (searchFields += "i") : ""
        }
      }
      return searchFields
    },
  },
  watch: {
    inputPhrase: function () {
      this.$store.dispatch("tickerlookup/doEquitySearch", {
        ticker: this.ticker,
        fields: this.searchFields,
      })
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
