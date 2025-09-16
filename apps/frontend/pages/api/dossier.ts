import type { NextApiRequest, NextApiResponse } from 'next';

const GRAPH_VIEWS_URL = process.env.NEXT_PUBLIC_VIEWS_API || 'http://localhost:8403';

// Utility function to safely convert header values to strings
function getHeaderValue(value: string | string[] | undefined, defaultValue: string): string {
  if (Array.isArray(value)) {
    return value[0] || defaultValue;
  }
  return value || defaultValue;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Validate request body
    const { title, items, options } = req.body;
    
    if (!title || typeof title !== 'string') {
      return res.status(400).json({ error: 'Title is required and must be a string' });
    }

    // Prepare payload for graph-views service
    const payload = {
      title,
      items: items || { docs: [], nodes: [], edges: [] },
      options: options || { summary: false }
    };

    // Forward request to graph-views service
    const response = await fetch(`${GRAPH_VIEWS_URL}/dossier`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Forward user context if needed
        'X-User-Id': getHeaderValue(req.headers['x-user-id'], 'system'),
        'X-Request-Id': getHeaderValue(req.headers['x-request-id'], 'dossier-' + Date.now())
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const error = await response.text();
      console.error('Graph-views dossier generation failed:', error);
      return res.status(response.status).json({ 
        error: `Dossier generation failed: ${error}` 
      });
    }

    const data = await response.json();
    
    // Calculate estimated size for metadata
    const estimatedSize = data.markdown ? 
      (data.markdown.length / 1024).toFixed(1) + ' KB' : 
      'Unknown';

    // Enhance response with metadata
    const enhancedResponse = {
      markdown: data.markdown || '',
      pdfUrl: data.pdfUrl || null,
      size: estimatedSize,
      metadata: {
        generatedAt: new Date().toISOString(),
        service: 'graph-views',
        itemCount: (payload.items.docs?.length || 0) + 
                   (payload.items.nodes?.length || 0) + 
                   (payload.items.edges?.length || 0)
      }
    };

    res.status(200).json(enhancedResponse);
  } catch (error) {
    console.error('Error proxying to graph-views dossier service:', error);
    res.status(500).json({ 
      error: 'Failed to generate dossier',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
