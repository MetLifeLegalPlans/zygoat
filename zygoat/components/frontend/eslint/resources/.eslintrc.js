module.exports = {
  parser: "babel-eslint",

  extends: [
    "airbnb",
    "plugin:jest/recommended",
    "prettier",
    "prettier/react"
  ],

  plugins: ["react", "react-hooks", "prettier"],

  env: {
    browser: true,
    jest: true
  },

  globals: {
    // React.js
    React: "writable",
    // Jest
    describe: false,
    jest: false,
  },

  rules: {
    // next.js does not require importing React at the top of the components everytime
    "react/react-in-jsx-scope": "off",

    // We don't want `console` calls in our code because they are generally
    //   used for debugging.
    "no-console": "error",

    // This rule makes string interpolation difficult because it makes you
    //   need explicit whitespace expressions.
    "react/jsx-one-expression-per-line": "off",

    // Generally, we want to make sure prop types are used in our components,
    //   but since we use the stores everywhere, it just ends up adding a lot
    //   of boilerplate, so we skip it for the stores only.
    "react/prop-types": [
      "error",
      {
        ignore: ["stores"]
      }
    ],

    // There are many situations where libraries expect you to modify the
    //   properties of a parameter passed to a function.
    'no-param-reassign': ['error', { props: false }],

    // We want to keep spacing consistent even for the children, which is not
    //   enabled by default, but should be.
    "react/jsx-curly-spacing": [
      "error",
      {
        when: "never",
        children: true,
        allowMultiline: true
      }
    ]
  },

  settings: {
    "import/resolver": {
      "babel-module": {
        alias: {
          "@wui": "@bequestinc/wui",
          "@@": "/"
        }
      }
    }
  }
};
