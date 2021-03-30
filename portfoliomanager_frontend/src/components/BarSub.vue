<template>
  <v-system-bar :height="height" :class="altClass">
    <slot></slot>
    <v-spacer></v-spacer>
  </v-system-bar>
</template>

<script>
export default {
  props: {
    height: {
      type: String,
      default: "50px",
    },
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
