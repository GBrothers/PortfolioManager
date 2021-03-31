import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)
import bes from "@/services/backend_service.js"
import * as tickerlookup from "@/store/modules/tickerlookup.js"
export default new Vuex.Store({
  modules: {
    tickerlookup,
  },
  state: {
    currentEquity: {
      ticker: "",
      name: "",
      exchange: "",
      isin: "",
      logopath: "",
    },
  },
  mutations: {
    SET_CURRENT_EQUITY(state, { ticker, name, exchange, isin, logopath }) {
      state.currentEquity.ticker = ticker
      state.currentEquity.name = name
      state.currentEquity.exchange = exchange
      state.currentEquity.isin = isin
      state.currentEquity.logopath = logopath
    },
  },
  actions: {
    doEquitySearch({ commit }, { ticker, fields }) {
      if (ticker != "") {
        bes
          .searchTicker(ticker, fields)
          .then((response) => {
            commit("SET_CURRENT_EQUITY_SEARCH", {
              sp: fields + ":" + ticker,
              results: response.data,
            })
          })
          .catch((error) => {
            console.log(error)
          })
      }
    },
    setCurrentEquity({ commit }, { ticker, name, exchange, isin }) {
      bes
        .getLogoPath(ticker)
        .then((response) => {
          let logopath = "/img/stocklogos" + response.data
          commit("SET_CURRENT_EQUITY", {
            ticker,
            name,
            exchange,
            isin,
            logopath,
          })
        })
        .catch((err) => {
          console.log("Error API: " + err)
        })
    },
  },
})
