import bes from "@/services/backend_service.js"

export const namespaced = true

export const state = {
  currentEquitySearch: {
    searchPhrase: "",
    results: [],
  },
}

export const mutations = {
  SET_CURRENT_EQUITY_SEARCH(state, { sp, results }) {
    state.currentEquitySearch.searchPhrase = sp
    state.currentEquitySearch.results = results
  },
}

export const actions = {
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
}

export const getters = {
  currentEquitySearchResultLength(state) {
    return state.currentEquitySearch.results.length
  },
}
