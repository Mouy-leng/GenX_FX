import globals from "globals";
import tseslint from "typescript-eslint";
import pluginReact from "eslint-plugin-react";
import pluginReactHooks from "eslint-plugin-react-hooks";
import pluginReactRefresh from "eslint-plugin-react-refresh";
import js from "@eslint/js";

export default tseslint.config(
  // Global ignores
  {
    ignores: ["dist", "node_modules", "GenX_FX", "amp-plugins", "amp_cli.egg-info", "aws", "forexconnect_env_37", "genx-cli", "historymaker-1", "ta-lib"],
  },

  // Base config for all files
  js.configs.recommended,

  // Config for TypeScript files (with type checking)
  {
    files: ["client/src/**/*.ts", "client/src/**/*.tsx", "services/server/**/*.ts", "shared/**/*.ts"],
    extends: tseslint.configs.recommended,
    languageOptions: {
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      "@typescript-eslint/no-unused-vars": [
        "error",
        { "argsIgnorePattern": "^_", "varsIgnorePattern": "^_" }
      ],
      "@typescript-eslint/no-explicit-any": "off", // Temporarily disable for now
    }
  },

  // Config for React/JSX files
  {
    files: ["client/src/**/*.jsx", "client/src/**/*.tsx"],
    plugins: {
      react: pluginReact,
      "react-hooks": pluginReactHooks,
      "react-refresh": pluginReactRefresh
    },
    languageOptions: {
      globals: {
        ...globals.browser,
      },
    },
    settings: {
        react: {
            version: "detect"
        }
    },
    rules: {
      ...pluginReact.configs.recommended.rules,
      ...pluginReactHooks.configs.recommended.rules,
      "react/react-in-jsx-scope": "off",
      "react-refresh/only-export-components": "warn",
    },
  },

  // Config for JS files (without type checking)
  {
    files: ["**/*.js", "**/*.cjs", "**/*.mjs"],
    languageOptions: {
        globals: {
            ...globals.node,
        }
    }
  }
);