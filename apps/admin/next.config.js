/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ["@leadscan/ui", "@leadscan/shared", "@leadscan/config", "@leadscan/sdk"],
};

module.exports = nextConfig;
