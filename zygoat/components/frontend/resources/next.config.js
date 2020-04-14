const withPlugins = require('next-compose-plugins');

const { plugins, config } = require('./zygoat.next.config');

module.exports = withPlugins(plugins, config);
