import React from 'react';
import { Filter } from 'lucide-react';
import Panel from '@/components/layout/Panel';
import { Domain, DomainConfig, DOMAIN_COLORS } from './types';

interface NLPDomainSelectorProps {
  domains: DomainConfig[];
  activeDomain: Domain;
  onDomainChange: (domain: Domain) => void;
}

export default function NLPDomainSelector({ 
  domains, 
  activeDomain, 
  onDomainChange 
}: NLPDomainSelectorProps) {
  const currentDomain = domains.find(d => d.id === activeDomain);

  return (
    <Panel title="Analysis Domain">
      <div className="space-y-4">
        <div className="flex items-center gap-2 mb-4">
          <Filter size={16} className="text-gray-500" />
          <span className="text-sm font-medium text-gray-700 dark:text-slate-300">
            Select domain for specialized analysis:
          </span>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {domains.map((domain) => (
            <button
              key={domain.id}
              onClick={() => onDomainChange(domain.id)}
              className={`p-4 rounded-lg border transition-colors text-left ${
                activeDomain === domain.id
                  ? DOMAIN_COLORS[domain.color as keyof typeof DOMAIN_COLORS]
                  : 'border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800'
              }`}
            >
              <div className="flex items-center gap-3 mb-2">
                <domain.icon size={20} />
                <span className="font-medium">{domain.name}</span>
              </div>
              <p className="text-xs opacity-75">{domain.description}</p>
            </button>
          ))}
        </div>

        {currentDomain && (
          <div className={`p-3 rounded-lg border ${DOMAIN_COLORS[currentDomain.color as keyof typeof DOMAIN_COLORS]}`}>
            <div className="flex items-center gap-2">
              <currentDomain.icon size={16} />
              <span className="font-medium">Active Domain: {currentDomain.name}</span>
            </div>
            <p className="text-sm mt-1 opacity-75">{currentDomain.description}</p>
          </div>
        )}
      </div>
    </Panel>
  );
}
