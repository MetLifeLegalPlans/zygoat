import { FlatCompat } from '@eslint/eslintrc';
import { dirname } from 'path';
import tseslint from 'typescript-eslint';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  // Get type information
  {
    languageOptions: {
      parserOptions: {
        project: true,
        projectService: {
          allowDefaultProject: ['*/ChatWidget.js'],
        },
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
  ...compat.extends('next/core-web-vitals', 'next/typescript'),
  ...tseslint.configs.stylisticTypeChecked,
  ...compat.config({
    extends: [
      'plugin:jest/recommended',
      'plugin:prettier/recommended',
      'next/core-web-vitals',
      'next/typescript',
    ],

    plugins: ['react', 'react-hooks', 'prettier'],

    env: {
      browser: true,
      jest: true,
    },

    globals: {
      // React.js
      React: 'writable',
      // Jest
      describe: false,
      jest: false,
    },

    rules: {
      // Type annotations that are only used in one spot are unnecessary and
      //   add visual clutter to the codebase
      '@typescript-eslint/no-unnecessary-type-parameters': 'error',

      // next.js does not require importing React at the top of the components everytime
      'react/react-in-jsx-scope': 'off',

      // We don't want `console` calls in our code because they are generally
      //   used for debugging.
      'no-console': 'error',

      // This rule makes string interpolation difficult because it makes you
      //   need explicit whitespace expressions.
      'react/jsx-one-expression-per-line': 'off',

      // There are many situations where libraries expect you to modify the
      //   properties of a parameter passed to a function.
      'no-param-reassign': ['error', { props: false }],

      // We want to keep spacing consistent even for the children, which is not
      //   enabled by default, but should be.
      'react/jsx-curly-spacing': [
        'error',
        {
          when: 'never',
          children: true,
          allowMultiline: true,
        },
      ],

      // NextJS Link components want to contain an anchor tag without an href as
      //   a child component (the Link component clones and includes the href).
      'jsx-a11y/anchor-is-valid': [
        'error',
        {
          components: ['Link'],
          specialLink: ['hrefLeft', 'hrefRight'],
          aspects: ['invalidHref', 'preferButton'],
        },
      ],

      // This rule doesn't play nicely with our default aliases.
      'import/no-extraneous-dependencies': ['off'],

      'no-restricted-syntax': ['off'],
      'react/jsx-filename-extension': ['off'],
      'prettier/prettier': 'error',
      'react/jsx-props-no-spreading': ['off'],
      'react/forbid-prop-types': ['off'],
      'react/no-unescaped-entities': ['off'],
      'react/no-array-index-key': ['off'],
      'jsx-a11y/no-static-element-interactions': ['off'],

      // For components that appear more than once, this is impossible
      'jsx-a11y/click-events-have-key-events': ['off'],

      // ...why would anybody ever use this rule?
      'no-plusplus': ['off'],

      // the function keyword has some unexpected scoping issues
      'func-names': ['off'],
      'react/function-component-definition': ['off'],
    },

    settings: {
      'import/resolver': {
        node: {
          paths: './',
        },
      },
    },
  }),
];

export default eslintConfig;
