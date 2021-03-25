import Vue from "vue"
import VueRouter from "vue-router"

Vue.use(VueRouter)

const routes = [
  {
    path: "/",
    redirect: { name: "Overview" },
  },
  {
    path: "/about",
    name: "About",
    component: () => import("../views/About.vue"),
  },
  {
    path: "/fundamentals",
    name: "Fundamentals",
    component: () => import("../views/Fundamentals.vue"),
  },
  {
    path: "/overview",
    name: "Overview",
    component: () => import("../views/Overview.vue"),
  },
  {
    path: "/portfolio",
    name: "Portfolio",
    component: () => import("../views/Portfolio.vue"),
  },
]

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
})

export default router
