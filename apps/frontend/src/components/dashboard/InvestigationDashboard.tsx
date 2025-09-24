/**
 * Investigation Dashboard
 *
 * Central hub for OSINT investigations with quick actions, recent activities,
 * bookmarked entities, and running analyses.
 */

import React, { useState, useEffect } from "react";
import {
  Search,
  Activity,
  Bookmark,
  Play,
  Clock,
  TrendingUp,
  Users,
  Globe,
  FileText,
  MapPin,
  BarChart3,
  AlertCircle,
  CheckCircle,
  Loader2,
  Plus,
  ArrowRight,
  Eye,
  Download,
  Share2,
} from "lucide-react";
import { motion } from "framer-motion";
import UserJourneyTracker from "@/lib/user-journey-tracker";

interface Investigation {
  id: string;
  name: string;
  type: "person" | "domain" | "social_media" | "document" | "geospatial";
  status: "active" | "completed" | "paused" | "scheduled";
  progress: number;
  createdAt: Date;
  lastUpdated: Date;
  entityCount: number;
  findings: number;
}

interface BookmarkedEntity {
  id: string;
  name: string;
  type: "person" | "organization" | "domain" | "email" | "phone" | "location";
  lastAccessed: Date;
  investigationId?: string;
  riskScore?: number;
  tags: string[];
}

interface QuickAction {
  id: string;
  label: string;
  description: string;
  icon: React.ElementType;
  path: string;
  category: "search" | "analysis" | "tools" | "workflow";
  estimatedTime: string;
}

interface DashboardStats {
  totalInvestigations: number;
  activeInvestigations: number;
  entitiesAnalyzed: number;
  findingsGenerated: number;
  averageInvestigationTime: number;
  successRate: number;
}

const InvestigationDashboard: React.FC = () => {
  const [investigations, setInvestigations] = useState<Investigation[]>([]);
  const [bookmarkedEntities, setBookmarkedEntities] = useState<BookmarkedEntity[]>([]);
  const [dashboardStats, setDashboardStats] = useState<DashboardStats | null>(null);
  const [recentActivities, setRecentActivities] = useState<any[]>([]);
  const [runningAnalyses, setRunningAnalyses] = useState<any[]>([]);
  const [selectedInvestigation, setSelectedInvestigation] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const { trackClick, trackWorkflowStep } = UserJourneyTracker.useUserJourney();

  useEffect(() => {
    loadDashboardData();

    // Set up periodic refresh for running analyses
    const interval = setInterval(loadRunningAnalyses, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      await Promise.all([
        loadInvestigations(),
        loadBookmarkedEntities(),
        loadDashboardStats(),
        loadRecentActivities(),
        loadRunningAnalyses(),
      ]);
    } catch (error) {
      console.error("Failed to load dashboard data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadInvestigations = async () => {
    try {
      const response = await fetch("/api/investigations");
      if (response.ok) {
        const data = await response.json();
        setInvestigations(data.investigations || []);
      }
    } catch (error) {
      console.error("Failed to load investigations:", error);
    }
  };

  const loadBookmarkedEntities = async () => {
    try {
      const response = await fetch("/api/bookmarks/entities");
      if (response.ok) {
        const data = await response.json();
        setBookmarkedEntities(data.entities || []);
      }
    } catch (error) {
      console.error("Failed to load bookmarked entities:", error);
    }
  };

  const loadDashboardStats = async () => {
    try {
      const response = await fetch("/api/dashboard/stats");
      if (response.ok) {
        const data = await response.json();
        setDashboardStats(data.stats);
      }
    } catch (error) {
      console.error("Failed to load dashboard stats:", error);
    }
  };

  const loadRecentActivities = async () => {
    try {
      const response = await fetch("/api/activities/recent?limit=10");
      if (response.ok) {
        const data = await response.json();
        setRecentActivities(data.activities || []);
      }
    } catch (error) {
      console.error("Failed to load recent activities:", error);
    }
  };

  const loadRunningAnalyses = async () => {
    try {
      const response = await fetch("/api/analyses/running");
      if (response.ok) {
        const data = await response.json();
        setRunningAnalyses(data.analyses || []);
      }
    } catch (error) {
      console.error("Failed to load running analyses:", error);
    }
  };

  const quickActions: QuickAction[] = [
    {
      id: "entity_search",
      label: "Entity Search",
      description: "Search for persons, domains, or organizations",
      icon: Search,
      path: "/search",
      category: "search",
      estimatedTime: "2-5 min",
    },
    {
      id: "domain_analysis",
      label: "Domain Analysis",
      description: "Analyze domain infrastructure and security",
      icon: Globe,
      path: "/tools/domain-analysis",
      category: "analysis",
      estimatedTime: "5-10 min",
    },
    {
      id: "social_investigation",
      label: "Social Media Investigation",
      description: "Investigate social media profiles and networks",
      icon: Users,
      path: "/tools/social-media",
      category: "analysis",
      estimatedTime: "10-20 min",
    },
    {
      id: "document_analysis",
      label: "Document Analysis",
      description: "Analyze documents for entities and metadata",
      icon: FileText,
      path: "/tools/document-analysis",
      category: "analysis",
      estimatedTime: "5-15 min",
    },
    {
      id: "geospatial_analysis",
      label: "Geospatial Analysis",
      description: "Verify locations and analyze geographic data",
      icon: MapPin,
      path: "/tools/geospatial",
      category: "analysis",
      estimatedTime: "3-8 min",
    },
    {
      id: "graph_visualization",
      label: "Graph Visualization",
      description: "Visualize entity relationships and networks",
      icon: BarChart3,
      path: "/graph",
      category: "tools",
      estimatedTime: "1-3 min",
    },
    {
      id: "new_investigation",
      label: "New Investigation",
      description: "Start a new structured investigation",
      icon: Plus,
      path: "/investigations/new",
      category: "workflow",
      estimatedTime: "30-120 min",
    },
    {
      id: "bulk_analysis",
      label: "Bulk Analysis",
      description: "Analyze multiple entities simultaneously",
      icon: TrendingUp,
      path: "/tools/bulk-analysis",
      category: "tools",
      estimatedTime: "10-30 min",
    },
  ];

  const handleQuickAction = (action: QuickAction) => {
    trackClick("dashboard-quick-action", {
      actionId: action.id,
      category: action.category,
    });

    // Navigate to action
    window.location.href = action.path;
  };

  const handleInvestigationSelect = (investigationId: string) => {
    setSelectedInvestigation(investigationId);
    trackClick("dashboard-investigation-selected", { investigationId });
  };

  const getStatusIcon = (status: Investigation["status"]) => {
    switch (status) {
      case "active":
        return <Play className="w-4 h-4 text-green-500" />;
      case "completed":
        return <CheckCircle className="w-4 h-4 text-blue-500" />;
      case "paused":
        return <AlertCircle className="w-4 h-4 text-yellow-500" />;
      case "scheduled":
        return <Clock className="w-4 h-4 text-gray-500" />;
      default:
        return <div className="w-4 h-4 bg-gray-300 rounded-full" />;
    }
  };

  const getTypeIcon = (type: Investigation["type"]) => {
    switch (type) {
      case "person":
        return <Users className="w-4 h-4" />;
      case "domain":
        return <Globe className="w-4 h-4" />;
      case "social_media":
        return <Users className="w-4 h-4" />;
      case "document":
        return <FileText className="w-4 h-4" />;
      case "geospatial":
        return <MapPin className="w-4 h-4" />;
      default:
        return <Search className="w-4 h-4" />;
    }
  };

  const getRiskScoreColor = (score?: number) => {
    if (!score) return "text-gray-500";
    if (score >= 8) return "text-red-500";
    if (score >= 6) return "text-yellow-500";
    if (score >= 4) return "text-blue-500";
    return "text-green-500";
  };

  if (isLoading) {
    return (
      <div className="dashboard-loading">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500 mb-4" />
        <p className="text-gray-600">Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="investigation-dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Investigation Dashboard</h1>
          <p className="dashboard-subtitle">
            Central hub for all your OSINT investigations and analyses
          </p>
        </div>

        <div className="header-actions">
          <button className="btn-secondary" onClick={() => trackClick("dashboard-refresh")}>
            <Activity className="w-4 h-4" />
            Refresh
          </button>
          <button
            className="btn-primary"
            onClick={() =>
              handleQuickAction(quickActions.find((a) => a.id === "new_investigation")!)
            }
          >
            <Plus className="w-4 h-4" />
            New Investigation
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      {dashboardStats && (
        <div className="stats-grid">
          <motion.div
            className="stat-card"
            whileHover={{ scale: 1.02 }}
            transition={{ duration: 0.2 }}
          >
            <div className="stat-icon">
              <Activity className="w-6 h-6 text-blue-500" />
            </div>
            <div className="stat-content">
              <div className="stat-value">{dashboardStats.activeInvestigations}</div>
              <div className="stat-label">Active Investigations</div>
            </div>
          </motion.div>

          <motion.div
            className="stat-card"
            whileHover={{ scale: 1.02 }}
            transition={{ duration: 0.2 }}
          >
            <div className="stat-icon">
              <Search className="w-6 h-6 text-green-500" />
            </div>
            <div className="stat-content">
              <div className="stat-value">{dashboardStats.entitiesAnalyzed}</div>
              <div className="stat-label">Entities Analyzed</div>
            </div>
          </motion.div>

          <motion.div
            className="stat-card"
            whileHover={{ scale: 1.02 }}
            transition={{ duration: 0.2 }}
          >
            <div className="stat-icon">
              <TrendingUp className="w-6 h-6 text-purple-500" />
            </div>
            <div className="stat-content">
              <div className="stat-value">{dashboardStats.findingsGenerated}</div>
              <div className="stat-label">Findings Generated</div>
            </div>
          </motion.div>

          <motion.div
            className="stat-card"
            whileHover={{ scale: 1.02 }}
            transition={{ duration: 0.2 }}
          >
            <div className="stat-icon">
              <CheckCircle className="w-6 h-6 text-orange-500" />
            </div>
            <div className="stat-content">
              <div className="stat-value">{Math.round(dashboardStats.successRate)}%</div>
              <div className="stat-label">Success Rate</div>
            </div>
          </motion.div>
        </div>
      )}

      <div className="dashboard-content">
        {/* Quick Actions */}
        <div className="dashboard-section">
          <h2 className="section-title">Quick Actions</h2>
          <div className="quick-actions-grid">
            {quickActions.map((action) => {
              const IconComponent = action.icon;
              return (
                <motion.button
                  key={action.id}
                  className="quick-action-card"
                  onClick={() => handleQuickAction(action)}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <div className="quick-action-icon">
                    <IconComponent className="w-6 h-6" />
                  </div>
                  <div className="quick-action-content">
                    <h3>{action.label}</h3>
                    <p>{action.description}</p>
                    <div className="quick-action-meta">
                      <span className="category-tag">{action.category}</span>
                      <span className="time-estimate">{action.estimatedTime}</span>
                    </div>
                  </div>
                  <ArrowRight className="quick-action-arrow w-5 h-5" />
                </motion.button>
              );
            })}
          </div>
        </div>

        <div className="dashboard-columns">
          {/* Recent Investigations */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2 className="section-title">Recent Investigations</h2>
              <button className="section-action">
                <Eye className="w-4 h-4" />
                View All
              </button>
            </div>

            <div className="investigations-list">
              {investigations.slice(0, 5).map((investigation) => (
                <motion.div
                  key={investigation.id}
                  className={`investigation-item ${selectedInvestigation === investigation.id ? "selected" : ""}`}
                  onClick={() => handleInvestigationSelect(investigation.id)}
                  whileHover={{ backgroundColor: "#f8fafc" }}
                >
                  <div className="investigation-header">
                    <div className="investigation-info">
                      <div className="investigation-type">{getTypeIcon(investigation.type)}</div>
                      <div>
                        <h4 className="investigation-name">{investigation.name}</h4>
                        <p className="investigation-meta">
                          {investigation.entityCount} entities • {investigation.findings} findings
                        </p>
                      </div>
                    </div>
                    <div className="investigation-status">
                      {getStatusIcon(investigation.status)}
                    </div>
                  </div>

                  <div className="investigation-progress">
                    <div className="progress-bar">
                      <div
                        className="progress-fill"
                        style={{ width: `${investigation.progress}%` }}
                      />
                    </div>
                    <span className="progress-text">{investigation.progress}%</span>
                  </div>

                  <div className="investigation-actions">
                    <button className="action-btn">
                      <Play className="w-3 h-3" />
                    </button>
                    <button className="action-btn">
                      <Download className="w-3 h-3" />
                    </button>
                    <button className="action-btn">
                      <Share2 className="w-3 h-3" />
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Bookmarked Entities */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2 className="section-title">Bookmarked Entities</h2>
              <button className="section-action">
                <Bookmark className="w-4 h-4" />
                Manage
              </button>
            </div>

            <div className="entities-list">
              {bookmarkedEntities.slice(0, 6).map((entity) => (
                <div key={entity.id} className="entity-item">
                  <div className="entity-info">
                    <div className="entity-type">{getTypeIcon(entity.type as any)}</div>
                    <div>
                      <h4 className="entity-name">{entity.name}</h4>
                      <p className="entity-meta">{entity.tags.slice(0, 2).join(", ")}</p>
                    </div>
                  </div>

                  {entity.riskScore && (
                    <div className={`risk-score ${getRiskScoreColor(entity.riskScore)}`}>
                      {entity.riskScore}/10
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Running Analyses */}
        {runningAnalyses.length > 0 && (
          <div className="dashboard-section">
            <h2 className="section-title">Running Analyses</h2>
            <div className="running-analyses">
              {runningAnalyses.map((analysis) => (
                <div key={analysis.id} className="analysis-item">
                  <div className="analysis-info">
                    <Loader2 className="w-4 h-4 animate-spin text-blue-500" />
                    <span>{analysis.name}</span>
                  </div>
                  <div className="analysis-progress">
                    <div className="progress-bar-small">
                      <div className="progress-fill" style={{ width: `${analysis.progress}%` }} />
                    </div>
                    <span className="progress-text-small">{analysis.progress}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        .investigation-dashboard {
          padding: 24px;
          max-width: 1400px;
          margin: 0 auto;
        }

        .dashboard-loading {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 400px;
        }

        .dashboard-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 32px;
        }

        .dashboard-title {
          font-size: 32px;
          font-weight: 700;
          color: #1f2937;
          margin: 0 0 8px 0;
        }

        .dashboard-subtitle {
          font-size: 16px;
          color: #6b7280;
          margin: 0;
        }

        .header-actions {
          display: flex;
          gap: 12px;
        }

        .btn-primary {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 10px 16px;
          background: #3b82f6;
          color: white;
          border: none;
          border-radius: 8px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .btn-primary:hover {
          background: #2563eb;
        }

        .btn-secondary {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 10px 16px;
          background: white;
          color: #374151;
          border: 1px solid #d1d5db;
          border-radius: 8px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .btn-secondary:hover {
          background: #f9fafb;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
          gap: 20px;
          margin-bottom: 32px;
        }

        .stat-card {
          background: white;
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          padding: 20px;
          display: flex;
          align-items: center;
          gap: 16px;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .stat-card:hover {
          border-color: #d1d5db;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .stat-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 48px;
          height: 48px;
          background: #f3f4f6;
          border-radius: 10px;
        }

        .stat-value {
          font-size: 24px;
          font-weight: 700;
          color: #1f2937;
          line-height: 1;
        }

        .stat-label {
          font-size: 14px;
          color: #6b7280;
          margin-top: 4px;
        }

        .dashboard-content {
          display: flex;
          flex-direction: column;
          gap: 32px;
        }

        .dashboard-section {
          background: white;
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          padding: 24px;
        }

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
        }

        .section-title {
          font-size: 20px;
          font-weight: 600;
          color: #1f2937;
          margin: 0 0 20px 0;
        }

        .section-action {
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 6px 12px;
          background: #f3f4f6;
          color: #374151;
          border: none;
          border-radius: 6px;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .section-action:hover {
          background: #e5e7eb;
        }

        .quick-actions-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 16px;
        }

        .quick-action-card {
          display: flex;
          align-items: center;
          gap: 16px;
          padding: 16px;
          background: white;
          border: 1px solid #e5e7eb;
          border-radius: 10px;
          text-align: left;
          cursor: pointer;
          transition: all 0.2s ease;
          width: 100%;
        }

        .quick-action-card:hover {
          border-color: #3b82f6;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .quick-action-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          background: #eff6ff;
          border-radius: 8px;
          color: #3b82f6;
          flex-shrink: 0;
        }

        .quick-action-content {
          flex: 1;
          min-width: 0;
        }

        .quick-action-content h3 {
          font-size: 14px;
          font-weight: 600;
          color: #1f2937;
          margin: 0 0 4px 0;
        }

        .quick-action-content p {
          font-size: 12px;
          color: #6b7280;
          margin: 0 0 8px 0;
          line-height: 1.4;
        }

        .quick-action-meta {
          display: flex;
          gap: 8px;
          align-items: center;
        }

        .category-tag {
          font-size: 10px;
          background: #f3f4f6;
          color: #374151;
          padding: 2px 6px;
          border-radius: 4px;
          text-transform: uppercase;
          font-weight: 500;
        }

        .time-estimate {
          font-size: 10px;
          color: #9ca3af;
        }

        .quick-action-arrow {
          color: #9ca3af;
          flex-shrink: 0;
        }

        .dashboard-columns {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 32px;
        }

        .investigations-list,
        .entities-list {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .investigation-item {
          padding: 16px;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .investigation-item:hover {
          border-color: #d1d5db;
        }

        .investigation-item.selected {
          border-color: #3b82f6;
          background: #eff6ff;
        }

        .investigation-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 12px;
        }

        .investigation-info {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .investigation-type {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 32px;
          height: 32px;
          background: #f3f4f6;
          border-radius: 6px;
          color: #6b7280;
        }

        .investigation-name {
          font-size: 14px;
          font-weight: 600;
          color: #1f2937;
          margin: 0;
        }

        .investigation-meta {
          font-size: 12px;
          color: #6b7280;
          margin: 2px 0 0 0;
        }

        .investigation-progress {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 12px;
        }

        .progress-bar {
          flex: 1;
          height: 6px;
          background: #e5e7eb;
          border-radius: 3px;
          overflow: hidden;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #3b82f6, #1d4ed8);
          transition: width 0.3s ease;
        }

        .progress-text {
          font-size: 12px;
          color: #6b7280;
          font-weight: 500;
        }

        .investigation-actions {
          display: flex;
          gap: 8px;
        }

        .action-btn {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 28px;
          height: 28px;
          background: #f3f4f6;
          border: none;
          border-radius: 4px;
          color: #6b7280;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .action-btn:hover {
          background: #e5e7eb;
          color: #374151;
        }

        .entity-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 12px;
          border: 1px solid #e5e7eb;
          border-radius: 6px;
        }

        .entity-info {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .entity-type {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 28px;
          height: 28px;
          background: #f3f4f6;
          border-radius: 4px;
          color: #6b7280;
        }

        .entity-name {
          font-size: 14px;
          font-weight: 500;
          color: #1f2937;
          margin: 0;
        }

        .entity-meta {
          font-size: 12px;
          color: #6b7280;
          margin: 2px 0 0 0;
        }

        .risk-score {
          font-size: 12px;
          font-weight: 600;
          padding: 4px 8px;
          background: #f3f4f6;
          border-radius: 4px;
        }

        .running-analyses {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .analysis-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 12px;
          background: #f8fafc;
          border-radius: 6px;
        }

        .analysis-info {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 14px;
          color: #374151;
        }

        .analysis-progress {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .progress-bar-small {
          width: 80px;
          height: 4px;
          background: #e5e7eb;
          border-radius: 2px;
          overflow: hidden;
        }

        .progress-text-small {
          font-size: 11px;
          color: #6b7280;
          font-weight: 500;
        }

        /* Responsive */
        @media (max-width: 1024px) {
          .dashboard-columns {
            grid-template-columns: 1fr;
          }

          .quick-actions-grid {
            grid-template-columns: 1fr;
          }
        }

        @media (max-width: 768px) {
          .investigation-dashboard {
            padding: 16px;
          }

          .dashboard-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 16px;
          }

          .stats-grid {
            grid-template-columns: 1fr;
            gap: 12px;
          }

          .quick-action-card {
            padding: 12px;
          }
        }
      `}</style>
    </div>
  );
};

export default InvestigationDashboard;
