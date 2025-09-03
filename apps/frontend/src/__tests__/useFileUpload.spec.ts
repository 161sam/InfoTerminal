import { renderHook, act } from '@testing-library/react';
import useFileUpload from '../hooks/useFileUpload';
import { vi } from 'vitest';

declare const global: any;

class MockXHR {
  upload: any = {};
  readyState = 0;
  status = 0;
  responseText = '';
  onreadystatechange: any;
  onerror: any;
  onabort: any;
  open() {}
  send() {
    setTimeout(() => {
      this.readyState = 4;
      this.status = 200;
      this.responseText = JSON.stringify({ ok: true, results: [{ file: 'a.txt', status: 'uploaded', doc_id: '1' }] });
      this.onreadystatechange && this.onreadystatechange();
    }, 0);
    setTimeout(() => {
      this.upload.onprogress && this.upload.onprogress({ lengthComputable: true, loaded: 5, total: 5 });
    }, 0);
  }
  abort() {
    this.onabort && this.onabort();
  }
}

global.XMLHttpRequest = MockXHR as any;

test('uploads file and updates progress', async () => {
  const file = new File(['hello'], 'a.txt', { type: 'text/plain' });
  const { result } = renderHook(() => useFileUpload('/api/documents/upload'));
  await act(async () => {
    await result.current.startUpload([file]);
  });
  const upload = result.current.uploads[0];
  expect(upload.status).toBe('success');
  expect(upload.progress).toBe(100);
  expect(upload.doc_id).toBe('1');
});
