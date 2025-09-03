import React from 'react';
import { UploadStatus } from '../../hooks/useFileUpload';

type Props = {
  progress: number;
  status: UploadStatus;
};

export default function UploadProgressBar({ progress, status }: Props) {
  let barClass = 'bg-gray-300';
  if (status === 'uploading') barClass = 'bg-blue-500';
  if (status === 'success') barClass = 'bg-green-500';
  if (status === 'error') barClass = 'bg-red-500';
  return (
    <div className="w-full h-2 bg-gray-200">
      <div
        className={`${barClass} h-2`}
        style={{ width: `${status === 'uploading' ? progress : 100}%` }}
      >
        {status === 'error' && (
          <span className="text-xs text-white ml-1">Error</span>
        )}
      </div>
    </div>
  );
}
