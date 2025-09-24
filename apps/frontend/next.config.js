const legacyRedirects = require("./lib/redirects.ts").legacyRedirects;

const GATEWAY =
  process.env.NEXT_PROXY_GATEWAY ||
  (process.env.IT_PORT_GATEWAY
    ? `http://localhost:${process.env.IT_PORT_GATEWAY}`
    : "http://localhost:8610");
const DOCENTS =
  process.env.NEXT_PROXY_DOC_ENTITIES ||
  (process.env.IT_PORT_DOC_ENTITIES
    ? `http://localhost:${process.env.IT_PORT_DOC_ENTITIES}`
    : "http://localhost:8613");
const PLUGINS =
  process.env.NEXT_PROXY_PLUGINS ||
  (process.env.IT_PORT_GATEWAY
    ? `http://localhost:${process.env.IT_PORT_GATEWAY}`
    : "http://localhost:8610");

const withExistingRewrites = (rewrites = []) => {
  const add = (arr, item) => (arr.some((r) => r.source === item.source) ? arr : [...arr, item]);
  let out = Array.isArray(rewrites) ? rewrites : [];
  out = add(out, { source: "/api/agent/:path*", destination: `${GATEWAY}/:path*` });
  out = add(out, {
    source: "/api/doc-entities/:path*",
    destination: `${DOCENTS}/:path*`,
  });
  out = add(out, {
    source: "/api/plugins/:path*",
    destination: `${PLUGINS}/plugins/:path*`,
  });
  out = add(out, {
    source: "/api/ops/:path*",
    destination: `${GATEWAY}/ops/:path*`,
  });
  return out;
};

// Detect if 'critters' is available to safely enable optimizeCss
const hasCritters = (() => {
  try {
    require.resolve("critters");
    return true;
  } catch (_) {
    return false;
  }
})();

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
  // Enable Next.js standalone output for slimmer Docker images
  output: "standalone",

  // Build optimizations
  compiler: {
    // Remove console.log in production builds
    removeConsole: process.env.NODE_ENV === "production",
  },

  // Performance optimizations
  experimental: {
    // Enable modern bundling
    esmExternals: true,
    // Optimize CSS only when 'critters' is present and in production
    // This avoids dev crashes like "Cannot find module 'critters'" with pnpm
    optimizeCss: process.env.NODE_ENV === "production" && hasCritters,
    // Enable SWC minification
    swcMinify: true,
  },

  // Image optimization
  images: {
    formats: ["image/webp", "image/avif"],
    dangerouslyAllowSVG: true,
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
  },

  // Legacy URL Redirects for UX Redesign
  async redirects() {
    return [
      // Agent pages consolidation
      {
        source: "/agents",
        destination: "/agent?tab=management",
        permanent: true,
      },
      {
        source: "/agents/:path*",
        destination: "/agent/management/:path*",
        permanent: true,
      },

      // NLP domain consolidation - Legal
      {
        source: "/legal",
        destination: "/nlp?domain=legal",
        permanent: true,
      },
      {
        source: "/legal/:path*",
        destination: "/nlp/legal/:path*",
        permanent: true,
      },

      // NLP domain consolidation - Documents
      {
        source: "/documents",
        destination: "/nlp?domain=documents",
        permanent: true,
      },
      {
        source: "/documents/:path*",
        destination: "/nlp/documents/:path*",
        permanent: true,
      },

      // NLP domain consolidation - Ethics
      {
        source: "/ethics",
        destination: "/nlp?domain=ethics",
        permanent: true,
      },
      {
        source: "/ethics/:path*",
        destination: "/nlp/ethics/:path*",
        permanent: true,
      },

      // NLP domain consolidation - Forensics
      {
        source: "/forensics",
        destination: "/nlp?domain=forensics",
        permanent: true,
      },
      {
        source: "/forensics/:path*",
        destination: "/nlp/forensics/:path*",
        permanent: true,
      },

      // Graph pages consolidation - ML Analytics
      {
        source: "/graph-ml",
        destination: "/graphx?tab=ml",
        permanent: true,
      },
      {
        source: "/graph-ml/:path*",
        destination: "/graphx/ml/:path*",
        permanent: true,
      },

      // Graph pages consolidation - 3D Visualization
      {
        source: "/viz3d",
        destination: "/graphx?tab=viz3d",
        permanent: true,
      },
      {
        source: "/viz3d/:path*",
        destination: "/graphx/viz3d/:path*",
        permanent: true,
      },
    ];
  },

  // Headers for security and performance
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "X-Frame-Options",
            value: "DENY",
          },
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "Referrer-Policy",
            value: "strict-origin-when-cross-origin",
          },
        ],
      },
    ];
  },

  // Enable webpack optimizations
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Production optimizations
    if (!dev) {
      config.optimization.splitChunks = {
        chunks: "all",
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: "vendors",
            chunks: "all",
          },
        },
      };
    }

    return config;
  },

  // ESLint configuration - Enable for build quality
  eslint: {
    // Only skip ESLint in CI/Docker if absolutely necessary
    ignoreDuringBuilds: process.env.CI === "true" || process.env.DOCKER_BUILD === "true",
    // Specify directories to lint
    dirs: ["pages", "src"],
  },

  // TypeScript configuration
  typescript: {
    // Enable type checking during builds (recommended for production)
    ignoreBuildErrors: false,
  },

  // Environment variables
  env: {
    NEXT_TELEMETRY_DISABLED: "1",
  },
};

const originalRewrites = config.rewrites;
config.rewrites = async function rewrites() {
  const existing = typeof originalRewrites === "function" ? await originalRewrites.call(this) : [];
  const flat = Array.isArray(existing)
    ? existing
    : [
        ...(existing.beforeFiles || []),
        ...(existing.afterFiles || []),
        ...(existing.fallback || []),
      ];
  return withExistingRewrites(flat);
};

module.exports = config;
