import React, { useState } from 'react';
import StatusDot, { ServiceState } from './StatusDot';
import HealthPopover from './HealthPopover';
import { useHealth } from '@/hooks/useHealth';

export const GlobalHealth: React.FC<{ pollIntervalMs?: number }> = ({ pollIntervalMs = 15000 }) => {
  const { data, error, refresh, stateAggregate } = useHealth(pollIntervalMs);
  const [open, setOpen] = useState(false);

  const aggState: ServiceState = error ? 'unreachable' : (stateAggregate as ServiceState);
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
        <div className="absolute right-0 mt-2 rounded z-50 shadow-lg
                        bg-white dark:bg-gray-900
                        border border-gray-200 dark:border-gray-800
                        text-gray-900 dark:text-gray-100">
          <HealthPopover data={data} onRefresh={refresh} />
        </div>
      )}
    </div>
  );
};

export default GlobalHealth;
