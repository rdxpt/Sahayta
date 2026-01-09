/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  webpack: (config) => {
    config.externals.push({
      'utf-8-validate': 'commonjs2 utf-8-validate',
      'bufferutil': 'commonjs2 bufferutil',
    });
    return config;
  },
};

module.exports = nextConfig;
