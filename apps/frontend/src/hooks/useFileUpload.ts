// apps/frontend/src/hooks/useFileUpload.ts
import { useCallback, useRef, useState } from 'react';

export type UploadStatus = 'pending' | 'uploading' | 'success' | 'error' | 'cancelled';

export interface UploadItem {
  id: string;
  file: File;
  fileName: string;
  progress: number;
  status: UploadStatus;
  xhr?: XMLHttpRequest;
  doc_id?: string;
  aleph_id?: string;
  message?: string;
  uploadedAt?: Date;
  retry: () => Promise<any>;
}

interface UploadOptions {
  maxConcurrent?: number;
  chunkSize?: number;
  allowedTypes?: string[];
  maxFileSize?: number; // in bytes
}

export default function useFileUpload(url: string = '/api/documents/upload', options: UploadOptions = {}) {
  const [uploads, setUploads] = useState<UploadItem[]>([]);
  const queueRef = useRef<UploadItem[]>([]);
  const abortControllersRef = useRef<Map<string, AbortController>>(new Map());
  
  const {
    maxConcurrent = 3,
    allowedTypes = ['application/pdf', 'text/plain', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    maxFileSize = 50 * 1024 * 1024 // 50MB
  } = options;

  const validateFile = useCallback((file: File): string | null => {
    if (allowedTypes.length > 0 && !allowedTypes.includes(file.type)) {
      return `File type ${file.type} is not supported. Allowed types: ${allowedTypes.join(', ')}`;
    }
    
    if (file.size > maxFileSize) {
      return `File size ${(file.size / 1024 / 1024).toFixed(1)}MB exceeds maximum allowed size of ${(maxFileSize / 1024 / 1024).toFixed(1)}MB`;
    }
    
    return null;
  }, [allowedTypes, maxFileSize]);

  const processQueue = useCallback(() => {
    const activeUploads = uploads.filter(u => u.status === 'uploading').length;
    const pendingUploads = queueRef.current.filter(u => u.status === 'pending');
    
    const slotsAvailable = maxConcurrent - activeUploads;
    const uploadsToStart = pendingUploads.slice(0, slotsAvailable);
    
    uploadsToStart.forEach(item => {
      if (item.status === 'pending') {
        uploadSingle(item);
      }
    });
  }, [uploads, maxConcurrent]);

  const uploadSingle = useCallback(async (item: UploadItem) => {
    const abortController = new AbortController();
    abortControllersRef.current.set(item.id, abortController);

    setUploads(prev => prev.map(upload => 
      upload.id === item.id ? { ...upload, status: 'uploading', progress: 0, message: undefined } : upload
    ));

    try {
      const xhr = new XMLHttpRequest();
      item.xhr = xhr;

      // Handle upload progress
      xhr.upload.addEventListener('progress', (event: ProgressEvent) => {
        if (event.lengthComputable) {
          const progress = Math.round((event.loaded / event.total) * 100);
          setUploads(prev => prev.map(upload =>
            upload.id === item.id ? { ...upload, progress } : upload
          ));
        }
      });

      // Handle response
      xhr.addEventListener('readystatechange', () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              const response = JSON.parse(xhr.responseText);
              const result = response.results?.[0] || response;
              
              setUploads(prev => prev.map(upload =>
                upload.id === item.id ? {
                  ...upload,
                  status: 'success',
                  progress: 100,
                  doc_id: result.doc_id,
                  aleph_id: result.aleph_id,
                  uploadedAt: new Date(),
                  message: 'Upload completed successfully'
                } : upload
              ));
            } catch (error) {
              setUploads(prev => prev.map(upload =>
                upload.id === item.id ? {
                  ...upload,
                  status: 'error',
                  message: 'Invalid response format'
                } : upload
              ));
            }
          } else {
            let errorMessage = `Upload failed (${xhr.status})`;
            try {
              const errorResponse = JSON.parse(xhr.responseText);
              errorMessage = errorResponse.message || errorMessage;
            } catch (e) {
              // Use default error message
            }
            
            setUploads(prev => prev.map(upload =>
              upload.id === item.id ? {
                ...upload,
                status: 'error',
                message: errorMessage
              } : upload
            ));
          }
          
          abortControllersRef.current.delete(item.id);
          
          // Remove from queue and process next uploads
          queueRef.current = queueRef.current.filter(q => q.id !== item.id);
          setTimeout(processQueue, 100);
        }
      });

      // Handle network errors
      xhr.addEventListener('error', () => {
        setUploads(prev => prev.map(upload =>
          upload.id === item.id ? {
            ...upload,
            status: 'error',
            message: 'Network error occurred'
          } : upload
        ));
        
        abortControllersRef.current.delete(item.id);
        queueRef.current = queueRef.current.filter(q => q.id !== item.id);
        setTimeout(processQueue, 100);
      });

      // Handle aborts
      xhr.addEventListener('abort', () => {
        setUploads(prev => prev.map(upload =>
          upload.id === item.id ? {
            ...upload,
            status: 'cancelled',
            message: 'Upload cancelled'
          } : upload
        ));
        
        abortControllersRef.current.delete(item.id);
        queueRef.current = queueRef.current.filter(q => q.id !== item.id);
        setTimeout(processQueue, 100);
      });

      // Prepare form data
      const formData = new FormData();
      formData.append('file', item.file);
      
      // Start upload
      xhr.open('POST', url);
      xhr.send(formData);

    } catch (error: any) {
      setUploads(prev => prev.map(upload =>
        upload.id === item.id ? {
          ...upload,
          status: 'error',
          message: error.message || 'Upload failed'
        } : upload
      ));
      
      abortControllersRef.current.delete(item.id);
      queueRef.current = queueRef.current.filter(q => q.id !== item.id);
      setTimeout(processQueue, 100);
    }
  }, [url, processQueue]);

  const startUpload = useCallback((files: File[]): Promise<any[]> => {
    const results: Promise<any>[] = [];
    
    files.forEach(file => {
      const validationError = validateFile(file);
      
      const uploadId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      const uploadItem: UploadItem = {
        id: uploadId,
        file,
        fileName: file.name,
        progress: 0,
        status: validationError ? 'error' : 'pending',
        message: validationError || undefined,
        retry: () => retryUpload(uploadId)
      };

      results.push(
        new Promise((resolve) => {
          // Store resolver for this upload
          uploadItem.retry = async () => {
            const retryResult = await retryUpload(uploadId);
            resolve(retryResult);
            return retryResult;
          };

          if (!validationError) {
            queueRef.current.push(uploadItem);
          } else {
            // Resolve immediately for invalid files
            resolve({ file: file.name, status: 'error', message: validationError });
          }
        })
      );
    });

    setUploads(prev => [...prev, ...files.map((file, index) => {
      const validationError = validateFile(file);
      return {
        id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        file,
        fileName: file.name,
        progress: 0,
        status: validationError ? 'error' as const : 'pending' as const,
        message: validationError || undefined,
        retry: () => retryUpload(`${Date.now()}-${Math.random().toString(36).substr(2, 9)}`),
      };
    })]);

    setTimeout(processQueue, 100);
    
    return Promise.all(results);
  }, [validateFile, processQueue]);

  const cancelUpload = useCallback((id: string) => {
    const abortController = abortControllersRef.current.get(id);
    if (abortController) {
      abortController.abort();
    }

    const upload = uploads.find(u => u.id === id);
    if (upload?.xhr) {
      upload.xhr.abort();
    }

    // Remove from queue
    queueRef.current = queueRef.current.filter(item => item.id !== id);
    
    setUploads(prev => prev.map(upload =>
      upload.id === id ? { ...upload, status: 'cancelled', message: 'Upload cancelled' } : upload
    ));
  }, [uploads]);

  const retryUpload = useCallback(async (id: string): Promise<any> => {
    const upload = uploads.find(u => u.id === id);
    if (!upload) return null;

    const validationError = validateFile(upload.file);
    if (validationError) {
      setUploads(prev => prev.map(u =>
        u.id === id ? { ...u, status: 'error', message: validationError } : u
      ));
      return { file: upload.fileName, status: 'error', message: validationError };
    }

    setUploads(prev => prev.map(u =>
      u.id === id ? { ...u, status: 'pending', progress: 0, message: 'Retrying...' } : u
    ));

    // Add back to queue
    if (!queueRef.current.find(item => item.id === id)) {
      queueRef.current.push(upload);
    }

    setTimeout(processQueue, 100);

    return new Promise((resolve) => {
      const checkStatus = () => {
        const currentUpload = uploads.find(u => u.id === id);
        if (currentUpload?.status === 'success') {
          resolve({
            file: currentUpload.fileName,
            status: 'success',
            doc_id: currentUpload.doc_id,
            aleph_id: currentUpload.aleph_id
          });
        } else if (currentUpload?.status === 'error') {
          resolve({
            file: currentUpload.fileName,
            status: 'error',
            message: currentUpload.message
          });
        } else {
          setTimeout(checkStatus, 1000);
        }
      };
      checkStatus();
    });
  }, [uploads, validateFile, processQueue]);

  const clearCompleted = useCallback(() => {
    setUploads(prev => prev.filter(upload => 
      upload.status !== 'success' && upload.status !== 'error' && upload.status !== 'cancelled'
    ));
  }, []);

  const clearAll = useCallback(() => {
    // Cancel all active uploads
    uploads.forEach(upload => {
      if (upload.status === 'uploading' || upload.status === 'pending') {
        cancelUpload(upload.id);
      }
    });
    
    setUploads([]);
    queueRef.current = [];
    abortControllersRef.current.clear();
  }, [uploads, cancelUpload]);

  return {
    uploads,
    startUpload,
    cancelUpload,
    retryUpload,
    clearCompleted,
    clearAll,
    stats: {
      total: uploads.length,
      pending: uploads.filter(u => u.status === 'pending').length,
      uploading: uploads.filter(u => u.status === 'uploading').length,
      completed: uploads.filter(u => u.status === 'success').length,
      failed: uploads.filter(u => u.status === 'error').length,
      cancelled: uploads.filter(u => u.status === 'cancelled').length
    }
  };
}
