// Legacy URL redirects for InfoTerminal UX Redesign
// Automatically redirect old page URLs to new consolidated structure

export const legacyRedirects = [
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

  // Clean URL patterns - Graph tabs
  {
    source: "/graphx/graph",
    destination: "/graphx?tab=graph",
    permanent: false, // Allow both patterns
  },
  {
    source: "/graphx/viz3d",
    destination: "/graphx?tab=viz3d",
    permanent: false,
  },
  {
    source: "/graphx/ml",
    destination: "/graphx?tab=ml",
    permanent: false,
  },

  // Clean URL patterns - NLP domains
  {
    source: "/nlp/general",
    destination: "/nlp?domain=general",
    permanent: false,
  },
  {
    source: "/nlp/legal",
    destination: "/nlp?domain=legal",
    permanent: false,
  },
  {
    source: "/nlp/documents",
    destination: "/nlp?domain=documents",
    permanent: false,
  },
  {
    source: "/nlp/ethics",
    destination: "/nlp?domain=ethics",
    permanent: false,
  },
  {
    source: "/nlp/forensics",
    destination: "/nlp?domain=forensics",
    permanent: false,
  },

  // Clean URL patterns - Agent tabs
  {
    source: "/agent/interaction",
    destination: "/agent?tab=interaction",
    permanent: false,
  },
  {
    source: "/agent/management",
    destination: "/agent?tab=management",
    permanent: false,
  },
];

export default legacyRedirects;
