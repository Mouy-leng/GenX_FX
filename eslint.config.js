import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";

export default [
  // Global ignores
  {
    ignores: ["node_modules/", "dist/", "build/", "forexconnect_env_37/", "*.lock", "**/__pycache__/"],
  },

  // Base configurations for all JS/TS files
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,

  // Configuration for React client-side code
  {
    files: ["client/src/**/*.{js,jsx,ts,tsx}"],
    languageOptions: {
      parserOptions: {
        ecmaFeatures: { jsx: true },
        // Set project for type-aware linting
        project: "./tsconfig.json",
      },
      globals: {
        ...globals.browser,
      },
    },
    plugins: {
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
      "react-refresh/only-export-components": "warn",
      // Add other React-specific rules here
    },
    settings: {
      react: {
        version: "detect",
      },
    },
  },

  // Configuration for server-side Node.js/config files
  {
    files: [
        "services/server/**/*.ts",
        "genx-cli/**/*.js",
        "*.config.js",
        "*.config.ts"
    ],
    languageOptions: {
      globals: {
        ...globals.node,
      },
    },
  },
];