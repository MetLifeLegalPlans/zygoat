const withPlugins = require('next-compose-plugins');

const { plugins, config } = require('./zygoat.next.config');

const contentSecurityPolicy = {
  key: 'Content-Security-Policy',
  value:
    "default-src 'self' https://static.zdassets.com/ekr/snippet.js https://www.google-analytics.com/analytics.js https://cdnjs.cloudflare.com https://hello.myfonts.net https://ekr.zendesk.com https://widget-mediator.zopim.com https://willing.zendesk.com https://www.google-analytics.com https://v2assets.zopim.io http://hello.myfonts.net/count/36e46e https://static.zdassets.com 'unsafe-eval' 'unsafe-inline'",
};

const extendedConfig = {
  ...config,
  headers: config.headers(contentSecurityPolicy),
};

module.exports = withPlugins(plugins, extendedConfig);
