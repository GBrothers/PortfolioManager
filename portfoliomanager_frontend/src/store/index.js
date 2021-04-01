import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)
import * as tickerlookup from "@/store/modules/tickerlookup.js"
import * as equityselect from "@/store/modules/equityselect.js"
export default new Vuex.Store({
  modules: {
    tickerlookup,
    equityselect,
  },
  state: {},
  mutations: {},
  actions: {},
  getters: {},
})
