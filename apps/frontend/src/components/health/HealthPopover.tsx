import React from 'react';
import ServiceHealthCard from './ServiceHealthCard';
import type { HealthResponse } from '../../../pages/api/health';
import config from '@/lib/config';

interface Props {
  data: HealthResponse | null;
  onRefresh: () => void;
}

export const HealthPopover: React.FC<Props> = ({ data, onRefresh }) => {
  const services = data?.services;
  return (
    <div className="p-4 w-64">
      <div className="grid grid-cols-1 gap-2">
        {services && (
          <>
            <ServiceHealthCard name="search" state={services.search.state} latencyMs={services.search.latencyMs} />
            <ServiceHealthCard name="graph" state={services.graph.state} latencyMs={services.graph.latencyMs} />
            <ServiceHealthCard name="docentities" state={services.docentities.state} latencyMs={services.docentities.latencyMs} />
            <ServiceHealthCard name="nlp" state={services.nlp.state} latencyMs={services.nlp.latencyMs} />
          </>
        )}
      </div>
      <div className="mt-4 flex justify-end gap-4 text-sm">
        {(config as any).GRAFANA_URL && (
          <a
            href={(config as any).GRAFANA_URL}
            target="_blank"
            rel="noreferrer"
            className="text-blue-600"
          >
            Open Grafana
          </a>
        )}
        <button onClick={onRefresh} className="underline">
          Force refresh
        </button>
      </div>
    </div>
  );
};

export default HealthPopover;
