import type { NextConfig } from "next";

// Get R2 public URL from environment if available
const R2_PUBLIC_URL = process.env.NEXT_PUBLIC_R2_PUBLIC_URL;

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      // Placeholder service (demo images)
      { protocol: 'https', hostname: 'placehold.co' },
      // Local backend (development)
      { protocol: 'http', hostname: 'localhost', port: '8000' },
      { protocol: 'http', hostname: '127.0.0.1', port: '8000' },
      // Allow https on localhost too, just in case
      { protocol: 'https', hostname: 'localhost', port: '8000' },
      { protocol: 'https', hostname: '127.0.0.1', port: '8000' },
      // Cloudflare R2 storage - allow R2 public domains
      // Pattern matches subdomains like pub-{account_id}.r2.dev
      { protocol: 'https', hostname: '*.r2.dev' },
      // If R2_PUBLIC_URL is set, extract and add the specific domain
      ...(R2_PUBLIC_URL ? (() => {
        try {
          const url = new URL(R2_PUBLIC_URL);
          return [{ protocol: 'https' as const, hostname: url.hostname }];
        } catch {
          return [];
        }
      })() : []),
    ],
    // Increase image sizes if needed
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
};

module.exports = nextConfig;
