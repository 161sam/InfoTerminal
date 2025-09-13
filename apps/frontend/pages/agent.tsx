import { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { getApis } from '@/lib/config';

type Msg = { role: string; content: string; steps?: any; references?: any };

export default function AgentPage() {
  const { AGENT_API } = getApis();
  const [messages, setMessages] = useState<Msg[]>([]);
  const [text, setText] = useState('');
  const [workflowStatus, setWorkflowStatus] = useState<string | null>(null);
  const [healthy, setHealthy] = useState<boolean | null>(null);
  const n8nConfigured = Boolean(process.env.NEXT_PUBLIC_N8N_URL);

  const checkHealth = () => {
    fetch(`${AGENT_API}/healthz`)
      .then((r) => setHealthy(r.ok))
      .catch(() => setHealthy(false));
  };

  useEffect(() => {
    checkHealth();
  }, [AGENT_API]);

  const send = async () => {
    const body = { messages: [...messages.map(({ steps, references, ...m }) => m), { role: 'user', content: text }] };
    try {
      const res = await fetch(`${AGENT_API}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      setMessages([
        ...body.messages,
        { role: 'assistant', content: data.reply || '', steps: data.steps, references: data.references },
      ]);
      setText('');
    } catch (e: any) {
      setHealthy(false);
      setMessages((m) => [...m, { role: 'system', content: e.message || 'agent not reachable' }]);
    }
  };

  const runPlaybook = async (name: string) => {
    try {
      const res = await fetch(`${AGENT_API}/playbooks/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, params: { q: text } }),
      });
      const data = await res.json();
      setMessages((m) => [...m, { role: 'system', content: JSON.stringify(data) }]);
    } catch (e: any) {
      setHealthy(false);
      setMessages((m) => [...m, { role: 'system', content: e.message || 'playbook failed' }]);
    }
  };

  const runWorkflow = async () => {
    if (!n8nConfigured) {
      setWorkflowStatus('n8n not configured');
      return;
    }
    try {
      const res = await fetch(`${AGENT_API}/workflows/trigger`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      });
      const data = await res.json();
      setWorkflowStatus(data.runId ? `started ${data.runId}` : 'ok');
      setMessages((m) => [...m, { role: 'system', content: JSON.stringify(data) }]);
    } catch (e: any) {
      const msg = e.message || 'workflow failed';
      setWorkflowStatus(msg);
      setHealthy(false);
      setMessages((m) => [...m, { role: 'system', content: msg }]);
    }
  };

  return (
    <DashboardLayout title="Agent">
      <div className="p-4 space-y-4">
        {healthy === false && (
          <div className="p-2 rounded bg-yellow-100 text-yellow-800 flex items-center gap-2">
            Service nicht erreichbar – ist der Container gestartet? (agent-connector)
            <button onClick={checkHealth} className="underline">
              Retry
            </button>
          </div>
        )}
        <div className="space-y-2">
        {messages.map((m, i) => (
          <div key={i} className="border p-2 rounded">
            <strong>{m.role}:</strong> {m.content}
            {m.steps && <pre className="bg-gray-100 p-2 mt-1 text-xs overflow-auto">{JSON.stringify(m.steps, null, 2)}</pre>}
            {m.references && (
              <pre className="bg-gray-100 p-2 mt-1 text-xs overflow-auto">{JSON.stringify(m.references, null, 2)}</pre>
            )}
          </div>
        ))}
      </div>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="w-full border p-2 rounded"
      />
        <div className="flex gap-2">
        <button onClick={send} className="px-4 py-2 bg-blue-600 text-white rounded">
          Send
        </button>
        <button
          onClick={() => runPlaybook('InvestigatePerson')}
          className="px-4 py-2 bg-green-600 text-white rounded"
        >
          InvestigatePerson
        </button>
        <button
          onClick={() => runPlaybook('FinancialRiskAssistant')}
          className="px-4 py-2 bg-amber-600 text-white rounded"
        >
          Financial Risk Assistant
        </button>
        <div className="flex flex-col gap-1">
          <button onClick={runWorkflow} className="px-4 py-2 bg-purple-600 text-white rounded">
            Run n8n
          </button>
          {workflowStatus && <span className="text-xs text-gray-600">{workflowStatus}</span>}
        </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
