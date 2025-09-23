import { useState, useEffect } from 'react';
import { 
  FileText, 
  Download, 
  Plus, 
  Trash2, 
  Eye, 
  RefreshCw, 
  Save, 
  Upload,
  Users,
  Network,
  BarChart3,
  Calendar,
  Tag,
  Settings,
  Copy,
  ExternalLink,
  CheckCircle,
  AlertTriangle,
  Clock
} from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';

interface DossierItem {
  id: string;
  type: 'document' | 'entity' | 'node' | 'edge';
  value: string;
  metadata?: {
    title?: string;
    description?: string;
    confidence?: number;
    lastSeen?: string;
  };
}

interface DossierTemplate {
  id: string;
  name: string;
  description: string;
  items: DossierItem[];
  settings: DossierSettings;
}

interface DossierSettings {
  includeTimeline: boolean;
  includeSummary: boolean;
  includeVisualization: boolean;
  confidenceThreshold: number;
  dateRange?: { from: string; to: string };
  language: 'en' | 'de';
}

interface GeneratedDossier {
  markdown: string;
  pdfUrl?: string;
  metadata: {
    title: string;
    generatedAt: string;
    itemCount: number;
    size: string;
  };
}

const DOSSIER_TEMPLATES: DossierTemplate[] = [
  {
    id: 'investigation',
    name: 'Investigation Report',
    description: 'Comprehensive investigation with entities and connections',
    items: [],
    settings: {
      includeTimeline: true,
      includeSummary: true,
      includeVisualization: true,
      confidenceThreshold: 0.8,
      language: 'en'
    }
  },
  {
    id: 'entity-profile',
    name: 'Entity Profile',
    description: 'Detailed profile for a specific person or organization',
    items: [],
    settings: {
      includeTimeline: true,
      includeSummary: false,
      includeVisualization: false,
      confidenceThreshold: 0.9,
      language: 'en'
    }
  },
  {
    id: 'network-analysis',
    name: 'Network Analysis',
    description: 'Focus on relationships and network connections',
    items: [],
    settings: {
      includeTimeline: false,
      includeSummary: true,
      includeVisualization: true,
      confidenceThreshold: 0.7,
      language: 'en'
    }
  }
];

const EXAMPLE_ITEMS: DossierItem[] = [
  {
    id: '1',
    type: 'document',
    value: 'financial-report-q3-2024.pdf',
    metadata: { title: 'Q3 Financial Report', description: 'Quarterly earnings report', lastSeen: '2024-03-01' }
  },
  {
    id: '2',
    type: 'entity',
    value: 'John Smith',
    metadata: { title: 'John Smith', description: 'CEO of ACME Corp', confidence: 0.95, lastSeen: '2024-03-01' }
  },
  {
    id: '3',
    type: 'entity',
    value: 'ACME Corporation',
    metadata: { title: 'ACME Corporation', description: 'Technology company', confidence: 0.98, lastSeen: '2024-03-02' }
  }
];

export default function DossierPage() {
  const [title, setTitle] = useState('Investigation Report');
  const [items, setItems] = useState<DossierItem[]>([]);
  const [settings, setSettings] = useState<DossierSettings>({
    includeTimeline: true,
    includeSummary: true,
    includeVisualization: true,
    confidenceThreshold: 0.8,
    language: 'en'
  });
  
  const [generatedDossier, setGeneratedDossier] = useState<GeneratedDossier | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<string>('');
  const [newItemValue, setNewItemValue] = useState('');
  const [newItemType, setNewItemType] = useState<DossierItem['type']>('document');

  useEffect(() => {
    // Load example items on mount
    setItems(EXAMPLE_ITEMS);
  }, []);

  const addItem = () => {
    if (!newItemValue.trim()) return;
    
    const newItem: DossierItem = {
      id: Date.now().toString(),
      type: newItemType,
      value: newItemValue.trim(),
      metadata: {
        title: newItemValue.trim(),
        lastSeen: new Date().toISOString().split('T')[0]
      }
    };
    
    setItems(prev => [...prev, newItem]);
    setNewItemValue('');
  };

  const removeItem = (id: string) => {
    setItems(prev => prev.filter(item => item.id !== id));
  };

  const loadTemplate = (templateId: string) => {
    const template = DOSSIER_TEMPLATES.find(t => t.id === templateId);
    if (!template) return;
    
    setTitle(template.name);
    setSettings(template.settings);
    setSelectedTemplate(templateId);
  };

  const generateDossier = async () => {
    setIsGenerating(true);
    
    try {
      const payload = {
        title,
        items: {
          docs: items.filter(i => i.type === 'document').map(i => i.value),
          nodes: items.filter(i => i.type === 'node' || i.type === 'entity').map(i => i.value),
          edges: items.filter(i => i.type === 'edge').map(i => i.value),
        },
        options: {
          summary: settings.includeSummary,
          timeline: settings.includeTimeline,
          visualization: settings.includeVisualization,
          confidence: settings.confidenceThreshold,
          language: settings.language,
          dateRange: settings.dateRange
        },
      };
      
      const response = await fetch('/api/dossier', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      
      if (!response.ok) throw new Error('Failed to generate dossier');
      
      const data = await response.json();
      
      setGeneratedDossier({
        markdown: data.markdown || 'No content generated',
        pdfUrl: data.pdfUrl,
        metadata: {
          title,
          generatedAt: new Date().toISOString(),
          itemCount: items.length,
          size: data.size || 'Unknown'
        }
      });
      
      setShowPreview(true);
    } catch (error) {
      console.error('Failed to generate dossier:', error);
      // Show error state
    } finally {
      setIsGenerating(false);
    }
  };

  const exportDossier = () => {
    const exportData = {
      title,
      items,
      settings,
      exportedAt: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title.replace(/\s+/g, '-').toLowerCase()}-config.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const copyMarkdown = () => {
    if (generatedDossier?.markdown) {
      navigator.clipboard.writeText(generatedDossier.markdown);
    }
  };

  const getItemTypeIcon = (type: DossierItem['type']) => {
    switch (type) {
      case 'document': return FileText;
      case 'entity': return Users;
      case 'node': return Network;
      case 'edge': return Network;
      default: return FileText;
    }
  };

  const getItemTypeColor = (type: DossierItem['type']) => {
    switch (type) {
      case 'document': return 'bg-blue-100 text-blue-800';
      case 'entity': return 'bg-green-100 text-green-800';
      case 'node': return 'bg-purple-100 text-purple-800';
      case 'edge': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <DashboardLayout title="Dossier Builder" subtitle="Create comprehensive investigation reports">
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* Header Controls */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex-1 max-w-md">
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter dossier title..."
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              />
            </div>
            
            <select
              value={selectedTemplate}
              onChange={(e) => loadTemplate(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              <option value="">Select Template</option>
              {DOSSIER_TEMPLATES.map(template => (
                <option key={template.id} value={template.id}>{template.name}</option>
              ))}
            </select>
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={exportDossier}
              className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
            >
              <Upload size={14} />
              Export Config
            </button>
            
            <button
              onClick={generateDossier}
              disabled={isGenerating || items.length === 0}
              className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGenerating ? (
                <RefreshCw size={14} className="animate-spin" />
              ) : (
                <FileText size={14} />
              )}
              {isGenerating ? 'Generating...' : 'Generate Dossier'}
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Items Section */}
            <Panel title="Dossier Content">
              <div className="space-y-4">
                
                {/* Add Item */}
                <div className="flex items-center gap-2 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <select
                    value={newItemType}
                    onChange={(e) => setNewItemType(e.target.value as DossierItem['type'])}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  >
                    <option value="document">Document</option>
                    <option value="entity">Entity</option>
                    <option value="node">Node</option>
                    <option value="edge">Edge</option>
                  </select>
                  
                  <input
                    type="text"
                    value={newItemValue}
                    onChange={(e) => setNewItemValue(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addItem()}
                    placeholder="Enter item identifier..."
                    className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  />
                  
                  <button
                    onClick={addItem}
                    disabled={!newItemValue.trim()}
                    className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Plus size={14} />
                    Add
                  </button>
                </div>

                {/* Items List */}
                <div className="space-y-2">
                  {items.length === 0 ? (
                    <div className="text-center py-8 text-gray-500 dark:text-slate-400">
                      <FileText size={32} className="mx-auto mb-2" />
                      <p>No items added yet</p>
                      <p className="text-sm">Add documents, entities, or graph nodes to build your dossier</p>
                    </div>
                  ) : (
                    items.map((item) => {
                      const Icon = getItemTypeIcon(item.type);
                      return (
                        <div key={item.id} className="flex items-center gap-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                          <div className="p-2 bg-gray-100 dark:bg-gray-800 rounded">
                            <Icon size={16} className="text-gray-600 dark:text-slate-400" />
                          </div>
                          
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-1">
                              <span className={`px-2 py-1 text-xs font-medium rounded-full ${getItemTypeColor(item.type)}`}>
                                {item.type}
                              </span>
                              <h4 className="font-medium text-gray-900 dark:text-slate-100 truncate">
                                {item.metadata?.title || item.value}
                              </h4>
                            </div>
                            
                            {item.metadata?.description && (
                              <p className="text-sm text-gray-600 dark:text-slate-400 truncate">
                                {item.metadata.description}
                              </p>
                            )}
                            
                            <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-slate-400 mt-1">
                              {item.metadata?.confidence && (
                                <span>Confidence: {Math.round(item.metadata.confidence * 100)}%</span>
                              )}
                              {item.metadata?.lastSeen && (
                                <span>Last seen: {item.metadata.lastSeen}</span>
                              )}
                            </div>
                          </div>
                          
                          <button
                            onClick={() => removeItem(item.id)}
                            className="p-1 text-gray-400 hover:text-red-600 rounded"
                          >
                            <Trash2 size={14} />
                          </button>
                        </div>
                      );
                    })
                  )}
                </div>
              </div>
            </Panel>

            {/* Generated Dossier Preview */}
            {showPreview && generatedDossier && (
              <Panel>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">Generated Dossier</h3>
                  
                  <div className="flex items-center gap-2">
                    <button
                      onClick={copyMarkdown}
                      className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
                    >
                      <Copy size={14} />
                      Copy
                    </button>
                    
                    {generatedDossier.pdfUrl && (
                      <a
                        href={generatedDossier.pdfUrl}
                        download
                        className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700"
                      >
                        <Download size={14} />
                        Download PDF
                      </a>
                    )}
                  </div>
                </div>
                
                {/* Metadata */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 text-sm">
                  <div>
                    <span className="text-gray-500 dark:text-slate-400">Generated</span>
                    <div className="font-medium text-gray-900 dark:text-slate-100">
                      {new Date(generatedDossier.metadata.generatedAt).toLocaleString()}
                    </div>
                  </div>
                  <div>
                    <span className="text-gray-500 dark:text-slate-400">Items</span>
                    <div className="font-medium text-gray-900 dark:text-slate-100">
                      {generatedDossier.metadata.itemCount}
                    </div>
                  </div>
                  <div>
                    <span className="text-gray-500 dark:text-slate-400">Size</span>
                    <div className="font-medium text-gray-900 dark:text-slate-100">
                      {generatedDossier.metadata.size}
                    </div>
                  </div>
                  <div>
                    <span className="text-gray-500 dark:text-slate-400">Status</span>
                    <div className="flex items-center gap-1">
                      <CheckCircle size={14} className="text-green-500" />
                      <span className="font-medium text-green-600">Complete</span>
                    </div>
                  </div>
                </div>
                
                {/* Markdown Preview */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div className="flex items-center justify-between p-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
                    <span className="text-sm font-medium text-gray-700 dark:text-slate-300">Markdown Preview</span>
                    <button
                      onClick={() => setShowPreview(false)}
                      className="text-gray-400 hover:text-gray-600 dark:hover:text-slate-200"
                    >
                      <Eye size={14} />
                    </button>
                  </div>
                  
                  <pre className="p-4 max-h-96 overflow-auto text-sm bg-white dark:bg-gray-900 text-gray-800 dark:text-slate-200 font-mono">
                    {generatedDossier.markdown}
                  </pre>
                </div>
              </Panel>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            
            {/* Templates */}
            <Panel title="Templates">
              <div className="space-y-3">
                {DOSSIER_TEMPLATES.map((template) => (
                  <button
                    key={template.id}
                    onClick={() => loadTemplate(template.id)}
                    className={`w-full text-left p-3 rounded-lg border-2 transition-colors ${
                      selectedTemplate === template.id
                        ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                        : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                    }`}
                  >
                    <div className="font-medium text-gray-900 dark:text-slate-100 text-sm">
                      {template.name}
                    </div>
                    <div className="text-xs text-gray-600 dark:text-slate-400 mt-1">
                      {template.description}
                    </div>
                  </button>
                ))}
              </div>
            </Panel>

            {/* Settings */}
            <Panel title="Generation Settings">
              <div className="space-y-4">
                <div className="space-y-3">
                  {[
                    { key: 'includeSummary', label: 'Include Summary', description: 'Generate executive summary' },
                    { key: 'includeTimeline', label: 'Include Timeline', description: 'Add chronological timeline' },
                    { key: 'includeVisualization', label: 'Include Visualization', description: 'Add charts and graphs' }
                  ].map((setting) => (
                    <div key={setting.key} className="flex items-center justify-between">
                      <div>
                        <div className="text-sm font-medium text-gray-900 dark:text-slate-100">
                          {setting.label}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-slate-400">
                          {setting.description}
                        </div>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={settings[setting.key as keyof DossierSettings] as boolean}
                          onChange={(e) => setSettings(prev => ({
                            ...prev,
                            [setting.key]: e.target.checked
                          }))}
                          className="sr-only peer"
                        />
                        <div className="w-9 h-5 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
                      </label>
                    </div>
                  ))}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
                    Confidence Threshold: {Math.round(settings.confidenceThreshold * 100)}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={settings.confidenceThreshold}
                    onChange={(e) => setSettings(prev => ({
                      ...prev,
                      confidenceThreshold: parseFloat(e.target.value)
                    }))}
                    className="w-full"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
                    Language
                  </label>
                  <select
                    value={settings.language}
                    onChange={(e) => setSettings(prev => ({
                      ...prev,
                      language: e.target.value as 'en' | 'de'
                    }))}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  >
                    <option value="en">English</option>
                    <option value="de">Deutsch</option>
                  </select>
                </div>
              </div>
            </Panel>

            {/* Statistics */}
            <Panel title="Content Statistics">
              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-slate-400">Total Items</span>
                  <span className="font-medium text-gray-900 dark:text-slate-100">{items.length}</span>
                </div>
                
                {['document', 'entity', 'node', 'edge'].map(type => {
                  const count = items.filter(item => item.type === type).length;
                  if (count === 0) return null;
                  
                  return (
                    <div key={type} className="flex items-center justify-between">
                      <span className="text-gray-600 dark:text-slate-400 capitalize">{type}s</span>
                      <span className="font-medium text-gray-900 dark:text-slate-100">{count}</span>
                    </div>
                  );
                })}
                
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-slate-400">Avg. Confidence</span>
                  <span className="font-medium text-gray-900 dark:text-slate-100">
                    {items.length > 0 
                      ? Math.round(items.reduce((sum, item) => sum + (item.metadata?.confidence || 0), 0) / items.length * 100)
                      : 0
                    }%
                  </span>
                </div>
              </div>
            </Panel>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
