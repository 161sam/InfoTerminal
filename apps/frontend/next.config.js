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
  const add = (arr, item) =>
    arr.some((r) => r.source === item.source) ? arr : [...arr, item];
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

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
  eslint: {
    // Skip ESLint during builds to avoid requiring eslint in CI/containers
    ignoreDuringBuilds: true,
  },
};

const originalRewrites = config.rewrites;
config.rewrites = async function rewrites() {
  const existing =
    typeof originalRewrites === "function"
      ? await originalRewrites.call(this)
      : [];
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
