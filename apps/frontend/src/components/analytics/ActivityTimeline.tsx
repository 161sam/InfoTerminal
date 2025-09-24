// Activity timeline component for OSINT events
import React, { useState } from "react";
import { Clock, Filter, Search, FileText, Users, Link, MapPin, Calendar } from "lucide-react";
import { useTimeline } from "../../hooks/analytics";
import { AnalyticsFilters, TimelineEvent } from "./types";

interface ActivityTimelineProps {
  filters: AnalyticsFilters;
  onEventClick?: (event: TimelineEvent) => void;
  className?: string;
}

export function ActivityTimeline({ filters, onEventClick, className = "" }: ActivityTimelineProps) {
  const { data, loading, error } = useTimeline(filters);
  const [selectedType, setSelectedType] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState("");

  if (loading) {
    return (
      <div
        className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}
      >
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="space-y-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="flex gap-4">
                <div className="w-12 h-12 bg-gray-200 dark:bg-gray-700 rounded"></div>
                <div className="flex-1">
                  <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                  <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div
        className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}
      >
        <div className="flex items-center gap-2 text-red-600 dark:text-red-400">
          <Clock size={20} />
          <span className="text-sm">Timeline service unavailable. Showing empty state.</span>
        </div>
      </div>
    );
  }

  const getEventIcon = (type: TimelineEvent["type"]) => {
    switch (type) {
      case "document":
        return <FileText size={16} />;
      case "entity":
        return <Users size={16} />;
      case "claim":
        return <Search size={16} />;
      case "relationship":
        return <Link size={16} />;
      default:
        return <Clock size={16} />;
    }
  };

  const getEventColor = (type: TimelineEvent["type"]) => {
    switch (type) {
      case "document":
        return "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300";
      case "entity":
        return "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300";
      case "claim":
        return "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300";
      case "relationship":
        return "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300";
      default:
        return "bg-gray-100 text-gray-700 dark:bg-gray-900/30 dark:text-gray-300";
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return "text-green-600 dark:text-green-400";
    if (confidence >= 0.6) return "text-yellow-600 dark:text-yellow-400";
    return "text-red-600 dark:text-red-400";
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);

    if (diffInHours < 24) {
      return `${Math.floor(diffInHours)}h ago`;
    } else if (diffInHours < 24 * 7) {
      return `${Math.floor(diffInHours / 24)}d ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  const filteredEvents =
    data?.events.filter((event) => {
      const matchesType = selectedType === "all" || event.type === selectedType;
      const matchesSearch =
        !searchQuery ||
        event.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        event.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        event.entities.some((entity) => entity.toLowerCase().includes(searchQuery.toLowerCase()));

      return matchesType && matchesSearch;
    }) || [];

  const eventTypes = data?.events
    ? [...new Set(data.events.map((event) => event.type))].sort()
    : [];

  return (
    <div
      className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}
    >
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Clock size={20} className="text-purple-600" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Activity Timeline
          </h3>
        </div>

        {data?.summary && (
          <div className="text-xs text-gray-500 dark:text-gray-400">
            {data.summary.totalEvents} events • {data.summary.timeSpan}
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <div className="flex-1">
          <div className="relative">
            <Search
              size={16}
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
            />
            <input
              type="text"
              placeholder="Search events..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-purple-500"
            />
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Filter size={16} className="text-gray-400" />
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-purple-500"
          >
            <option value="all">All Types</option>
            {eventTypes.map((type) => (
              <option key={type} value={type}>
                {type.charAt(0).toUpperCase() + type.slice(1)}s
              </option>
            ))}
          </select>
        </div>
      </div>

      {!data || filteredEvents.length === 0 ? (
        <div className="text-center py-12">
          <Clock size={48} className="mx-auto mb-4 text-gray-400" />
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            {searchQuery || selectedType !== "all"
              ? "No events match the current filters."
              : "No timeline events available for the selected period."}
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Summary Stats */}
          {data.summary.categories && Object.keys(data.summary.categories).length > 0 && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(data.summary.categories).map(([category, count]) => (
                <div
                  key={category}
                  className="text-center p-3 bg-gray-50 dark:bg-gray-900/50 rounded-lg"
                >
                  <div className="text-lg font-bold text-gray-900 dark:text-gray-100">{count}</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400 capitalize">
                    {category}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Timeline */}
          <div className="relative">
            {/* Timeline line */}
            <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gray-200 dark:bg-gray-700"></div>

            <div className="space-y-6">
              {filteredEvents.map((event, index) => (
                <div
                  key={event.id}
                  className="relative flex gap-4 cursor-pointer group"
                  onClick={() => onEventClick?.(event)}
                >
                  {/* Timeline marker */}
                  <div
                    className={`relative z-10 flex items-center justify-center w-12 h-12 rounded-full ${getEventColor(event.type)} group-hover:ring-4 group-hover:ring-opacity-20 transition-all`}
                  >
                    {getEventIcon(event.type)}
                  </div>

                  {/* Event content */}
                  <div className="flex-1 min-w-0 pb-6">
                    <div className="bg-gray-50 dark:bg-gray-900/50 rounded-lg p-4 group-hover:bg-gray-100 dark:group-hover:bg-gray-900/70 transition-colors">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                          {event.title}
                        </h4>
                        <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                          <Calendar size={12} />
                          {formatTimestamp(event.timestamp)}
                        </div>
                      </div>

                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
                        {event.description}
                      </p>

                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          {/* Entities */}
                          {event.entities.length > 0 && (
                            <div className="flex items-center gap-1">
                              <Users size={12} className="text-gray-400" />
                              <span className="text-xs text-gray-600 dark:text-gray-400">
                                {event.entities.length} entities
                              </span>
                            </div>
                          )}

                          {/* Source */}
                          <div className="flex items-center gap-1">
                            <MapPin size={12} className="text-gray-400" />
                            <span className="text-xs text-gray-600 dark:text-gray-400">
                              {event.source}
                            </span>
                          </div>
                        </div>

                        {/* Confidence */}
                        <div className="flex items-center gap-1">
                          <span
                            className={`text-xs font-medium ${getConfidenceColor(event.confidence)}`}
                          >
                            {Math.round(event.confidence * 100)}%
                          </span>
                        </div>
                      </div>

                      {/* Entities tags */}
                      {event.entities.length > 0 && (
                        <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                          <div className="flex flex-wrap gap-1">
                            {event.entities.slice(0, 3).map((entity, idx) => (
                              <span
                                key={idx}
                                className="inline-block px-2 py-1 text-xs bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded"
                              >
                                {entity}
                              </span>
                            ))}
                            {event.entities.length > 3 && (
                              <span className="text-xs text-gray-500 dark:text-gray-400 py-1">
                                +{event.entities.length - 3} more
                              </span>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Clusters */}
          {data.clusters.length > 0 && (
            <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
              <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-4">
                Event Clusters
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {data.clusters.map((cluster) => (
                  <div
                    key={cluster.id}
                    className="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                        {cluster.label}
                      </span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {cluster.events.length} events
                      </span>
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">
                      {new Date(cluster.timeRange.start).toLocaleDateString()} -{" "}
                      {new Date(cluster.timeRange.end).toLocaleDateString()}
                    </div>
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-purple-500 h-2 rounded-full"
                          style={{ width: `${cluster.significance * 100}%` }}
                        />
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                        Significance: {Math.round(cluster.significance * 100)}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ActivityTimeline;
