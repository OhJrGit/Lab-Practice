import js from "@eslint/js";
import globals from "globals";
import pluginReact from "eslint-plugin-react";
import json from "@eslint/json";
import css from "@eslint/css";
import { defineConfig } from "eslint/config";

import jest from "eslint-plugin-jest";

import pluginSecurity from "eslint-plugin-security";

export default defineConfig([
  { files: ["**/*.{js,mjs,cjs,jsx}"], plugins: { js }, extends: ["js/recommended"], languageOptions: { globals: globals.browser } },
  { files: ["**/*.{js,mjs,cjs,jsx}"], ...pluginReact.configs.flat.recommended },
  { files: ["**/*.json"], plugins: { json }, language: "json/json", extends: ["json/recommended"] },
  { files: ["**/*.css"], plugins: { css }, language: "css/css", extends: ["css/recommended"] },
  {
    files: ['**/*.spec.js', '**/*.test.js', '**/*.test.jsx'],
    plugins: { 
      jest 
    },
    languageOptions: {
      globals: {
        ...globals.jest,
      },
    },
    rules: {
      'jest/no-disabled-tests': 'warn',
      'jest/no-focused-tests': 'error',
      'jest/no-identical-title': 'error',
      'jest/prefer-to-have-length': 'warn',
      'jest/valid-expect': 'error',
    },
  },
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    plugins: {
      security: pluginSecurity,
    },
    rules: {
      'react/react-in-jsx-scope': 'off',
      'security/detect-eval-with-expression': 'error'
    },
    settings: {
      react: {
        version: 'detect',
      }
    }
  }
]);
