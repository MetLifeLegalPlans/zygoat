module.exports = {
  singleQuote: true,
  trailingComma: 'all',
  endOfLine: 'lf',
  printWidth: 100,
  arrowParens: 'avoid',
  plugins: [require.resolve('@trivago/prettier-plugin-sort-imports')],
  importOrder: ['react', '<THIRD_PARTY_MODULES>', 'components/*', 'hooks/*', 'constants/*'],
  importOrderSeparation: true,
  importOrderSortSpecifiers: true,
};
