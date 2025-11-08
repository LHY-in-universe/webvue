module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
    '@vue/eslint-config-prettier'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  rules: {
    // 生产环境警告，开发环境关闭
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    
    // Vue特定规则
    'vue/multi-word-component-names': 'off',
    'vue/no-unused-vars': 'warn',
    'vue/no-v-html': 'warn',
    'vue/require-default-prop': 'off',
    'vue/require-explicit-emits': 'warn',
    
    // 代码质量
    'no-unused-vars': 'warn',
    'no-undef': 'error',
    'prefer-const': 'warn',
    'no-var': 'error',
    
    // 禁止使用alert
    'no-alert': 'error',
    'no-confirm': 'error'
  },
  ignorePatterns: [
    'node_modules/',
    'dist/',
    '*.config.js'
  ]
}

