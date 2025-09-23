// Enhanced API client for InfoTerminal with error handling and retries
import { getApis } from './config';

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  success: boolean;
}

export interface RequestOptions extends RequestInit {
  timeout?: number;
  retries?: number;
  retryDelay?: number;
}

class ApiClientError extends Error {
  constructor(
    message: string,
    public status?: number,
    public response?: Response
  ) {
    super(message);
    this.name = 'ApiClientError';
  }
}

export class ApiClient {
  private baseTimeout = 10000;
  private maxRetries = 3;
  private retryDelay = 1000;

  async request<T = any>(
    endpoint: string,
    options: RequestOptions = {}
  ): Promise<ApiResponse<T>> {
    const {
      timeout = this.baseTimeout,
      retries = this.maxRetries,
      retryDelay = this.retryDelay,
      ...fetchOptions
    } = options;

    let lastError: Error;

    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        const response = await fetch(endpoint, {
          ...fetchOptions,
          signal: controller.signal,
          headers: {
            'Content-Type': 'application/json',
            ...fetchOptions.headers,
          },
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
          throw new ApiClientError(
            `HTTP ${response.status}: ${response.statusText}`,
            response.status,
            response
          );
        }

        const contentType = response.headers.get('content-type');
        let data: T;

        if (contentType?.includes('application/json')) {
          data = await response.json();
        } else {
          data = (await response.text()) as unknown as T;
        }

        return { data, success: true };
      } catch (error) {
        lastError = error as Error;

        if (attempt === retries) {
          break;
        }

        // Don't retry on client errors (400-499)
        if (error instanceof ApiClientError && error.status && error.status >= 400 && error.status < 500) {
          break;
        }

        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, retryDelay * (attempt + 1)));
      }
    }

    return {
      error: lastError.message,
      success: false,
    };
  }

  async get<T = any>(endpoint: string, options: RequestOptions = {}): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  async post<T = any>(endpoint: string, data?: any, options: RequestOptions = {}): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T = any>(endpoint: string, data?: any, options: RequestOptions = {}): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T = any>(endpoint: string, options: RequestOptions = {}): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' });
  }
}

// Analytics-specific API client with service endpoints
export class AnalyticsApiClient extends ApiClient {
  private apis = getApis();

  // Entity Analytics
  async getEntityStats(filters: any): Promise<ApiResponse<any>> {
    const params = new URLSearchParams();
    if (filters.timeRange) params.append('time_range', filters.timeRange);
    if (filters.entityTypes?.length) params.append('entity_types', filters.entityTypes.join(','));
    if (filters.sources?.length) params.append('sources', filters.sources.join(','));
    
    return this.get(`${this.apis.SEARCH_API}/v1/analytics/entities?${params}`);
  }

  async getTopEntities(filters: any): Promise<ApiResponse<any>> {
    const params = new URLSearchParams();
    if (filters.limit) params.append('limit', filters.limit.toString());
    if (filters.entityTypes?.length) params.append('types', filters.entityTypes.join(','));
    
    return this.get(`${this.apis.SEARCH_API}/v1/analytics/entities/top?${params}`);
  }

  // Source Coverage
  async getSourceCoverage(filters: any): Promise<ApiResponse<any>> {
    const params = new URLSearchParams();
    if (filters.timeRange) params.append('time_range', filters.timeRange);
    
    return this.get(`${this.apis.SEARCH_API}/v1/analytics/sources?${params}`);
  }

  // Evidence Quality
  async getEvidenceQuality(filters: any): Promise<ApiResponse<any>> {
    const params = new URLSearchParams();
    if (filters.timeRange) params.append('time_range', filters.timeRange);
    
    // Try verification service first, fallback to search
    const verificationResponse = await this.get(`${this.apis.DOC_ENTITIES_API}/v1/analytics/evidence?${params}`);
    if (verificationResponse.success) {
      return verificationResponse;
    }

    return this.get(`${this.apis.SEARCH_API}/v1/analytics/evidence?${params}`);
  }

  // Workflow Runs
  async getWorkflowRuns(filters: any): Promise<ApiResponse<any>> {
    const params = new URLSearchParams();
    if (filters.limit) params.append('limit', filters.limit.toString());
    if (filters.status) params.append('status', filters.status);
    
    return this.get(`${this.apis.FLOWISE_API}/v1/runs?${params}`);
  }

  // Timeline Data
  async getTimeline(filters: any): Promise<ApiResponse<any>> {
    const params = new URLSearchParams();
    if (filters.timeRange) params.append('time_range', filters.timeRange);
    if (filters.entityTypes?.length) params.append('entity_types', filters.entityTypes.join(','));
    
    return this.get(`${this.apis.SEARCH_API}/v1/analytics/timeline?${params}`);
  }

  // Geospatial Data
  async getGeoEntities(filters: any): Promise<ApiResponse<any>> {
    const params = new URLSearchParams();
    if (filters.bbox) params.append('bbox', filters.bbox.join(','));
    if (filters.entityTypes?.length) params.append('entity_types', filters.entityTypes.join(','));
    
    return this.get(`${this.apis.SEARCH_API}/v1/analytics/geo?${params}`);
  }

  // Graph Metrics
  async getGraphMetrics(filters: any): Promise<ApiResponse<any>> {
    const params = new URLSearchParams();
    if (filters.algorithm) params.append('algorithm', filters.algorithm);
    if (filters.limit) params.append('limit', filters.limit.toString());
    
    return this.get(`${this.apis.GRAPH_API}/v1/analytics/metrics?${params}`);
  }

  // Query Insights
  async getQueryInsights(filters: any): Promise<ApiResponse<any>> {
    const params = new URLSearchParams();
    if (filters.timeRange) params.append('time_range', filters.timeRange);
    
    return this.get(`${this.apis.SEARCH_API}/v1/analytics/queries?${params}`);
  }
}

export const apiClient = new ApiClient();
export const analyticsApi = new AnalyticsApiClient();
