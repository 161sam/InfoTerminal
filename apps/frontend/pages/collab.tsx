import { useEffect, useRef, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';

function wsUrl() {
  const port = process.env.NEXT_PUBLIC_COLLAB_PORT || process.env.IT_PORT_COLLAB || '8625';
  return `ws://localhost:${port}/ws`;
}

export default function CollabPage() {
  const [messages, setMessages] = useState<any[]>([]);
  const [text, setText] = useState('');
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const url = wsUrl();
    const ws = new WebSocket(url);
    wsRef.current = ws;
    ws.onmessage = (ev) => {
      try { setMessages(prev => [...prev, JSON.parse(ev.data)]); } catch {}
    };
    return () => { ws.close(); };
  }, []);

  const send = () => {
    if (!text.trim()) return;
    wsRef.current?.send(JSON.stringify({ type: 'note', text }));
    setText('');
  };

  return (
    <DashboardLayout title="Collaboration" subtitle="Shared notes & audit stream">
      <div className="max-w-5xl mx-auto p-4 space-y-4">
        <Panel title="New note">
          <div className="flex items-center gap-2">
            <input className="flex-1 border rounded p-2" value={text} onChange={e => setText(e.target.value)} placeholder="Type a note and press send" />
            <button className="px-4 py-2 bg-primary-600 text-white rounded" onClick={send}>Send</button>
          </div>
        </Panel>
        <Panel title="Audit stream">
          <div className="space-y-2 max-h-[400px] overflow-auto">
            {messages.map((m, i) => (
              <div key={i} className="text-sm p-2 border rounded">
                <pre className="whitespace-pre-wrap">{JSON.stringify(m, null, 2)}</pre>
              </div>
            ))}
            {!messages.length && <div className="text-sm text-gray-500">No messages yet</div>}
          </div>
        </Panel>
      </div>
    </DashboardLayout>
  );
}

