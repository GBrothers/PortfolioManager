/*
This module translates colors from vuetify.js to css variables like e.g. --vuetify-primary.
Those variables can be used in css or in the style section of
vue components. If the theme changes from dark to light and
vice versa those variable are updated. So more complex color
schemas are possible, all maintained in vuetify.js. Also custom
colors are possible.

You have to init this module calling the init method with a
reference to this.$vuetify as param from inside a vue component!
e.g. in app.vue in hook created().
*/

var _vtfy
var _dark = "_vtfy.theme.themes.dark."
var _light = "_vtfy.theme.themes.light."
var _properties = []

export default {
  init(vuetify) {
    _vtfy = vuetify
    for (var key in _vtfy.theme.themes.dark) {
      _properties.push(key)
    }
    this.setTheme()
  },

  switchTheme() {
    _vtfy.theme.dark = !_vtfy.theme.dark
    this.setTheme()
  },

  setTheme() {
    _properties.forEach(function (item) {
      document.documentElement.style.setProperty(
        "--vuetify-" + item,
        _vtfy.theme.dark ? eval(_dark + item) : eval(_light + item),
      )
    })
  },
}
