// apps/frontend/src/components/upload/UploadBox.tsx
import React, { useRef, useState } from 'react';
import { Upload as UploadIcon, CheckCircle, XCircle, Clock, X, RotateCcw } from 'lucide-react';
import useFileUpload from '@/hooks/useFileUpload';
import UploadProgressBar from './UploadProgressBar';

type Props = {
  accept?: string[];
  multiple?: boolean;
  onComplete?: (results: any[]) => void;
};

type UploadItem = {
  id: string;
  fileName: string;
  status: 'pending' | 'uploading' | 'success' | 'error';
  progress: number;
  doc_id?: string;
  doc_url?: string;
  url?: string;
  result?: { id?: string; url?: string } | any;
  message?: string;
};

function resolveDocHref(u: UploadItem): string | undefined {
  if (u.doc_url) return u.doc_url;
  if (u.url) return u.url;
  if (u.result?.url) return u.result.url;
  const id = u.doc_id ?? u.result?.id;
  if (id) return `/documents/${id}`;
  return undefined;
}

export default function UploadBox({ accept, multiple, onComplete }: Props) {
  const { uploads, startUpload, cancelUpload, retryUpload } = useFileUpload();
  const inputRef = useRef<HTMLInputElement>(null);
  const [drag, setDrag] = useState(false);

  const handleFiles = (files: FileList | null) => {
    if (!files) return;
    startUpload(Array.from(files)).then((r) => onComplete && onComplete(r));
  };

  return (
    <div>
      <div
        onDragEnter={(e) => {
          e.preventDefault();
          setDrag(true);
        }}
        onDragOver={(e) => e.preventDefault()}
        onDragLeave={(e) => {
          e.preventDefault();
          setDrag(false);
        }}
        onDrop={(e) => {
          e.preventDefault();
          setDrag(false);
          handleFiles(e.dataTransfer.files);
        }}
        onClick={() => inputRef.current?.click()}
        className={`p-6 text-center cursor-pointer border-2 border-dashed rounded ${
          drag ? 'border-blue-400 bg-blue-50' : 'border-gray-300'
        }`}
      >
        <UploadIcon className="mx-auto mb-2" aria-hidden="true" />
        <p>Dateien hier ablegen oder klicken zum Auswählen</p>
        <input
          ref={inputRef}
          type="file"
          className="hidden"
          multiple={multiple}
          accept={accept?.join(',')}
          onChange={(e) => handleFiles(e.target.files)}
        />
      </div>

      <ul className="mt-4 space-y-2">
        {(uploads as UploadItem[]).map((u) => {
          const href = resolveDocHref(u);
          return (
            <li key={u.id} className="border p-2 rounded">
              <div className="flex items-center justify-between">
                <span>{u.fileName}</span>
                <div className="flex items-center space-x-2">
                  {(u.status === 'pending' || u.status === 'uploading') && (
                    <Clock className="w-4 h-4" aria-hidden="true" />
                  )}
                  {u.status === 'success' && (
                    <CheckCircle className="w-4 h-4 text-green-600" aria-hidden="true" />
                  )}
                  {u.status === 'error' && (
                    <XCircle className="w-4 h-4 text-red-600" aria-hidden="true" />
                  )}
                  {u.status === 'uploading' && (
                    <button onClick={() => cancelUpload(u.id)} aria-label="Cancel">
                      <X className="w-4 h-4" />
                    </button>
                  )}
                  {u.status === 'error' && (
                    <button onClick={() => retryUpload(u.id)} aria-label="Retry">
                      <RotateCcw className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>

              <UploadProgressBar progress={u.progress} status={u.status} />

              {u.status === 'success' && (
                <a className="text-blue-600 underline text-sm" href={href ?? '#'}>
                  Zum Dokument
                </a>
              )}

              {u.status === 'error' && u.message && (
                <p className="text-red-600 text-sm">{u.message}</p>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
