import { useRef, useState } from 'react';

export type UploadStatus = 'pending' | 'uploading' | 'success' | 'error';

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
  resolver?: (r: any) => void;
}

export default function useFileUpload(url: string = '/api/documents/upload') {
  const [uploads, setUploads] = useState<UploadItem[]>([]);
  const queueRef = useRef<UploadItem[]>([]);
  const maxConcurrent = 3;

  function processQueue() {
    const active = uploads.filter(u => u.status === 'uploading').length;
    while (queueRef.current.length > 0 && active + queueRef.current.filter(u => u.status === 'uploading').length < maxConcurrent) {
      const item = queueRef.current.shift()!;
      uploadSingle(item);
    }
  }

  function uploadSingle(item: UploadItem) {
    setUploads(u => u.map(it => (it.id === item.id ? { ...it, status: 'uploading', progress: 0 } : it)));
    const xhr = new XMLHttpRequest();
    item.xhr = xhr;
    xhr.upload.onprogress = (e: ProgressEvent) => {
      if (e.lengthComputable) {
        const prog = Math.round((e.loaded / e.total) * 100);
        setUploads(u => u.map(it => (it.id === item.id ? { ...it, progress: prog } : it)));
      }
    };
    xhr.onreadystatechange = () => {
      if (xhr.readyState === 4) {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            const resp = JSON.parse(xhr.responseText);
            const result = resp.results?.[0];
            setUploads(u =>
              u.map(it =>
                it.id === item.id
                  ? { ...it, status: 'success', progress: 100, doc_id: result?.doc_id, aleph_id: result?.aleph_id }
                  : it
              )
            );
            item.resolver && item.resolver(result);
          } catch {
            setUploads(u => u.map(it => (it.id === item.id ? { ...it, status: 'error', message: 'invalid response' } : it)));
            item.resolver && item.resolver({ file: item.fileName, status: 'error', message: 'invalid response' });
          }
        } else {
          setUploads(u => u.map(it => (it.id === item.id ? { ...it, status: 'error', message: 'upload failed' } : it)));
          item.resolver && item.resolver({ file: item.fileName, status: 'error', message: 'upload failed' });
        }
        processQueue();
      }
    };
    xhr.onerror = () => {
      setUploads(u => u.map(it => (it.id === item.id ? { ...it, status: 'error', message: 'network error' } : it)));
      item.resolver && item.resolver({ file: item.fileName, status: 'error', message: 'network error' });
      processQueue();
    };
    xhr.onabort = () => {
      setUploads(u => u.map(it => (it.id === item.id ? { ...it, status: 'error', message: 'aborted' } : it)));
      item.resolver && item.resolver({ file: item.fileName, status: 'error', message: 'aborted' });
      processQueue();
    };
    const formData = new FormData();
    formData.append('file', item.file);
    xhr.open('POST', url);
    xhr.send(formData);
  }

  function startUpload(files: File[]) {
    const newItems: UploadItem[] = files.map(f => ({
      id: crypto.randomUUID(),
      file: f,
      fileName: f.name,
      progress: 0,
      status: 'pending'
    }));
    const promises = newItems.map(item =>
      new Promise(resolve => {
        item.resolver = resolve;
      })
    );
    setUploads(u => [...u, ...newItems]);
    queueRef.current.push(...newItems);
    processQueue();
    return Promise.all(promises);
  }

  function cancelUpload(id: string) {
    const item = uploads.find(u => u.id === id);
    item?.xhr?.abort();
  }

  function retryUpload(id: string) {
    const item = uploads.find(u => u.id === id);
    if (item) {
      item.status = 'pending';
      item.progress = 0;
      queueRef.current.push(item);
      const promise = new Promise(resolve => {
        item.resolver = resolve;
      });
      processQueue();
      return promise;
    }
  }

  return { uploads, startUpload, cancelUpload, retryUpload };
}
