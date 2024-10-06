const path = require('path');
const CopyPlugin = require('copy-webpack-plugin');

/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: true,
  // Enabling the experimental Webpack build worker
  experimental: {
    webpackBuildWorker: true,
  },
  webpack: (config) => {
    // Add CopyPlugin to copy images from Leaflet's node_modules to public folder
    config.plugins.push(
      new CopyPlugin({
        patterns: [
          {
            from: 'node_modules/leaflet/dist/images',
            to: path.resolve(__dirname, 'public', 'leaflet', 'images'),
          },
        ],
      })
    );
    return config;
  },
};

module.exports = nextConfig;
