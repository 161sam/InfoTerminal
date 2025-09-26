/* eslint-env node */
module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  parserOptions: {
    project: ['./tsconfig.json'],
    tsconfigRootDir: __dirname,
  },
  plugins: ['@typescript-eslint', 'import', 'local-rules'],
  extends: ['next/core-web-vitals'],
  settings: {
    'import/resolver': {
      typescript: {},
    },
  },
  rules: {
    // Keep rules strict; we aim for 0 errors.
    'react/no-unescaped-entities': 'error',
    '@next/next/no-html-link-for-pages': 'error',
  },
  overrides: [
    {
      files: ['**/*.test.{ts,tsx}', '**/__tests__/**/*.{ts,tsx}'],
      env: { node: true, jest: true },
      rules: {
        // Tests may use require where needed
        '@typescript-eslint/no-var-requires': 'off',
      },
    },
  ],
};

