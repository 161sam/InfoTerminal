# InfoTerminal Frontend - Next.js Application
FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Use monorepo workspace manifests (root-level lockfile)
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
# Ensure workspace layout exists for the frontend package.json
RUN mkdir -p apps/frontend
COPY apps/frontend/package.json apps/frontend/package.json
# Install pnpm
RUN npm install -g pnpm
# Install only the frontend's dependencies using the workspace lockfile
RUN pnpm install --filter @infoterminal/frontend... --frozen-lockfile

# Rebuild the source code only when needed
FROM base AS builder
# Keep monorepo layout during build so prebuild scripts with relative paths work
WORKDIR /app/apps/frontend
# Install bash for prebuild scripts invoked via npm lifecycle
RUN apk add --no-cache bash
COPY --from=deps /app/node_modules /app/node_modules
# Copy only what is needed for building the frontend
COPY apps/frontend/ /app/apps/frontend
# Copy shared scripts referenced by prebuild hooks (../../scripts)
COPY scripts /app/scripts
COPY tools /app/tools

# Environment variables for build
ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV production
ENV DOCKER_BUILD true
ENV NEXT_IGNORE_ESLINT 1
ENV NEXT_IGNORE_TYPECHECK 1

# Build the application
RUN npm install -g pnpm && pnpm build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy public assets
COPY --from=builder /app/apps/frontend/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/apps/frontend/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/apps/frontend/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget -qO- http://localhost:3000/api/health >/dev/null 2>&1 || exit 1
