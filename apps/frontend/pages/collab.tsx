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
  const [tasks, setTasks] = useState<{ id: string; text: string; status: 'todo'|'doing'|'done'; priority?: 'low'|'normal'|'high'|'critical'; labels?: string[] }[]>([]);
  const clientId = useMemo(() => Math.random().toString(36).slice(2), []);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [history, setHistory] = useState<typeof tasks[]>([]);
  const [future, setFuture] = useState<typeof tasks[]>([]);
  const [labelEdit, setLabelEdit] = useState<{ id: string; open: boolean; value: string }>({ id: '', open: false, value: '' });
  const [serverSync, setServerSync] = useState(true);
  const [suggestions, setSuggestions] = useState<string[]>([]);

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
        } else if (msg.type === 'task_update') {
          const ut = msg.task;
          if (ut?.id) setTasks(prev => prev.map(t => t.id === ut.id ? { ...t, ...ut } : t));
        } else if (msg.type === 'task_delete') {
          setTasks(prev => prev.filter(t => t.id !== msg.id));
        }
      } catch {}
    };
    return () => { ws.close(); };
  }, []);

  // Fetch persisted tasks and labels on mount
  useEffect(() => {
    fetch('/api/collab/tasks').then(r => r.json()).then(d => setTasks(d.items || [])).catch(() => {});
    fetch('/api/collab/labels').then(r => r.json()).then(d => setSuggestions((d.items||[]).map((x:any)=>x.label))).catch(() => {});
  }, []);

  // Keyboard shortcuts: undo/redo
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const mod = e.ctrlKey || e.metaKey;
      if (mod && e.key.toLowerCase() === 'z') {
        e.preventDefault(); undo();
      } else if ((mod && e.key.toLowerCase() === 'y') || (mod && e.shiftKey && e.key.toLowerCase() === 'z')) {
        e.preventDefault(); redo();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [history, future, tasks]);

  const snapshot = () => JSON.parse(JSON.stringify(tasks)) as typeof tasks;
  const pushHistory = () => setHistory(prev => [...prev, snapshot()]);
  const audit = (entry: any) => { if (serverSync) fetch('/api/collab/audit', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(entry) }).catch(()=>{}); };
  const applySnapshot = (snap: typeof tasks) => setTasks(JSON.parse(JSON.stringify(snap)));
  const undo = () => {
    if (!history.length) return;
    const last = history[history.length - 1];
    setFuture(prev => [snapshot(), ...prev]);
    setHistory(prev => prev.slice(0, -1));
    applySnapshot(last);
  };
  const redo = () => {
    if (!future.length) return;
    const next = future[0];
    setHistory(prev => [...prev, snapshot()]);
    setFuture(prev => prev.slice(1));
    applySnapshot(next);
  };

  const send = () => {
    if (!text.trim()) return;
    wsRef.current?.send(JSON.stringify({ type: 'note', text, clientId }));
    setText('');
  };

  const addTask = () => {
    const t = text.trim();
    if (!t) return;
    pushHistory(); setFuture([]);
    audit({ type: 'add', text: t });
    fetch('/api/collab/tasks', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: t }) })
      .then(r => r.json()).then(task => setTasks(prev => [...prev, task])).catch(() => {});
    setText('');
  };
  const moveTask = (id: string, to: 'todo'|'doing'|'done') => {
    pushHistory(); setFuture([]);
    audit({ type: 'move', id, to });
    fetch(`/api/collab/tasks/${id}/move`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ to }) })
      .then(() => setTasks(prev => prev.map(t => t.id === id ? { ...t, status: to } : t))).catch(() => {});
  };
  const deleteTask = (id: string) => {
    pushHistory(); setFuture([]);
    audit({ type: 'delete', id });
    fetch(`/api/collab/tasks/${id}`, { method: 'DELETE' })
      .then(() => setTasks(prev => prev.filter(t => t.id !== id))).catch(() => {});
  };

  const updateTask = (id: string, patch: any) => {
    pushHistory(); setFuture([]);
    audit({ type: 'update', id, patch });
    fetch(`/api/collab/tasks/${id}/update`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(patch) })
      .then(r => r.json()).then((t) => setTasks(prev => prev.map(x => x.id === id ? { ...x, ...t } : x))).catch(() => {});
  };

  const onDragStart = (e: React.DragEvent, id: string) => {
    e.dataTransfer.setData('text/task-id', id);
  };
  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };
  const onDrop = (e: React.DragEvent, col: 'todo'|'doing'|'done') => {
    e.preventDefault();
    const id = e.dataTransfer.getData('text/task-id');
    if (id) moveTask(id, col);
  };

  const prioColor = (p?: string) => p === 'high' ? 'border-red-400' : p === 'critical' ? 'border-red-600' : p === 'low' ? 'border-blue-300' : 'border-amber-300';
  const prioBadge = (p?: string) => p ? (p[0].toUpperCase() + p.slice(1)) : 'Normal';
  const allLabels = Array.from(new Set(tasks.flatMap(t => t.labels || [])));

  const onTaskKey = (e: React.KeyboardEvent, t: typeof tasks[number]) => {
    if (e.key === ' ') {
      e.preventDefault(); setSelectedId(prev => prev === t.id ? null : t.id);
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
      e.preventDefault();
      const order: ('todo'|'doing'|'done')[] = ['todo','doing','done'];
      const idx = order.indexOf(t.status);
      if (e.key === 'ArrowLeft' && idx > 0) moveTask(t.id, order[idx-1]);
      if (e.key === 'ArrowRight' && idx < order.length-1) moveTask(t.id, order[idx+1]);
    }
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
        <Panel title="Board (Drag & Drop / Keyboard)">
          <div className="flex items-center gap-2 mb-2">
            <button className="px-3 py-1 text-xs bg-gray-200 rounded" onClick={undo} disabled={!history.length}>Undo</button>
            <button className="px-3 py-1 text-xs bg-gray-200 rounded" onClick={redo} disabled={!future.length}>Redo</button>
            <span className="text-xs text-gray-500">Shortcuts: Ctrl/Cmd+Z, Ctrl+Y / Shift+Ctrl/Cmd+Z</span>
            <label className="ml-auto text-xs flex items-center gap-1">
              <input type="checkbox" checked={serverSync} onChange={e => setServerSync(e.target.checked)} /> Server Sync (audit)
            </label>
          </div>
          <div className="grid grid-cols-3 gap-3">
            {(['todo','doing','done'] as const).map(col => (
              <div key={col} className="border rounded p-2" onDragOver={onDragOver} onDrop={(e) => onDrop(e, col)}>
                <div className="font-medium capitalize mb-2">{col}</div>
                <div className="space-y-2 min-h-[200px]">
                  {tasks.filter(t => t.status === col).map(t => (
                    <div
                      key={t.id}
                      className={`p-2 border-l-4 rounded bg-white ${prioColor(t.priority)} shadow-sm outline-none ${selectedId===t.id?'ring-2 ring-primary-400':''}`}
                      draggable
                      onDragStart={(e) => onDragStart(e, t.id)}
                      tabIndex={0}
                      onKeyDown={(e) => onTaskKey(e, t)}
                      onFocus={() => setSelectedId(t.id)}
                    >
                      <div className="text-xs flex items-center gap-2 mb-1">
                        <span className={`px-2 py-0.5 rounded-full ${t.priority==='high'||t.priority==='critical'?'bg-red-100 text-red-700':t.priority==='low'?'bg-blue-100 text-blue-700':'bg-amber-100 text-amber-700'}`}>{prioBadge(t.priority)}</span>
                        {(t.labels||[]).map((lb, i) => (
                          <span key={i} className="px-2 py-0.5 rounded-full bg-gray-100 text-gray-700">{lb}</span>
                        ))}
                        <button className="ml-auto text-xs px-2 py-0.5 bg-gray-100 rounded" onClick={() => setLabelEdit({ id: t.id, open: true, value: '' })}>Labels</button>
                      </div>
                      <div className="text-sm">{t.text}</div>
                      <div className="mt-1 flex gap-1">
                        {col !== 'todo' && <button className="text-xs px-2 py-1 bg-gray-200 rounded" onClick={() => moveTask(t.id, col === 'doing' ? 'todo' : 'doing')}>{col === 'doing' ? '← Todo' : '← Doing'}</button>}
                        {col !== 'done' && <button className="text-xs px-2 py-1 bg-gray-200 rounded" onClick={() => moveTask(t.id, col === 'todo' ? 'doing' : 'done')}>{col === 'todo' ? 'Doing →' : 'Done →'}</button>}
                        <button className="text-xs px-2 py-1 bg-red-200 rounded" onClick={() => deleteTask(t.id)}>Delete</button>
                        <select value={t.priority||'normal'} onChange={(e) => updateTask(t.id, { priority: e.target.value })} className="text-xs px-2 py-1 border rounded">
                          <option value="low">Low</option>
                          <option value="normal">Normal</option>
                          <option value="high">High</option>
                          <option value="critical">Critical</option>
                        </select>
                      </div>
                      {labelEdit.open && labelEdit.id===t.id && (
                        <div className="mt-2 p-2 border rounded bg-gray-50">
                          <div className="flex items-center gap-2">
                            <input className="flex-1 border rounded p-1 text-xs" placeholder="Add label..." value={labelEdit.value} onChange={e => setLabelEdit(prev => ({...prev, value: e.target.value}))} list="labels-suggestions" />
                            <datalist id="labels-suggestions">
                              {Array.from(new Set([...allLabels, ...suggestions])).map((l, i) => (<option key={i} value={l} />))}
                            </datalist>
                            <button className="text-xs px-2 py-1 bg-gray-200 rounded" onClick={() => {
                              const v = (labelEdit.value||'').trim(); if (!v) return;
                              const labels = Array.from(new Set([...(t.labels||[]), v]));
                              updateTask(t.id, { labels });
                              setLabelEdit({ id: '', open: false, value: '' });
                            }}>Add</button>
                            <button className="text-xs px-2 py-1 bg-gray-100 rounded" onClick={() => setLabelEdit({ id: '', open: false, value: '' })}>Close</button>
                          </div>
                          <div className="mt-2 flex flex-wrap gap-1">
                            {(t.labels||[]).map((lb, i) => (
                              <span key={i} className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-gray-200 text-xs">
                                {lb}
                                <button className="text-[10px]" onClick={() => {
                                  const next = (t.labels||[]).filter(x => x !== lb);
                                  updateTask(t.id, { labels: next });
                                }}>✕</button>
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
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
