import { Calendar, Star, FileText, ExternalLink, Eye } from "lucide-react";
import Panel from "@/components/layout/Panel";
import { SearchResult, getResultTypeIcon } from "@/lib/search/search-config";

interface SearchResultCardProps {
  result: SearchResult;
}

export default function SearchResultCard({ result }: SearchResultCardProps) {
  const Icon = getResultTypeIcon(result.type || "other");

  return (
    <Panel className="hover:shadow-md transition-shadow">
      <div className="flex items-start gap-4">
        <div className="p-2 bg-gray-100 dark:bg-gray-800 rounded-lg">
          <Icon size={20} className="text-gray-600 dark:text-slate-400" />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h3 className="font-semibold text-gray-900 dark:text-slate-100 mb-1">
                {result.title || result.id}
              </h3>

              {result.snippet && (
                <p className="text-gray-600 dark:text-slate-400 text-sm mb-2 leading-relaxed">
                  {result.snippet}
                </p>
              )}

              <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-slate-400">
                {result.score !== undefined && (
                  <div className="flex items-center gap-1">
                    <Star size={12} />
                    Score: {result.score.toFixed(2)}
                  </div>
                )}
                {result.date && (
                  <div className="flex items-center gap-1">
                    <Calendar size={12} />
                    {new Date(result.date).toLocaleDateString()}
                  </div>
                )}
                {result.source && (
                  <div className="flex items-center gap-1">
                    <FileText size={12} />
                    {result.source}
                  </div>
                )}
              </div>

              {result.entities && result.entities.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {result.entities.slice(0, 3).map((entity, index) => (
                    <span
                      key={index}
                      className="inline-block px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full"
                    >
                      {entity}
                    </span>
                  ))}
                  {result.entities.length > 3 && (
                    <span className="inline-block px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full">
                      +{result.entities.length - 3} more
                    </span>
                  )}
                </div>
              )}
            </div>

            <div className="flex items-center gap-2">
              <button className="p-1 text-gray-400 hover:text-gray-600 rounded">
                <Eye size={16} />
              </button>
              {result.url && (
                <button className="p-1 text-gray-400 hover:text-gray-600 rounded">
                  <ExternalLink size={16} />
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </Panel>
  );
}
