// Media Forensics Components for InfoTerminal
// Provides image analysis, EXIF extraction, and forensic capabilities

import React, { useState, useCallback, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Progress } from '../ui/progress';
import { 
  Upload, 
  Image as ImageIcon, 
  Search, 
  Download, 
  RefreshCw, 
  AlertTriangle, 
  Camera, 
  Map, 
  Calendar, 
  Hash,
  Eye,
  ExternalLink,
  Zap
} from 'lucide-react';

interface ExifData {
  [key: string]: any;
}

interface ForensicAnalysis {
  md5_hash: string;
  sha256_hash: string;
  color_depth: number;
  has_transparency: boolean;
  estimated_jpeg_quality?: number;
  potential_manipulation_signs: string[];
  analysis_error?: string;
}

interface ReverseSearchResult {
  url: string;
  title: string;
  thumbnail: string;
  source: string;
  error?: string;
}

interface ImageAnalysisResult {
  filename: string;
  file_size: number;
  image_format: string;
  dimensions: {
    width: number;
    height: number;
  };
  exif_data: ExifData;
  perceptual_hash: {
    phash: string;
    dhash: string;
    whash: string;
  };
  forensic_analysis: ForensicAnalysis;
  reverse_search_results?: ReverseSearchResult[];
}

interface ComparisonResult {
  similarity_score: number;
  hash_distance: number;
  likely_match: boolean;
  analysis: {
    hash1: string;
    hash2: string;
    dimensions1: { width: number; height: number };
    dimensions2: { width: number; height: number };
    same_dimensions: boolean;
    size_difference: number;
    formats: { image1: string; image2: string };
  };
}

interface MediaForensicsProps {
  apiBaseUrl?: string;
  className?: string;
}

export const MediaForensics: React.FC<MediaForensicsProps> = ({ 
  apiBaseUrl = 'http://localhost:8618',
  className = ''
}) => {
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [activeTab, setActiveTab] = useState('analyze');
  const [error, setError] = useState<string | null>(null);
  
  // Analysis state
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [analysisResult, setAnalysisResult] = useState<ImageAnalysisResult | null>(null);
  const [includeReverseSearch, setIncludeReverseSearch] = useState(false);
  
  // Comparison state
  const [compareFile1, setCompareFile1] = useState<File | null>(null);
  const [compareFile2, setCompareFile2] = useState<File | null>(null);
  const [comparisonResult, setComparisonResult] = useState<ComparisonResult | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const compareFile1Ref = useRef<HTMLInputElement>(null);
  const compareFile2Ref = useRef<HTMLInputElement>(null);

  const handleFileSelect = useCallback((file: File, setter: (file: File | null) => void) => {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please select a valid image file');
      return;
    }
    
    // Validate file size (50MB limit)
    if (file.size > 50 * 1024 * 1024) {
      setError('File size must be less than 50MB');
      return;
    }
    
    setter(file);
    setError(null);
  }, []);

  const analyzeImage = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setProgress(0);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('include_reverse_search', includeReverseSearch.toString());

      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + 10, 90));
      }, 200);

      const response = await fetch(`${apiBaseUrl}/image/analyze`, {
        method: 'POST',
        body: formData
      });

      clearInterval(progressInterval);
      setProgress(100);

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`Analysis failed: ${errorData}`);
      }

      const result = await response.json();
      setAnalysisResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setLoading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  };

  const compareImages = async () => {
    if (!compareFile1 || !compareFile2) return;

    setLoading(true);
    setProgress(0);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file1', compareFile1);
      formData.append('file2', compareFile2);

      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + 15, 90));
      }, 150);

      const response = await fetch(`${apiBaseUrl}/image/compare`, {
        method: 'POST',
        body: formData
      });

      clearInterval(progressInterval);
      setProgress(100);

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`Comparison failed: ${errorData}`);
      }

      const result = await response.json();
      setComparisonResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Comparison failed');
    } finally {
      setLoading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  };

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

  const renderFileUpload = (
    file: File | null, 
    onFileSelect: (file: File) => void,
    inputRef: React.RefObject<HTMLInputElement>,
    label: string
  ) => (
    <Card className="border-dashed border-2 hover:border-blue-400 transition-colors">
      <CardContent className="pt-6">
        <div 
          className="text-center cursor-pointer"
          onClick={() => inputRef.current?.click()}
        >
          <input
            type="file"
            ref={inputRef}
            className="hidden"
            accept="image/*"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) onFileSelect(file);
            }}
          />
          
          {file ? (
            <div className="space-y-4">
              <div className="flex items-center justify-center w-16 h-16 mx-auto bg-blue-100 rounded-full">
                <ImageIcon className="h-8 w-8 text-blue-600" />
              </div>
              <div>
                <div className="font-medium">{file.name}</div>
                <div className="text-sm text-gray-500">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </div>
              </div>
              <Button variant="outline" size="sm" onClick={(e) => {
                e.stopPropagation();
                onFileSelect(null as any);
              }}>
                Remove
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-center w-16 h-16 mx-auto bg-gray-100 rounded-full">
                <Upload className="h-8 w-8 text-gray-400" />
              </div>
              <div>
                <div className="font-medium">{label}</div>
                <div className="text-sm text-gray-500">
                  Drag & drop or click to select
                </div>
                <div className="text-xs text-gray-400 mt-1">
                  Supports: JPG, PNG, BMP, TIFF, WebP (max 50MB)
                </div>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );

  const renderExifData = (exifData: ExifData) => (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Camera className="h-5 w-5" />
          EXIF Metadata
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {Object.keys(exifData).length === 0 ? (
            <div className="text-center text-gray-500 py-4">
              No EXIF data found
            </div>
          ) : (
            Object.entries(exifData).map(([key, value]) => (
              <div key={key} className="grid grid-cols-3 gap-4 text-sm">
                <div className="font-medium text-gray-700">{key}</div>
                <div className="col-span-2 break-all">
                  {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                </div>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );

  const renderForensicAnalysis = (analysis: ForensicAnalysis) => (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Zap className="h-5 w-5" />
          Forensic Analysis
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium">MD5 Hash</label>
            <div className="font-mono text-xs bg-gray-50 p-2 rounded">
              {analysis.md5_hash}
            </div>
          </div>
          <div>
            <label className="text-sm font-medium">SHA256 Hash</label>
            <div className="font-mono text-xs bg-gray-50 p-2 rounded">
              {analysis.sha256_hash}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <label className="font-medium">Color Depth</label>
            <div>{analysis.color_depth} channels</div>
          </div>
          <div>
            <label className="font-medium">Transparency</label>
            <div>{analysis.has_transparency ? 'Yes' : 'No'}</div>
          </div>
          {analysis.estimated_jpeg_quality && (
            <div>
              <label className="font-medium">JPEG Quality</label>
              <div>{analysis.estimated_jpeg_quality}%</div>
            </div>
          )}
        </div>

        {analysis.potential_manipulation_signs.length > 0 && (
          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-yellow-600" />
              Potential Manipulation Signs
            </label>
            <div className="space-y-1">
              {analysis.potential_manipulation_signs.map((sign, idx) => (
                <Badge key={idx} variant="outline" className="bg-yellow-50 text-yellow-800">
                  {sign}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );

  const renderPerceptualHashes = (hashes: { phash: string; dhash: string; whash: string }) => (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Hash className="h-5 w-5" />
          Perceptual Hashes
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div>
          <label className="text-sm font-medium">pHash (Perceptual)</label>
          <div className="font-mono text-xs bg-gray-50 p-2 rounded">{hashes.phash}</div>
        </div>
        <div>
          <label className="text-sm font-medium">dHash (Difference)</label>
          <div className="font-mono text-xs bg-gray-50 p-2 rounded">{hashes.dhash}</div>
        </div>
        <div>
          <label className="text-sm font-medium">wHash (Wavelet)</label>
          <div className="font-mono text-xs bg-gray-50 p-2 rounded">{hashes.whash}</div>
        </div>
      </CardContent>
    </Card>
  );

  const renderReverseSearchResults = (results: ReverseSearchResult[]) => (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Search className="h-5 w-5" />
          Reverse Image Search Results
        </CardTitle>
      </CardHeader>
      <CardContent>
        {results.length === 0 ? (
          <div className="text-center text-gray-500 py-4">
            No reverse search results found
          </div>
        ) : (
          <div className="space-y-3">
            {results.map((result, idx) => (
              <div key={idx} className="flex items-center gap-3 p-3 border rounded">
                {result.thumbnail && (
                  <img 
                    src={result.thumbnail} 
                    alt="" 
                    className="w-16 h-16 object-cover rounded"
                    onError={(e) => {
                      (e.target as HTMLImageElement).style.display = 'none';
                    }}
                  />
                )}
                <div className="flex-1">
                  <div className="font-medium">{result.title}</div>
                  <div className="text-sm text-gray-500">Source: {result.source}</div>
                  {result.url && (
                    <Button variant="link" size="sm" className="p-0 h-auto" asChild>
                      <a href={result.url} target="_blank" rel="noopener noreferrer">
                        View Source <ExternalLink className="h-3 w-3 ml-1" />
                      </a>
                    </Button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );

  const renderAnalysisTab = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          {renderFileUpload(
            selectedFile,
            (file) => handleFileSelect(file, setSelectedFile),
            fileInputRef,
            "Upload Image for Analysis"
          )}
        </div>
        
        <Card>
          <CardHeader>
            <CardTitle>Analysis Options</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="reverseSearch"
                checked={includeReverseSearch}
                onChange={(e) => setIncludeReverseSearch(e.target.checked)}
              />
              <label htmlFor="reverseSearch" className="text-sm">
                Include reverse image search
              </label>
            </div>
            
            <Button 
              onClick={analyzeImage} 
              disabled={!selectedFile || loading}
              className="w-full"
            >
              {loading ? (
                <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Eye className="h-4 w-4 mr-2" />
              )}
              Analyze Image
            </Button>

            {analysisResult && (
              <Button 
                variant="outline" 
                onClick={() => downloadResults(analysisResult, `analysis_${analysisResult.filename}.json`)}
                className="w-full"
              >
                <Download className="h-4 w-4 mr-2" />
                Download Results
              </Button>
            )}
          </CardContent>
        </Card>
      </div>

      {loading && progress > 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Processing...</span>
                <span>{progress}%</span>
              </div>
              <Progress value={progress} />
            </div>
          </CardContent>
        </Card>
      )}

      {analysisResult && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Analysis Results: {analysisResult.filename}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <label className="font-medium">Format</label>
                  <div>{analysisResult.image_format}</div>
                </div>
                <div>
                  <label className="font-medium">Dimensions</label>
                  <div>{analysisResult.dimensions.width} × {analysisResult.dimensions.height}</div>
                </div>
                <div>
                  <label className="font-medium">File Size</label>
                  <div>{(analysisResult.file_size / 1024 / 1024).toFixed(2)} MB</div>
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {renderExifData(analysisResult.exif_data)}
            {renderForensicAnalysis(analysisResult.forensic_analysis)}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {renderPerceptualHashes(analysisResult.perceptual_hash)}
            {analysisResult.reverse_search_results && 
              renderReverseSearchResults(analysisResult.reverse_search_results)}
          </div>
        </div>
      )}
    </div>
  );

  const renderComparisonTab = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {renderFileUpload(
          compareFile1,
          (file) => handleFileSelect(file, setCompareFile1),
          compareFile1Ref,
          "Upload First Image"
        )}
        
        {renderFileUpload(
          compareFile2,
          (file) => handleFileSelect(file, setCompareFile2),
          compareFile2Ref,
          "Upload Second Image"
        )}
      </div>

      <Card>
        <CardContent className="pt-6">
          <Button 
            onClick={compareImages} 
            disabled={!compareFile1 || !compareFile2 || loading}
            className="w-full"
          >
            {loading ? (
              <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
            ) : (
              <Search className="h-4 w-4 mr-2" />
            )}
            Compare Images
          </Button>
        </CardContent>
      </Card>

      {loading && progress > 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Comparing...</span>
                <span>{progress}%</span>
              </div>
              <Progress value={progress} />
            </div>
          </CardContent>
        </Card>
      )}

      {comparisonResult && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              Comparison Results
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => downloadResults(comparisonResult, 'image_comparison.json')}
              >
                <Download className="h-4 w-4 mr-2" />
                Download
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">
                {comparisonResult.similarity_score.toFixed(1)}%
              </div>
              <div className="text-lg">Similarity Score</div>
              <Badge 
                className={`mt-2 ${comparisonResult.likely_match 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'}`}
              >
                {comparisonResult.likely_match ? 'Likely Match' : 'Different Images'}
              </Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Image 1</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 text-sm">
                    <div>Format: {comparisonResult.analysis.formats.image1}</div>
                    <div>Dimensions: {comparisonResult.analysis.dimensions1.width} × {comparisonResult.analysis.dimensions1.height}</div>
                    <div>Hash: <code className="text-xs">{comparisonResult.analysis.hash1}</code></div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Image 2</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 text-sm">
                    <div>Format: {comparisonResult.analysis.formats.image2}</div>
                    <div>Dimensions: {comparisonResult.analysis.dimensions2.width} × {comparisonResult.analysis.dimensions2.height}</div>
                    <div>Hash: <code className="text-xs">{comparisonResult.analysis.hash2}</code></div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="grid grid-cols-3 gap-4 text-center text-sm">
              <div>
                <div className="font-medium">Hash Distance</div>
                <div className="text-lg">{comparisonResult.hash_distance}</div>
              </div>
              <div>
                <div className="font-medium">Same Dimensions</div>
                <div className="text-lg">{comparisonResult.analysis.same_dimensions ? 'Yes' : 'No'}</div>
              </div>
              <div>
                <div className="font-medium">Size Difference</div>
                <div className="text-lg">{(comparisonResult.analysis.size_difference / 1024).toFixed(1)} KB</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );

  return (
    <div className={`w-full ${className}`}>
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="analyze">Image Analysis</TabsTrigger>
          <TabsTrigger value="compare">Compare Images</TabsTrigger>
        </TabsList>
        
        <TabsContent value="analyze" className="mt-6">
          {renderAnalysisTab()}
        </TabsContent>
        
        <TabsContent value="compare" className="mt-6">
          {renderComparisonTab()}
        </TabsContent>
      </Tabs>

      {error && (
        <div className="fixed bottom-4 right-4 bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded shadow-lg">
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-4 w-4" />
            {error}
          </div>
        </div>
      )}
    </div>
  );
};

export default MediaForensics;
