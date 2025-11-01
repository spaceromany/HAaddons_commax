import js from '@eslint/js';
import tsParser from '@typescript-eslint/parser';
import globals from 'globals';
import svelte from 'eslint-plugin-svelte';
import tseslint from 'typescript-eslint';

const tsConfigs = [
  ...tseslint.configs.recommendedTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,
].map((config) => ({
  ...config,
  files: ['**/*.{ts,tsx}'],
}));

export default [
  {
    ignores: ['build', '.svelte-kit', 'node_modules'],
  },
  js.configs.recommended,
  ...tsConfigs,
  ...svelte.configs['flat/recommended'],
  {
    files: ['**/*.{ts,js,svelte}'],
    languageOptions: {
      parserOptions: {
        parser: tsParser,
        project: './tsconfig.json',
        tsconfigRootDir: import.meta.dirname,
        extraFileExtensions: ['.svelte'],
      },
      globals: {
        ...globals.browser,
      },
    },
    rules: {
      'svelte/no-at-html-tags': 'error',
    },
  },
];
