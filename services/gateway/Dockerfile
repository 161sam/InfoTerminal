FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev && npm install ts-node typescript
COPY . .
ENV PORT=8080
EXPOSE 8080
CMD ["node", "server.js"]
