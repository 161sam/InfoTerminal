// Graph Analytics Components for InfoTerminal
// Provides centrality analysis, community detection, and network statistics

import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Play, Download, RefreshCw, Network, Users, TrendingUp } from 'lucide-react';

interface CentralityNode {
  node_id: string;
  name: string;
  labels: string[];
  centrality_score: number;
  degree?: number;
}

interface Community {
  id: number;
  size: number;
  members: Array<{
    node_id: string;
    name: string;
    labels: string[];
  }>;
}

interface GraphSummary {
  total_nodes: number;
  total_relationships: number;
  node_types: Array<{
    label: string;
    count: number;
  }>;
  relationship_types: Array<{
    type: string;
    count: number;
  }>;
}

interface GraphAnalyticsProps {
  apiBaseUrl?: string;
  className?: string;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

export const GraphAnalytics: React.FC<GraphAnalyticsProps> = ({ 
  apiBaseUrl = 'http://localhost:8612',
  className = ''
}) => {
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('centrality');
  
  // Centrality state
  const [centralityType, setCentralityType] = useState<'degree' | 'betweenness'>('degree');
  const [centralityData, setCentralityData] = useState<CentralityNode[]>([]);
  const [nodeTypeFilter, setNodeTypeFilter] = useState<string>('');
  const [centralityLimit, setCentralityLimit] = useState(20);
  
  // Community state
  const [communities, setCommunities] = useState<Community[]>([]);
  const [communityAlgorithm, setCommunityAlgorithm] = useState('louvain');
  const [minCommunitySize, setMinCommunitySize] = useState(3);
  
  // Summary state
  const [graphSummary, setGraphSummary] = useState<GraphSummary | null>(null);
  
  // Error state
  const [error, setError] = useState<string | null>(null);

  const fetchCentralityData = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const params = new URLSearchParams({
        limit: centralityLimit.toString()
      });
      
      if (nodeTypeFilter) {
        params.append('node_type', nodeTypeFilter);
      }
      
      const response = await fetch(
        `${apiBaseUrl}/analytics/centrality/${centralityType}?${params}`
      );
      
      if (!response.ok) {
        throw new Error(`Failed to fetch centrality data: ${response.statusText}`);
      }
      
      const data = await response.json();
      setCentralityData(data.nodes || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl, centralityType, nodeTypeFilter, centralityLimit]);

  const fetchCommunities = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${apiBaseUrl}/analytics/communities`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          algorithm: communityAlgorithm,
          min_community_size: minCommunitySize
        })
      });
      
      if (!response.ok) {
        throw new Error(`Failed to fetch community data: ${response.statusText}`);
      }
      
      const data = await response.json();
      setCommunities(data.communities || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl, communityAlgorithm, minCommunitySize]);

  const fetchGraphSummary = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${apiBaseUrl}/analytics/summary`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch graph summary: ${response.statusText}`);
      }
      
      const data = await response.json();
      setGraphSummary(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl]);

  useEffect(() => {
    if (activeTab === 'centrality') {
      fetchCentralityData();
    } else if (activeTab === 'communities') {
      fetchCommunities();
    } else if (activeTab === 'overview') {
      fetchGraphSummary();
    }
  }, [activeTab, fetchCentralityData, fetchCommunities, fetchGraphSummary]);

  const downloadResults = (data: any, filename: string) => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const renderCentralityTab = () => (
    <div className="space-y-6">
      {/* Controls */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Centrality Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <label className="text-sm font-medium">Centrality Type</label>
              <Select value={centralityType} onValueChange={(value: 'degree' | 'betweenness') => setCentralityType(value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="degree">Degree Centrality</SelectItem>
                  <SelectItem value="betweenness">Betweenness Centrality</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div>
              <label className="text-sm font-medium">Node Type Filter</label>
              <Input
                placeholder="e.g., Person, Organization"
                value={nodeTypeFilter}
                onChange={(e) => setNodeTypeFilter(e.target.value)}
              />
            </div>
            
            <div>
              <label className="text-sm font-medium">Limit</label>
              <Input
                type="number"
                min="5"
                max="100"
                value={centralityLimit}
                onChange={(e) => setCentralityLimit(Number(e.target.value))}
              />
            </div>
            
            <div className="flex items-end gap-2">
              <Button onClick={fetchCentralityData} disabled={loading} className="flex-1">
                {loading ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
                Analyze
              </Button>
              <Button 
                variant="outline" 
                size="icon"
                onClick={() => downloadResults(centralityData, `centrality_${centralityType}.json`)}
                disabled={centralityData.length === 0}
              >
                <Download className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Results */}
      {error && (
        <Card>
          <CardContent className="pt-6">
            <div className="text-red-600 text-center">{error}</div>
          </CardContent>
        </Card>
      )}

      {centralityData.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Top Nodes by {centralityType === 'degree' ? 'Degree' : 'Betweenness'}</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={centralityData.slice(0, 10)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="name" 
                    angle={-45}
                    textAnchor="end"
                    height={100}
                    interval={0}
                  />
                  <YAxis />
                  <Tooltip 
                    formatter={(value: number, name: string) => [
                      typeof value === 'number' ? value.toFixed(2) : value,
                      centralityType === 'degree' ? 'Degree' : 'Betweenness Score'
                    ]}
                  />
                  <Bar dataKey="centrality_score" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Table */}
          <Card>
            <CardHeader>
              <CardTitle>Detailed Results</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="max-h-96 overflow-y-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-2">Node</th>
                      <th className="text-left p-2">Labels</th>
                      <th className="text-right p-2">Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {centralityData.map((node, index) => (
                      <tr key={node.node_id} className="border-b hover:bg-gray-50">
                        <td className="p-2">
                          <div className="font-medium">{node.name || 'Unnamed'}</div>
                          <div className="text-xs text-gray-500">{node.node_id}</div>
                        </td>
                        <td className="p-2">
                          <div className="flex flex-wrap gap-1">
                            {node.labels.map(label => (
                              <Badge key={label} variant="secondary" className="text-xs">
                                {label}
                              </Badge>
                            ))}
                          </div>
                        </td>
                        <td className="p-2 text-right font-mono">
                          {typeof node.centrality_score === 'number' 
                            ? node.centrality_score.toFixed(2) 
                            : node.centrality_score}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );

  const renderCommunitiesTab = () => (
    <div className="space-y-6">
      {/* Controls */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5" />
            Community Detection
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium">Algorithm</label>
              <Select value={communityAlgorithm} onValueChange={setCommunityAlgorithm}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="louvain">Louvain</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div>
              <label className="text-sm font-medium">Min Community Size</label>
              <Input
                type="number"
                min="2"
                max="50"
                value={minCommunitySize}
                onChange={(e) => setMinCommunitySize(Number(e.target.value))}
              />
            </div>
            
            <div className="flex items-end gap-2">
              <Button onClick={fetchCommunities} disabled={loading} className="flex-1">
                {loading ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
                Detect
              </Button>
              <Button 
                variant="outline" 
                size="icon"
                onClick={() => downloadResults(communities, 'communities.json')}
                disabled={communities.length === 0}
              >
                <Download className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Community Results */}
      {communities.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Size Distribution */}
          <Card>
            <CardHeader>
              <CardTitle>Community Size Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={communities.map(c => ({ name: `Community ${c.id}`, value: c.size }))}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name} (${value})`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {communities.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Community List */}
          <Card>
            <CardHeader>
              <CardTitle>Communities Found: {communities.length}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="max-h-96 overflow-y-auto space-y-4">
                {communities.map((community, index) => (
                  <div key={community.id} className="border rounded p-3">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium">Community {community.id}</h4>
                      <Badge variant="outline">{community.size} members</Badge>
                    </div>
                    <div className="text-sm space-y-1">
                      {community.members.slice(0, 5).map(member => (
                        <div key={member.node_id} className="flex items-center gap-2">
                          <span className="font-medium">{member.name || 'Unnamed'}</span>
                          <div className="flex gap-1">
                            {member.labels.map(label => (
                              <Badge key={label} variant="secondary" className="text-xs">
                                {label}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      ))}
                      {community.size > 5 && (
                        <div className="text-gray-500 text-xs">
                          ... and {community.size - 5} more
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );

  const renderOverviewTab = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Network className="h-5 w-5" />
            Graph Overview
            <Button 
              variant="outline" 
              size="sm" 
              onClick={fetchGraphSummary} 
              disabled={loading}
            >
              {loading ? <RefreshCw className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}
              Refresh
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {graphSummary && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{graphSummary.total_nodes.toLocaleString()}</div>
                <div className="text-sm text-gray-600">Total Nodes</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{graphSummary.total_relationships.toLocaleString()}</div>
                <div className="text-sm text-gray-600">Relationships</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">{graphSummary.node_types.length}</div>
                <div className="text-sm text-gray-600">Node Types</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">{graphSummary.relationship_types.length}</div>
                <div className="text-sm text-gray-600">Relation Types</div>
              </div>
            </div>
          )}

          {graphSummary && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Node Types */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Node Types Distribution</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={graphSummary.node_types.slice(0, 10)}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="label" angle={-45} textAnchor="end" height={80} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Relationship Types */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Relationship Types</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={graphSummary.relationship_types.slice(0, 10)}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="type" angle={-45} textAnchor="end" height={80} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#82ca9d" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );

  return (
    <div className={`w-full ${className}`}>
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="centrality">Centrality</TabsTrigger>
          <TabsTrigger value="communities">Communities</TabsTrigger>
          <TabsTrigger value="overview">Overview</TabsTrigger>
        </TabsList>
        
        <TabsContent value="centrality" className="mt-6">
          {renderCentralityTab()}
        </TabsContent>
        
        <TabsContent value="communities" className="mt-6">
          {renderCommunitiesTab()}
        </TabsContent>
        
        <TabsContent value="overview" className="mt-6">
          {renderOverviewTab()}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default GraphAnalytics;
