// ESLint settings for the JavaScript in this toolbox.
//
// The only JavaScript here is Postman pre-request scripts (postman/*.js), which
// run inside Postman's sandbox: `pm` is provided by the host, and the scripts
// are plain scripts, not modules. The config is dependency-free on purpose -
// CI runs `npx eslint` and the repo keeps no package.json or lockfile.
export default [
  {
    files: ["**/*.js", "**/*.cjs"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "script",
      globals: {
        // Postman sandbox
        pm: "readonly",
        // available in both Postman and Node
        console: "readonly",
        require: "readonly",
        setTimeout: "readonly",
        clearTimeout: "readonly",
      },
    },
    rules: {
      "no-undef": "error",
      "no-unused-vars": "error",
      "no-dupe-keys": "error",
      "no-dupe-args": "error",
      "no-unreachable": "error",
      "no-cond-assign": "error",
      "no-constant-condition": "error",
      "no-dupe-else-if": "error",
      "no-duplicate-case": "error",
      "no-fallthrough": "error",
      "no-func-assign": "error",
      "no-self-assign": "error",
      "no-sparse-arrays": "error",
      "no-unsafe-negation": "error",
      "use-isnan": "error",
      "valid-typeof": "error",
    },
  },
  {
    // ES modules in the repo itself, such as this config file.
    files: ["**/*.mjs"],
    languageOptions: { ecmaVersion: 2022, sourceType: "module" },
    rules: {
      "no-undef": "error",
      "no-unused-vars": "error",
      "no-dupe-keys": "error",
    },
  },
];
