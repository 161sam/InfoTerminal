// apps/frontend/pages/docs/[id].tsx - Moderne Dokument-Detail-Seite
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { 
  FileText, 
  Download, 
  Share2, 
  Eye, 
  Clock, 
  User, 
  Building2,
  MapPin,
  Network,
  Sparkles,
  ExternalLink,
  Copy,
  Check
} from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import EntityBadge from '@/components/entities/EntityBadge';
import { DocRecord } from '@/types/docs';
import { uniqueEntities } from '@/lib/entities';
import HighlightedText from '@/components/HighlightedText';

export default function DocumentDetailPage() {
  const router = useRouter();
  const { id } = router.query;
  const [doc, setDoc] = useState<DocRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [summary, setSummary] = useState<string>('');
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!id) return;
    
    const fetchDocument = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_DOC_ENTITIES_URL}/docs/${encodeURIComponent(id as string)}`);
        if (!response.ok) throw new Error('Document not found');
        const docData = await response.json();
        try {
          const nerRes = await fetch(`${process.env.NEXT_PUBLIC_DOC_ENTITIES_URL}/ner`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: docData.text, lang: 'en' })
          });
          const nerData = await nerRes.json();
          setDoc({ ...docData, entities: nerData.entities });
        } catch {
          setDoc(docData);
        }
      } catch (err) {
        setError('Document not found or unavailable');
      } finally {
        setLoading(false);
      }
    };

    fetchDocument();
  }, [id]);

  const generateSummary = async () => {
    if (!doc) return;
    
    setSummaryLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_DOC_ENTITIES_URL}/summary`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: doc.text, lang: 'en' })
      });
      const data = await response.json();
      setSummary(data.summary || '');
    } catch (err) {
      console.error('Failed to generate summary:', err);
    } finally {
      setSummaryLoading(false);
    }
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  if (error || !doc) {
    return (
      <DashboardLayout title="Document Not Found">
        <div className="p-6">
          <div className="text-center py-12">
            <FileText className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-4 text-lg font-medium text-gray-900">Document not found</h3>
            <p className="mt-2 text-gray-500">{error}</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  const entities = uniqueEntities(
    doc.entities.map(e => ({ label: e.label, value: e.text || '' }))
  );

  const handleEntityClick = (entity: any) => {
    if (entity.value) {
      router.push(`/search?value=${encodeURIComponent(entity.value)}`);
    } else {
      router.push(`/search?entity=${encodeURIComponent(entity.label)}`);
    }
  };

  return (
    <DashboardLayout 
      title={doc.meta?.title || 'Document'} 
      subtitle={`Document ID: ${doc.id}`}
    >
      <div className="p-6">
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
          
          {/* Main Content */}
          <div className="xl:col-span-3 space-y-6">
            
            {/* Document Header */}
            <div className="rounded-xl shadow-sm p-6
                 bg-white dark:bg-gray-900
                 border border-gray-200 dark:border-gray-800
                 text-gray-900 dark:text-gray-100">
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-primary-50 rounded-lg">
                    <FileText size={24} className="text-primary-600" />
                  </div>
                  <div>
                    <h1 className="text-2xl font-bold text-gray-900 mb-2">
                      {doc.meta?.title || 'Untitled Document'}
                    </h1>
                    <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                      {doc.meta?.source && (
                        <span className="inline-flex items-center gap-1">
                          <Building2 size={16} />
                          Source: {doc.meta.source}
                        </span>
                      )}
                      {doc.meta?.created_at && (
                        <span className="inline-flex items-center gap-1">
                          <Clock size={16} />
                          {new Date(doc.meta.created_at).toLocaleDateString()}
                        </span>
                      )}
                      <span className="inline-flex items-center gap-1">
                        <Eye size={16} />
                        {doc.text.length.toLocaleString()} characters
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => copyToClipboard(window.location.href)}
                    className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg
            text-gray-700 dark:text-gray-200
            bg-white dark:bg-gray-800
            border border-gray-300 dark:border-gray-600
            hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                  >
                    {copied ? <Check size={16} /> : <Copy size={16} />}
                    {copied ? 'Copied!' : 'Share'}
                  </button>
                  {doc.meta?.aleph_id && (
                    <a
                      href={`${process.env.NEXT_PUBLIC_ALEPH_URL}/#/documents/${doc.meta.aleph_id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary-700 bg-primary-50 border border-primary-200 rounded-lg hover:bg-primary-100 transition-colors"
                    >
                      <ExternalLink size={16} />
                      Open in Aleph
                    </a>
                  )}
                </div>
              </div>

              {/* AI Summary Section */}
              <div className="border-t border-gray-200 dark:border-gray-800 pt-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">AI Summary</h3>
                  <button
                    onClick={generateSummary}
                    disabled={summaryLoading}
                    className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-purple-700 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 transition-colors disabled:opacity-50"
                  >
                    <Sparkles size={16} />
                    {summaryLoading ? 'Generating...' : 'Generate Summary'}
                  </button>
                </div>
                
                {summary ? (
                  <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4 border border-purple-100">
                    <p className="text-gray-800 leading-relaxed">{summary}</p>
                  </div>
                ) : (
                  <div className="rounded-lg p-4 border-2 border-dashed
                 bg-gray-50 dark:bg-gray-800
                 border-gray-300 dark:border-gray-700
                 text-gray-600 dark:text-gray-300">
                    <p className="text-gray-500 text-center">
                      Click "Generate Summary" to create an AI-powered summary of this document
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Document Content */}
            <div className="rounded-xl shadow-sm p-6
                 bg-white dark:bg-gray-900
                 border border-gray-200 dark:border-gray-800
                 text-gray-900 dark:text-gray-100">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Document Content</h3>
              <div className="prose max-w-none">
                <HighlightedText text={doc.text} entities={doc.entities} />
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            
            {/* Entities Panel */}
            <div className="rounded-xl shadow-sm p-6
                 bg-white dark:bg-gray-900
                 border border-gray-200 dark:border-gray-800
                 text-gray-900 dark:text-gray-100">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Entities</h3>
                <span className="text-sm text-gray-500">{entities.length} found</span>
              </div>
              
              {entities.length > 0 ? (
                <div className="space-y-4">
                  {entities.slice(0, 20).map((entity, index) => (
                    <div key={index} className="flex items-start justify-between">
                      <EntityBadge
                        label={entity.label}
                        value={entity.value}
                        countBadge={entity.count}
                        clickable
                        onClick={() => handleEntityClick(entity)}
                      />
                      {entity.count && entity.count > 1 && (
                        <span className="text-xs text-gray-400 ml-2">
                          {entity.count}x
                        </span>
                      )}
                    </div>
                  ))}
                  
                  {entities.length > 20 && (
                    <div className="pt-2 border-t border-gray-100">
                      <span className="text-sm text-gray-500">
                        +{entities.length - 20} more entities
                      </span>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-gray-500 text-sm">No entities detected</p>
              )}
            </div>

            {/* Quick Actions */}
            <div className="rounded-xl shadow-sm p-6
                 bg-white dark:bg-gray-900
                 border border-gray-200 dark:border-gray-800
                 text-gray-900 dark:text-gray-100">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
              
              <div className="space-y-3">
                <button className="w-full flex items-center justify-between p-3 text-left text-sm font-medium text-gray-700 dark:text-gray-200
            bg-gray-50 dark:bg-gray-800 rounded-lg
            hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                  <div className="flex items-center gap-3">
                    <Network size={16} className="text-gray-500" />
                    <span>Explore Graph</span>
                  </div>
                </button>
                
                <button className="w-full flex items-center justify-between p-3 text-left text-sm font-medium text-gray-700 dark:text-gray-200
            bg-gray-50 dark:bg-gray-800 rounded-lg
            hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                  <div className="flex items-center gap-3">
                    <FileText size={16} className="text-gray-500" />
                    <span>Find Similar</span>
                  </div>
                </button>
                
                <button className="w-full flex items-center justify-between p-3 text-left text-sm font-medium text-gray-700 dark:text-gray-200
            bg-gray-50 dark:bg-gray-800 rounded-lg
            hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                  <div className="flex items-center gap-3">
                    <Download size={16} className="text-gray-500" />
                    <span>Export Data</span>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
