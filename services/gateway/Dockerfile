FROM node:20-alpine

# Create app directory
WORKDIR /app

# Install production deps and runtime TS tools
COPY services/gateway/package.json ./package.json
RUN npm install --omit=dev \
 && npm install --no-save ts-node typescript

# Copy application sources
COPY services/gateway/index.ts ./index.ts
COPY services/gateway/server.js ./server.js
COPY services/gateway/obs ./obs
COPY services/gateway/app ./app

# Drop privileges to default non-root user
USER node

ENV PORT=8080
EXPOSE 8080

CMD ["node", "server.js"]
