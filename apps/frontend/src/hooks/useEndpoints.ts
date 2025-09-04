import { useEffect, useState } from 'react';
import { getEndpoints } from '../../../lib/endpoints';

export function useEndpoints() {
  const [eps, setEps] = useState(getEndpoints());
  useEffect(() => {
    const handler = () => setEps(getEndpoints());
    window.addEventListener('it-gateway-change', handler);
    window.addEventListener('storage', handler);
    return () => {
      window.removeEventListener('it-gateway-change', handler);
      window.removeEventListener('storage', handler);
    };
  }, []);
  return eps;
}

export default useEndpoints;
