import bes from "@/services/backend_service.js"

export const namespaced = true

export const state = {
  equities: [
    {
      id: "Fund",
      items: [
        {
          ticker: "",
          name: "",
          exchange: "",
          isin: "",
          logopath: "",
          isActive: true,
        },
      ],
    },
    {
      id: "Fund2",
      items: [
        {
          ticker: "",
          name: "",
          exchange: "",
          isin: "",
          logopath: "",
          isActive: true,
        },
      ],
    },
  ],
}

export const mutations = {
  SET_CURRENT_EQUITY(state, { id, ticker, name, exchange, isin, logopath }) {
    let equity = state.equities.filter((item) => item.id === id)[0].items[0]
    equity.ticker = ticker
    equity.name = name
    equity.exchange = exchange
    equity.isin = isin
    equity.logopath = logopath
    equity.isActive = true
  },
}

export const actions = {
  setCurrentEquity({ commit }, { id, ticker, name, exchange, isin }) {
    bes
      .getLogoPath(ticker)
      .then((response) => {
        let logopath = "/img/stocklogos" + response.data
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
    return state.equities.filter((item) => item.id === ctxID)[0].items[0]
  },
}
