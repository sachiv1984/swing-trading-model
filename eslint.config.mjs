// eslint.config.mjs
// ─────────────────────────────────────────────────────────────
// ESLint v9 flat config — applies to files Claude writes/edits.
// Existing files are NOT retroactively blocked; violations in
// existing code are tracked in the product backlog instead.
//
// PROTECTED FILE — do not modify without PO sign-off.
// A PreToolUse hook blocks automated modification of this file.
//
// WHY COMMENTS ARE BANNED (no-comments/disallowComments: error)
// -------------------------------------------------------------
// If a comment is needed to explain what code does, the code is not clear
// enough. The fix is better names and smaller functions — not more prose.
// "This function logs in the user" above loginUser() is noise, not signal.
//
// Rule of thumb:
//   - Code that needs a comment → rename it, extract it, simplify it.
//   - Explanation that genuinely can't be expressed in code → it belongs
//     in docs/, not inline.
//
// This rule exists to force self-documenting code at write time, not as a
// review note. The lint feedback loop makes the constraint immediate.
// ─────────────────────────────────────────────────────────────

import js from '@eslint/js';
import globals from 'globals';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import playwright from 'eslint-plugin-playwright';
import noComments from 'eslint-plugin-no-comments';
import betterMaxParams from 'eslint-plugin-better-max-params';

// ── Shared custom rules ─────────────────────────────────────
const customRules = {
  // Ban all inline comments.
  // NOTE: This bans ALL comments — JSDoc, TODO, block comments, etc.
  // If this proves too restrictive for documentation purposes,
  // raise with the team and consider replacing with
  // 'no-warning-comments' to target only TODO/FIXME/HACK.
  'no-comments/disallowComments': 'error',

  // Max function parameters.
  // constructor:10 for DI-heavy classes; func:3 to allow common
  // JS patterns (item, index, array) — raised from the suggested
  // func:2 which breaks array callbacks and event handlers.
  'better-max-params/better-max-params': [
    'error',
    {
      constructor: 10,
      func: 3,
    },
  ],

  // Function body length (blank lines excluded).
  'max-lines-per-function': ['error', { max: 50, skipBlankLines: true, skipComments: true }],

  // File length (blank lines excluded).
  'max-lines': ['error', { max: 550, skipBlankLines: true, skipComments: true }],

  // Magic numbers — allow common sentinels.
  'no-magic-numbers': [
    'error',
    {
      detectObjects: false,
      enforceConst: true,
      ignore: [0, 1, -1, 2],
      ignoreArrayIndexes: true,
    },
  ],
};

// ── Config array ─────────────────────────────────────────────
export default [
  // Global ignores
  {
    ignores: [
      'node_modules/**',
      'build/**',
      'dist/**',
      'coverage/**',
      'public/**',
      '*.config.js',  // postcss.config.js, tailwind.config.js
    ],
  },

  // Base JS recommended rules
  js.configs.recommended,

  // ── React source files ──────────────────────────────────
  {
    files: ['src/**/*.{js,jsx}'],
    plugins: {
      react,
      'react-hooks': reactHooks,
      'no-comments': noComments,
      'better-max-params': betterMaxParams,
    },
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.es2021,
      },
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        ecmaFeatures: { jsx: true },
      },
    },
    settings: {
      react: { version: 'detect' },
    },
    rules: {
      // React core
      ...react.configs.flat.recommended.rules,
      'react/react-in-jsx-scope': 'off',     // Not needed with React 17+
      'react/prop-types': 'warn',             // Warn rather than error (no TS)

      // React Hooks
      ...reactHooks.configs.recommended.rules,

      // Custom rules
      ...customRules,
    },
  },

  // ── Playwright e2e test files ───────────────────────────
  {
    ...playwright.configs['flat/recommended'],
    files: [
      'tests/e2e/**/*.spec.{js,ts}',
      'tests/e2e/**/*.test.{js,ts}',
    ],
    rules: {
      ...playwright.configs['flat/recommended'].rules,

      // Relax some rules for tests
      'no-magic-numbers': 'off',             // Test assertions use literal values
      'max-lines-per-function': ['warn', { max: 100, skipBlankLines: true }],
      'no-comments/disallowComments': 'off', // Test files may have scenario comments
    },
  },
];
