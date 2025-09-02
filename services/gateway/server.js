const express = require('express');
const client = require('prom-client');

const register = new client.Registry();
client.collectDefaultMetrics({ register });

const app = express();
app.get('/metrics', async (_, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.get('/healthz', (_, res) => res.json({ ok: true }));

const port = process.env.PORT || 8080;
app.listen(port, () => console.log(`gateway listening on ${port}`));
