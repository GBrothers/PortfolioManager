import bes from "@/services/backend_service.js"

export const namespaced = true

export const state = {
  equities: [],
}

export const mutations = {
  SET_CURRENT_EQUITY(state, { id, ticker, name, exchange, isin, logopath }) {
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
    }

    console.log("Commit  For: " + id + " ticker: " + ticker)
  },
}

export const actions = {
  setCurrentEquity({ commit }, { id, ticker, name, exchange, isin }) {
    bes
      .getLogoPath(ticker)
      .then((response) => {
        let logopath = "/img/stocklogos" + response.data
        console.log("Action  For: " + id + " ticker: " + ticker)
        commit("SET_CURRENT_EQUITY", {
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
}

export const getters = {
  getEquity: (state) => (ctxID) => {
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
}
