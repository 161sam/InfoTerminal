FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm i --omit=dev
COPY server.js ./
ENV PORT=8080
EXPOSE 8080
CMD ["node", "server.js"]
