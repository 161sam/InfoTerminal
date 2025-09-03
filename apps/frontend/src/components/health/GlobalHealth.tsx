import React, { useState } from 'react';
import StatusDot from './StatusDot';
import HealthPopover from './HealthPopover';
import { useHealth } from '../../hooks/useHealth';

export const GlobalHealth: React.FC<{ pollIntervalMs?: number }> = ({ pollIntervalMs = 15000 }) => {
  const { data, error, refresh, stateAggregate } = useHealth(pollIntervalMs);
  const [open, setOpen] = useState(false);

  const aggState = error ? 'unreachable' : stateAggregate;
  const tooltip =
    aggState === 'ok'
      ? 'All systems operational'
      : aggState === 'degraded'
      ? 'Issues detected'
      : 'Issues detected';

  return (
    <div className="relative">
      <button
        aria-label="service-health"
        title={tooltip}
        onClick={() => setOpen((o) => !o)}
        className="flex items-center"
      >
        <StatusDot state={aggState} />
      </button>
      {open && (
        <div className="absolute right-0 mt-2 bg-white shadow-lg rounded z-50">
          <HealthPopover data={data} onRefresh={refresh} />
        </div>
      )}
    </div>
  );
};

export default GlobalHealth;
