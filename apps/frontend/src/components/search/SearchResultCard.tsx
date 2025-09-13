// apps/frontend/src/components/search/SearchResultCard.tsx
import React from 'react';
import Link from 'next/link';
import { Network, ExternalLink, FileText, Calendar, User } from 'lucide-react';
import type { SearchHit } from '@/types/search';
import EntityBadge from '../entities/EntityBadge';
import { normalizeLabel } from '@/lib/entities';

interface SearchResultCardProps {
  item: SearchHit;
}

export default function SearchResultCard({ item }: SearchResultCardProps) {
  return (
    <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
            {item.id ? (
              <Link 
                href={`/documents/${item.id}`}
                className="hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
              >
                {item.title || item.id}
              </Link>
            ) : (
              item.title || item.id
            )}
          </h3>
          
          {/* Snippet with highlights */}
          {item.highlights && item.highlights.length > 0 ? (
            <div className="text-gray-600 dark:text-gray-300 mb-3 line-clamp-3">
              {item.highlights.map((highlight, index) => (
                <p 
                  key={index} 
                  dangerouslySetInnerHTML={{ 
                    __html: highlight.fragments.join(' ... ').replace(/<(?!\/?(em|mark|strong)>)/g, '&lt;')
                  }}
                />
              ))}
            </div>
          ) : item.snippet ? (
            <p className="text-gray-600 dark:text-gray-300 mb-3 line-clamp-3">{item.snippet}</p>
          ) : null}
          
          {/* Entity Types */}
          {item.entity_types && item.entity_types.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-3">
              {item.entity_types.slice(0, 3).map((type, index) => (
                <EntityBadge 
                  key={index}
                  label={normalizeLabel(type)} 
                  size="sm"
                />
              ))}
              {item.entity_types.length > 3 && (
                <span className="text-xs text-gray-500 px-2 py-1 bg-gray-100 rounded-full">
                  +{item.entity_types.length - 3} more
                </span>
              )}
            </div>
          )}

          {/* Additional Entities */}
          {item.meta?.entities && item.meta.entities.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-3">
              {item.meta.entities.slice(0, 5).map((entity: any, index: number) => (
                <EntityBadge
                  key={index}
                  label={normalizeLabel(entity.label)}
                  value={entity.text || entity.value}
                  size="sm"
                />
              ))}
              {item.meta.entities.length > 5 && (
                <span className="text-xs text-gray-500 px-2 py-1 bg-gray-100 rounded-full">
                  +{item.meta.entities.length - 5} entities
                </span>
              )}
            </div>
          )}
          
          {/* Metadata */}
          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
            {item.source && (
              <span className="inline-flex items-center gap-1">
                <FileText size={14} />
                Source: <span className="font-medium">{item.source}</span>
              </span>
            )}
            
            {item.meta?.created_at && (
              <span className="inline-flex items-center gap-1">
                <Calendar size={14} />
                {new Date(item.meta.created_at).toLocaleDateString()}
              </span>
            )}
            
            {item.meta?.author && (
              <span className="inline-flex items-center gap-1">
                <User size={14} />
                {item.meta.author}
              </span>
            )}
            
            {item.score && item.score > 0 && (
              <span className="text-primary-600 dark:text-primary-400">
                Relevance: {(item.score * 100).toFixed(1)}%
              </span>
            )}
          </div>
        </div>
        
        {/* Actions */}
        <div className="ml-4 flex-shrink-0 flex items-center gap-2">
          {item.node_id && (
            <Link
              href={`/graphx?focus=${encodeURIComponent(item.node_id)}`}
              className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-primary-700 dark:text-primary-300 bg-primary-50 dark:bg-primary-900/20 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/30 transition-colors"
              title="View in Graph"
            >
              <Network size={16} />
              Graph
            </Link>
          )}
          
          {item.meta?.external_url && (
            <a
              href={item.meta.external_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              title="Open External Link"
            >
              <ExternalLink size={16} />
            </a>
          )}
        </div>
      </div>
      
      {/* Progress bar for score visualization */}
      {item.score && item.score > 0 && (
        <div className="mt-4">
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5">
            <div 
              className="bg-primary-600 dark:bg-primary-500 h-1.5 rounded-full transition-all duration-500"
              style={{ width: `${Math.min(item.score * 100, 100)}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
