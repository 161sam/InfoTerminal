import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import {
  Shield,
  Search,
  Scale,
  Target,
  Activity,
  CheckCircle,
  AlertTriangle,
  TrendingUp,
  Database,
  Clock,
  Users,
  FileText,
  ExternalLink,
} from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";

interface VerificationMetrics {
  totalVerifications: number;
  activeInvestigations: number;
  credibilityChecks: number;
  sourceAnalysis: number;
  avgCredibilityScore: number;
  recentActivity: Array<{
    id: string;
    type: "claim" | "evidence" | "stance" | "credibility";
    description: string;
    timestamp: string;
    confidence?: number;
    status: "completed" | "in-progress" | "failed";
  }>;
}

export default function VerificationDashboard() {
  const router = useRouter();
  const [metrics, setMetrics] = useState<VerificationMetrics>({
    totalVerifications: 0,
    activeInvestigations: 0,
    credibilityChecks: 0,
    sourceAnalysis: 0,
    avgCredibilityScore: 0,
    recentActivity: [],
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadMetrics();
  }, []);

  const loadMetrics = async () => {
    setIsLoading(true);
    try {
      // Mock data for demonstration - would be replaced with actual API calls
      const mockMetrics: VerificationMetrics = {
        totalVerifications: 156,
        activeInvestigations: 8,
        credibilityChecks: 42,
        sourceAnalysis: 89,
        avgCredibilityScore: 0.73,
        recentActivity: [
          {
            id: "1",
            type: "credibility",
            description: "Assessed credibility of Reuters article on climate change",
            timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
            confidence: 0.92,
            status: "completed",
          },
          {
            id: "2",
            type: "stance",
            description: "Classified evidence stance for economic policy claim",
            timestamp: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
            confidence: 0.78,
            status: "completed",
          },
          {
            id: "3",
            type: "evidence",
            description: "Retrieved 5 sources for healthcare reform statement",
            timestamp: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
            status: "completed",
          },
          {
            id: "4",
            type: "claim",
            description: "Extracted 3 verifiable claims from news article",
            timestamp: new Date(Date.now() - 1000 * 60 * 180).toISOString(),
            status: "completed",
          },
          {
            id: "5",
            type: "credibility",
            description: "Analysis of social media source reliability",
            timestamp: new Date(Date.now() - 1000 * 60 * 240).toISOString(),
            confidence: 0.34,
            status: "in-progress",
          },
        ],
      };

      setTimeout(() => {
        setMetrics(mockMetrics);
        setIsLoading(false);
      }, 1000);
    } catch (error) {
      console.error("Failed to load verification metrics:", error);
      setIsLoading(false);
    }
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case "claim":
        return <Search className="h-4 w-4 text-blue-500" />;
      case "evidence":
        return <Target className="h-4 w-4 text-green-500" />;
      case "stance":
        return <Scale className="h-4 w-4 text-purple-500" />;
      case "credibility":
        return <Shield className="h-4 w-4 text-orange-500" />;
      default:
        return <Activity className="h-4 w-4 text-gray-500" />;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case "in-progress":
        return <Clock className="h-4 w-4 text-yellow-500" />;
      case "failed":
        return <AlertTriangle className="h-4 w-4 text-red-500" />;
      default:
        return <Activity className="h-4 w-4 text-gray-500" />;
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));

    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
    return date.toLocaleDateString();
  };

  return (
    <DashboardLayout
      title="Verification Dashboard"
      subtitle="Overview of fact-checking and verification activities"
    >
      <div className="p-6">
        <div className="max-w-7xl space-y-6">
          {/* Header Actions */}
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold">Verification Center</h1>
              <p className="text-gray-600">Real-time fact-checking and claim verification</p>
            </div>
            <div className="flex gap-3">
              <Button variant="outline" onClick={() => router.push("/verification")}>
                <Activity className="h-4 w-4 mr-2" />
                Full Verification Tools
              </Button>
              <Button onClick={() => window.open("http://localhost:8618/nifi", "_blank")}>
                <Database className="h-4 w-4 mr-2" />
                NiFi Orchestration
              </Button>
            </div>
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Verifications</p>
                    <p className="text-3xl font-bold text-blue-600">{metrics.totalVerifications}</p>
                  </div>
                  <div className="p-3 bg-blue-100 rounded-full">
                    <Activity className="h-6 w-6 text-blue-600" />
                  </div>
                </div>
                <div className="flex items-center mt-4 text-sm">
                  <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                  <span className="text-green-600">+12% from last week</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Active Investigations</p>
                    <p className="text-3xl font-bold text-green-600">
                      {metrics.activeInvestigations}
                    </p>
                  </div>
                  <div className="p-3 bg-green-100 rounded-full">
                    <Search className="h-6 w-6 text-green-600" />
                  </div>
                </div>
                <div className="flex items-center mt-4 text-sm">
                  <Users className="h-4 w-4 text-blue-500 mr-1" />
                  <span className="text-gray-600">3 analysts working</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Credibility Checks</p>
                    <p className="text-3xl font-bold text-orange-600">
                      {metrics.credibilityChecks}
                    </p>
                  </div>
                  <div className="p-3 bg-orange-100 rounded-full">
                    <Shield className="h-6 w-6 text-orange-600" />
                  </div>
                </div>
                <div className="flex items-center mt-4 text-sm">
                  <div className="w-full">
                    <div className="flex justify-between text-xs mb-1">
                      <span>Avg Score</span>
                      <span>{(metrics.avgCredibilityScore * 100).toFixed(0)}%</span>
                    </div>
                    <Progress value={metrics.avgCredibilityScore * 100} className="h-1" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Source Analysis</p>
                    <p className="text-3xl font-bold text-purple-600">{metrics.sourceAnalysis}</p>
                  </div>
                  <div className="p-3 bg-purple-100 rounded-full">
                    <Target className="h-6 w-6 text-purple-600" />
                  </div>
                </div>
                <div className="flex items-center mt-4 text-sm">
                  <FileText className="h-4 w-4 text-purple-500 mr-1" />
                  <span className="text-gray-600">Multi-source validation</span>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Recent Activity & Quick Actions */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Recent Activity */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5" />
                  Recent Activity
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {isLoading ? (
                    <div className="space-y-3">
                      {[1, 2, 3, 4].map((i) => (
                        <div key={i} className="animate-pulse">
                          <div className="flex gap-3">
                            <div className="w-8 h-8 bg-gray-200 rounded-full"></div>
                            <div className="flex-1">
                              <div className="h-4 bg-gray-200 rounded mb-2"></div>
                              <div className="h-3 bg-gray-100 rounded w-1/2"></div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    metrics.recentActivity.map((activity) => (
                      <div
                        key={activity.id}
                        className="flex items-start gap-3 p-3 border rounded-lg hover:bg-gray-50"
                      >
                        <div className="flex items-center gap-2">
                          {getActivityIcon(activity.type)}
                          {getStatusIcon(activity.status)}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {activity.description}
                          </p>
                          <div className="flex items-center gap-2 mt-1">
                            <span className="text-xs text-gray-500">
                              {formatTimestamp(activity.timestamp)}
                            </span>
                            {activity.confidence && (
                              <Badge variant="outline" className="text-xs">
                                {(activity.confidence * 100).toFixed(0)}% confidence
                              </Badge>
                            )}
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
                <div className="mt-4 pt-4 border-t">
                  <Button variant="outline" size="sm" onClick={() => router.push("/verification")}>
                    View All Activity
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <Button
                    variant="outline"
                    className="h-20 flex flex-col gap-2"
                    onClick={() => router.push("/verification?tab=extract")}
                  >
                    <Search className="h-6 w-6" />
                    <span className="text-sm">Extract Claims</span>
                  </Button>

                  <Button
                    variant="outline"
                    className="h-20 flex flex-col gap-2"
                    onClick={() => router.push("/verification?tab=evidence")}
                  >
                    <Target className="h-6 w-6" />
                    <span className="text-sm">Find Evidence</span>
                  </Button>

                  <Button
                    variant="outline"
                    className="h-20 flex flex-col gap-2"
                    onClick={() => router.push("/verification?tab=stance")}
                  >
                    <Scale className="h-6 w-6" />
                    <span className="text-sm">Classify Stance</span>
                  </Button>

                  <Button
                    variant="outline"
                    className="h-20 flex flex-col gap-2"
                    onClick={() => router.push("/verification?tab=credibility")}
                  >
                    <Shield className="h-6 w-6" />
                    <span className="text-sm">Check Credibility</span>
                  </Button>
                </div>

                <div className="mt-6 space-y-2">
                  <h4 className="text-sm font-medium text-gray-900">Orchestration Tools</h4>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => window.open("http://localhost:8618/nifi", "_blank")}
                    >
                      <ExternalLink className="h-4 w-4 mr-1" />
                      NiFi
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => window.open("http://localhost:5678", "_blank")}
                    >
                      <ExternalLink className="h-4 w-4 mr-1" />
                      n8n
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Verification Pipeline Status */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5" />
                Verification Pipeline Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="w-16 h-16 mx-auto mb-3 bg-blue-100 rounded-full flex items-center justify-center">
                    <Search className="h-8 w-8 text-blue-600" />
                  </div>
                  <h4 className="font-medium mb-1">Claim Extraction</h4>
                  <p className="text-sm text-gray-600 mb-2">NLP-powered claim detection</p>
                  <Badge variant="outline" className="text-green-600 border-green-600">
                    Online
                  </Badge>
                </div>

                <div className="text-center">
                  <div className="w-16 h-16 mx-auto mb-3 bg-green-100 rounded-full flex items-center justify-center">
                    <Target className="h-8 w-8 text-green-600" />
                  </div>
                  <h4 className="font-medium mb-1">Evidence Retrieval</h4>
                  <p className="text-sm text-gray-600 mb-2">Multi-source evidence gathering</p>
                  <Badge variant="outline" className="text-green-600 border-green-600">
                    Online
                  </Badge>
                </div>

                <div className="text-center">
                  <div className="w-16 h-16 mx-auto mb-3 bg-purple-100 rounded-full flex items-center justify-center">
                    <Scale className="h-8 w-8 text-purple-600" />
                  </div>
                  <h4 className="font-medium mb-1">Stance Classification</h4>
                  <p className="text-sm text-gray-600 mb-2">Evidence-claim relationship analysis</p>
                  <Badge variant="outline" className="text-green-600 border-green-600">
                    Online
                  </Badge>
                </div>

                <div className="text-center">
                  <div className="w-16 h-16 mx-auto mb-3 bg-orange-100 rounded-full flex items-center justify-center">
                    <Shield className="h-8 w-8 text-orange-600" />
                  </div>
                  <h4 className="font-medium mb-1">Source Credibility</h4>
                  <p className="text-sm text-gray-600 mb-2">Automated credibility assessment</p>
                  <Badge variant="outline" className="text-green-600 border-green-600">
                    Online
                  </Badge>
                </div>
              </div>

              <div className="mt-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <h4 className="font-medium text-green-800 dark:text-green-300">
                    All Systems Operational
                  </h4>
                </div>
                <p className="text-sm text-green-700 dark:text-green-400">
                  Verification pipeline is running smoothly. Average processing time: 2.3 seconds
                  per claim.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
