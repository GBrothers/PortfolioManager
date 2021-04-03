import bes from "@/services/backend_service.js"

export const namespaced = true

export const state = {
  equities: [],
  ctxIDs: ["Fund-1"],
}

export const mutations = {
  ADD_EQUITY(state, { id, ticker, name, exchange, isin, logopath }) {
    let item = state.equities.find((item) => item.id === id)
    if (!item)
      state.equities.push({
        id: id,
        equity: {
          ticker: ticker,
          name: name,
          exchange: exchange,
          isin: isin,
          logopath: logopath,
          isActive: true,
        },
      })
    else {
      item.equity.ticker = ticker
      item.equity.name = name
      item.equity.exchange = exchange
      item.equity.isin = isin
      item.equity.logopath = logopath
      item.equity.isActive = true
    }

    console.log("Commit  For: " + id + " ticker: " + ticker)
  },
  SET_ACTIVE_EQUITY(state, id) {
    state.equities.forEach((entry) => {
      entry.equity.isActive = entry.id === id
    })
  },
  ADD_CTX_ID(state) {
    state.ctxIDs.push("Fund-" + (state.ctxIDs.length + 1))
  },
  REMOVE_CTX_ID(state) {
    state.ctxIDs.pop()
  },
}

export const actions = {
  addEquity({ commit }, { id, ticker, name, exchange, isin }) {
    bes
      .getLogoPath(ticker)
      .then((response) => {
        let logopath = "/img/stocklogos" + response.data
        console.log("Action  For: " + id + " ticker: " + ticker)
        commit("ADD_EQUITY", {
          id,
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
  setActiveEquity({ commit }, id) {
    commit("SET_ACTIVE_EQUITY", id)
  },
  addCtxID({ commit }) {
    commit("ADD_CTX_ID")
  },
  removeCtxID({ commit }) {
    commit("REMOVE_CTX_ID")
  },
}

export const getters = {
  getEquityForCtx: (state) => (ctxID) => {
    var eq_id = state.equities.find((item) => item.id === ctxID)
    console.log("Getter for: " + ctxID + " Found: " + eq_id)
    if (eq_id) {
      return eq_id.equity
    } else {
      return {
        ticker: "",
        name: "",
        exchange: "",
        isin: "",
        logopath: "",
        isActive: false,
      }
    }
  },
  selectedEquity: (state) => {
    let result = state.equities.find((item) => item.equity.isActive)
    if (result) result = result.equity
    return result
  },
  ctxIDs: (state) => {
    return state.ctxIDs
  },
  getActiveCtxID: (state) => {
    return state.equities.find((item) => item.equity.isActive).id
  },
}
