module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: 'babel-eslint'
  },
  extends: [
    //'@nuxtjs',
    'eslint:recommended',
    'plugin:nuxt/recommended',
    //'plugin:prettier/recommended'
  ],
  // required to lint *.vue files
  plugins: [
    'vue'
  ],
  // add your custom rules here
  rules: {
    'semi': ['error', 'never'],
    'indent': ['error', 4],
    'no-console': 2,
    'no-alert': 2,
    'no-debugger': 2,
    'vue/max-attributes-per-line': 'off',
    //'prettier/prettier': ['error', { 'semi': false }]
  }
}
