<template>
  <v-system-bar height="40px" :class="altClass">
    <slot></slot>
    <v-spacer></v-spacer>
  </v-system-bar>
</template>

<script>
export default {
  props: {
    altClass: {
      type: String,
      default: "subBarGradient",
    },
  },
}
</script>

<style lang="scss" scoped>
.subBarGradient {
  background: rgb(26, 26, 45);
  background: linear-gradient(
    177deg,
    var(--vuetify-gradientbegin) 50%,
    var(--vuetify-gradientend) 100%
  );
}
</style>
