import React, { useState } from 'react';
import useServiceHealthMatrix from '@/hooks/useServiceHealthMatrix';

const colors: Record<string, string> = {
  ok: 'bg-green-500',
  degraded: 'bg-yellow-500',
  fail: 'bg-red-500',
  unknown: 'bg-gray-400',
};

const ServiceHealthMatrix: React.FC = () => {
  const matrix = useServiceHealthMatrix();
  const [open, setOpen] = useState(false);
  const keys = Object.keys(matrix);
  return (
    <div className="relative" data-testid="svc-health">
      <button className="flex gap-1" onClick={() => setOpen((o) => !o)}>
        {keys.map((k) => (
          <span
            key={k}
            className={`h-3 w-3 rounded-full ${colors[matrix[k].status]}`}
            title={k}
          />
        ))}
      </button>
      {open && (
        <div className="absolute right-0 z-50 mt-2 w-40 rounded p-2 text-xs shadow
                        bg-white dark:bg-gray-900
                        border border-gray-200 dark:border-gray-800
                        text-gray-900 dark:text-gray-100">
          {keys.map((k) => (
            <div key={k} className="flex justify-between">
              <span>{k}</span>
              <span>{matrix[k].status}</span>
              {matrix[k].latency != null && <span>{matrix[k].latency}ms</span>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ServiceHealthMatrix;
