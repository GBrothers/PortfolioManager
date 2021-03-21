import axios from "axios"

const apiClient = axios.create({
  baseURL: `http://192.168.0.71:5001`,
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
}
