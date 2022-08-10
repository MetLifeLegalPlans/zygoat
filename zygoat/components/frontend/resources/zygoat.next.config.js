// This file is automatically generated and updated by Zygoat and should not
// be edited manually. To extend or overwrite these settings, edit
// next.config.js

const withSvgr = require("next-svgr");
const withImages = require("next-images");

const prod = process.env.NODE_ENV === "production";

const headers = [
  { key: "X-FRAME-Options", value: "DENY" },
  { key: "Content-Security-Policy", value: "frame-ancestors 'none'" },
  {
    key: "Strict-Transport-Security",
    value: "max-age=31536000; includeSubDomains",
  },
  { key: "Cache-Control", value: "no-cache, no-store" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-XSS-Protection", value: "1; mode=block" },
];

const buildHeaders =
  (overrideHeaders = []) =>
  async () =>
    [
      {
        source: "/:path*",
        // This file does not get compiled
        // eslint-disable-next-line object-shorthand
        headers: [...headers, ...overrideHeaders],
      },
      {
        source: "/",
        // eslint-disable-next-line object-shorthand
        headers: [...headers, ...overrideHeaders],
      },
    ];

const config = {
  webpack5: true,
  webpack: (webpackConfig, { webpack }) => {
    webpackConfig.resolve.alias["@@"] = __dirname;
    webpackConfig.resolve.alias["@wui"] = "@bequestinc/wui";

    webpackConfig.plugins.push(
      new webpack.ProvidePlugin({
        React: "react",
      })
    );

    return webpackConfig;
  },
  env: {
    PROD: prod,
  },

  headers: buildHeaders(),
  productionBrowserSourceMaps: true,
  poweredByHeader: false,
  swcMinify: true,
  reactStrictMode: true,
};

const withImagesConfig = {
  exclude: /\.svg$/,
};

const plugins = [withSvgr, [withImages, withImagesConfig]];

module.exports = { plugins, config, buildHeaders };
