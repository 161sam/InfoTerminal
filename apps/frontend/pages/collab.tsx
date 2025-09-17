import { useEffect, useMemo, useRef, useState } from 'react';
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
  const [tasks, setTasks] = useState<{ id: string; text: string; status: 'todo'|'doing'|'done' }[]>([]);
  const clientId = useMemo(() => Math.random().toString(36).slice(2), []);

  useEffect(() => {
    const url = wsUrl();
    const ws = new WebSocket(url);
    wsRef.current = ws;
    ws.onmessage = (ev) => {
      try {
        const msg = JSON.parse(ev.data);
        setMessages(prev => [...prev, msg]);
        if (msg.type === 'task_add') {
          setTasks(prev => prev.some(t => t.id === msg.task?.id) ? prev : [...prev, msg.task]);
        } else if (msg.type === 'task_move') {
          setTasks(prev => prev.map(t => t.id === msg.id ? { ...t, status: msg.to } : t));
        } else if (msg.type === 'task_delete') {
          setTasks(prev => prev.filter(t => t.id !== msg.id));
        }
      } catch {}
    };
    return () => { ws.close(); };
  }, []);

  // Fetch persisted tasks on mount
  useEffect(() => {
    fetch('/api/collab/tasks').then(r => r.json()).then(d => setTasks(d.items || [])).catch(() => {});
  }, []);

  const send = () => {
    if (!text.trim()) return;
    wsRef.current?.send(JSON.stringify({ type: 'note', text, clientId }));
    setText('');
  };

  const addTask = () => {
    const t = text.trim();
    if (!t) return;
    fetch('/api/collab/tasks', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: t }) })
      .then(r => r.json()).then(task => setTasks(prev => [...prev, task])).catch(() => {});
    setText('');
  };
  const moveTask = (id: string, to: 'todo'|'doing'|'done') => {
    fetch(`/api/collab/tasks/${id}/move`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ to }) })
      .then(() => setTasks(prev => prev.map(t => t.id === id ? { ...t, status: to } : t))).catch(() => {});
  };
  const deleteTask = (id: string) => {
    fetch(`/api/collab/tasks/${id}`, { method: 'DELETE' })
      .then(() => setTasks(prev => prev.filter(t => t.id !== id))).catch(() => {});
  };

  return (
    <DashboardLayout title="Collaboration" subtitle="Shared notes & audit stream">
      <div className="max-w-5xl mx-auto p-4 space-y-4">
        <Panel title="Notes & Tasks">
          <div className="flex items-center gap-2">
            <input className="flex-1 border rounded p-2" value={text} onChange={e => setText(e.target.value)} placeholder="Type a note and press send" />
            <button className="px-4 py-2 bg-primary-600 text-white rounded" onClick={send}>Send Note</button>
            <button className="px-4 py-2 bg-gray-800 text-white rounded" onClick={addTask}>Add Task</button>
          </div>
        </Panel>
        <Panel title="Board">
          <div className="grid grid-cols-3 gap-3">
            {(['todo','doing','done'] as const).map(col => (
              <div key={col} className="border rounded p-2">
                <div className="font-medium capitalize mb-2">{col}</div>
                <div className="space-y-2 min-h-[200px]">
                  {tasks.filter(t => t.status === col).map(t => (
                    <div key={t.id} className="p-2 border rounded bg-white">
                      <div className="text-sm">{t.text}</div>
                      <div className="mt-1 flex gap-1">
                        {col !== 'todo' && <button className="text-xs px-2 py-1 bg-gray-200 rounded" onClick={() => moveTask(t.id, col === 'doing' ? 'todo' : 'doing')}>{col === 'doing' ? '← Todo' : '← Doing'}</button>}
                        {col !== 'done' && <button className="text-xs px-2 py-1 bg-gray-200 rounded" onClick={() => moveTask(t.id, col === 'todo' ? 'doing' : 'done')}>{col === 'todo' ? 'Doing →' : 'Done →'}</button>}
                        <button className="text-xs px-2 py-1 bg-red-200 rounded" onClick={() => deleteTask(t.id)}>Delete</button>
                      </div>
                    </div>
                  ))}
                  {tasks.filter(t => t.status === col).length === 0 && (
                    <div className="text-xs text-gray-500">No tasks</div>
                  )}
                </div>
              </div>
            ))}
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
