import axios from "axios"

const apiClient = axios.create({
  baseURL: localStorage.baseAPIUrl,
  withCredentials: false,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
})

export default {
  searchTicker(phrase, fields) {
    return apiClient.get("/search", {
      params: {
        phrase: phrase,
        fields: fields,
      },
    })
  },
  checkAPI() {
    return apiClient.get("/")
  },
  checkDB() {
    return apiClient.get("/intern/checkdb")
  },
  eodReqLimit() {
    return apiClient.get("/userdata?requests=1")
  },
  getAPIUrl() {
    return apiClient.defaults.baseURL
  },
  setAPIUrl(newAPIIP) {
    localStorage.baseAPIUrl = newAPIIP
    apiClient.defaults.baseURL = newAPIIP
  },
}
