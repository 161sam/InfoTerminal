import { useState } from 'react';
import config from '@/lib/config';

export default function AgentPage() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [text, setText] = useState('');

  const send = async () => {
    const body = { messages: [...messages, { role: 'user', content: text }] };
    const res = await fetch(`${config.GATEWAY_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    setMessages([...body.messages, { role: 'assistant', content: data.reply || JSON.stringify(data) }]);
    setText('');
  };

  const runPlaybook = async (name: string) => {
    const res = await fetch(`${config.GATEWAY_URL}/playbooks/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    });
    const data = await res.json();
    setMessages((m) => [...m, { role: 'system', content: JSON.stringify(data) }]);
  };

  return (
    <div className="p-4 space-y-4">
      <div className="space-y-2">
        {messages.map((m, i) => (
          <div key={i} className="border p-2 rounded">
            <strong>{m.role}:</strong> {m.content}
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
      </div>
    </div>
  );
}
