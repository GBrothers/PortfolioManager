<template>
  <v-navigation-drawer
    app
    clipped
    expand-on-hover
    floating
    color="primary"
    overlay-color="error"
    width="180px"
  >
    <v-list dense nav>
      <v-list-item v-for="item in items" :key="item.title" link :to="item.link">
        <v-list-item-icon>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  data() {
    return {
      items: [
        {
          title: "Overview",
          icon: "mdi-view-dashboard",
          link: "Overview",
        },
        {
          title: "Fundamentals",
          icon: "mdi-home-analytics",
          link: "Fundamentals",
        },
        { title: "Portfolio", icon: "mdi-text-box", link: "Portfolio" },
        { title: "About", icon: "mdi-help-box", link: "About" },
      ],
      right: null,
    }
  },
}
</script>
