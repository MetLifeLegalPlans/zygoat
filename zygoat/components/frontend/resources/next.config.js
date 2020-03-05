const prod = process.env.NODE_ENV === 'production';

module.exports = {
  webpack: config => {
    config.resolve.alias['@@'] = __dirname;
    config.resolve.alias['@wui'] = '@bequestinc/wui';
    return config;
  },
  env: {
    PROD: prod,
    BACKEND_URL: prod ? process.env.BACKEND_URL : 'http://backend:3001',
  },
};
