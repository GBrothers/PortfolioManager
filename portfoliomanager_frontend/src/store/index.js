import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentEquity: {
      ticker: "",
      name: "",
      exchange: "",
      isin: "",
      logopath: "",
    },
    currentEquitySearch: {
      searchPhrase: "",
      results: [],
    },
  },
  mutations: {},
  actions: {},
  modules: {},
  getters: {
    currentEquity: (state) => {
      return state.currentEquity
    },
  },
})
