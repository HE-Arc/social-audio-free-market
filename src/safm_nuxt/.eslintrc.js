module.exports = {
    root: true,
    env: {
        browser: true,
        node: true,
    },
    parserOptions: {
        parser: 'babel-eslint',
    },
    extends: [
        '@nuxtjs',
    ],
    plugins: [
    ],
    // add your custom rules here
    rules: {
        'comma-dangle': ['error', 'only-multiline'],
        indent: ['warn', 4],
        'no-trailing-spaces': ['error', { skipBlankLines: true }],
        semi: ['error', 'always'],
        'space-before-function-paren': ['warn', 'never'],
        'vue/html-indent': ['warn', 4],
    },
};
