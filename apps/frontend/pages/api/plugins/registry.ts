import type { NextApiRequest, NextApiResponse } from 'next';

type PluginRegItem = {
  name: string;
  version?: string;
  provider?: string;
  description?: string;
  category?: string;
  endpoints?: { baseUrl?: string };
  icon?: string;
};

function envInt(name: string, def: number): number {
  const v = process.env[name];
  if (!v) return def;
  const n = parseInt(v, 10);
  return Number.isFinite(n) ? n : def;
}

function buildIntegrations(): PluginRegItem[] {
  const alephPort = envInt('IT_PORT_ALEPH', 8641);
  const supersetPort = envInt('IT_PORT_SUPERSET', 8644);
  const nifiPort = envInt('IT_PORT_NIFI', 8619);
  const airflowPort = envInt('IT_PORT_AIRFLOW', 8642);

  return [
    {
      name: 'aleph',
      version: 'latest',
      provider: 'AlephData',
      description: 'Open-source investigations and document analysis',
      category: 'integration',
      endpoints: { baseUrl: `http://localhost:${alephPort}` },
    },
    {
      name: 'superset',
      version: 'latest',
      provider: 'Apache',
      description: 'Business Intelligence dashboards and exploration',
      category: 'integration',
      endpoints: { baseUrl: `http://localhost:${supersetPort}` },
    },
    {
      name: 'nifi',
      version: '2.x',
      provider: 'Apache',
      description: 'Dataflow orchestration for batch and streaming ingest',
      category: 'integration',
      endpoints: { baseUrl: `http://localhost:${nifiPort}/nifi` },
    },
    {
      name: 'airflow',
      version: '2.x',
      provider: 'Apache',
      description: 'Workflow orchestration for ETL and scheduling',
      category: 'integration',
      endpoints: { baseUrl: `http://localhost:${airflowPort}` },
    },
  ];
}

export default async function handler(_req: NextApiRequest, res: NextApiResponse) {
  // For now this registry lists the standard integrations. In future we can merge
  // with plugin-runner registry for tool-based plugins.
  const items = buildIntegrations();
  res.status(200).json({ items, total: items.length });
}

