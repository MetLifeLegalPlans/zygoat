const withPlugins = require('next-compose-plugins');

const { withSentryConfig } = require('@sentry/nextjs');
const { plugins: zgPlugins, config: zgConfig } = require('./zygoat.next.config');

const { webpack: zgWebpackConf } = zgConfig;

zgConfig.webpack = (webpackConfig: unknown, buildInfo: unknown) => {
  const withAliases = zgWebpackConf(webpackConfig, buildInfo);

  return withAliases;
};

const zygoatPlugins = withPlugins(zgPlugins, zgConfig);

module.exports = withSentryConfig(
  zygoatPlugins,
  {
    org: 'willing-n2',
    project: 'sponsors-frontend',
    authToken: process.env.SENTRY_AUTH_TOKEN,
    silent: true, // Suppresses all logs
  },
  {
    // Upload a larger set of source maps for prettier stack traces
    widenClientFileUpload: true,

    // Hides source maps from generated client bundles
    hideSourceMaps: true,

    // Automatically tree-shake Sentry logger statements to reduce bundle size
    disableLogger: true,
  },
);
