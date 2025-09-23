import { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { Bot, MessageSquare, ShieldAlert } from 'lucide-react';

import DashboardLayout from '@/components/layout/DashboardLayout';
import { isAgentEnabled } from '@/lib/config';

interface ToolParameter {
  name: string;
  label: string;
  type: 'text' | 'number' | 'boolean';
  required?: boolean;
  placeholder?: string;
}

interface ToolOption {
  id: string;
  label: string;
  description: string;
  parameters: ToolParameter[];
  defaultParams: Record<string, unknown>;
}

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'tool';
  content: string;
  status?: 'pending' | 'success' | 'error';
  details?: any;
}

const TOOL_OPTIONS: ToolOption[] = [
  {
    id: 'search',
    label: 'search',
    description: 'Mocked document search over the offline knowledge base.',
    parameters: [
      { name: 'query', label: 'Query', type: 'text', required: true, placeholder: 'e.g. renewable energy policy' },
      { name: 'limit', label: 'Limit', type: 'number', placeholder: '5' }
    ],
    defaultParams: { limit: 5 }
  },
  {
    id: 'graph.query',
    label: 'graph.query',
    description: 'Run a canned Cypher query against the demo graph dataset.',
    parameters: [
      { name: 'cypher', label: 'Cypher', type: 'text', required: true, placeholder: 'MATCH (n) RETURN n LIMIT 5' }
    ],
    defaultParams: { parameters: {} }
  },
  {
    id: 'dossier.build',
    label: 'dossier.build',
    description: 'Compose a dossier summary using search + graph mocks.',
    parameters: [
      { name: 'subject', label: 'Subject', type: 'text', required: true, placeholder: 'ACME Corp' },
      { name: 'include_sources', label: 'Include sources', type: 'boolean' }
    ],
    defaultParams: { include_sources: true }
  }
];

const initialMessage: ChatMessage = {
  id: 'intro',
  role: 'assistant',
  content: 'Select a tool, type a prompt, and submit to execute a single mocked tool call.'
};

export default function AgentMvpChatPage() {
  const agentEnabled = isAgentEnabled();
  const router = useRouter();
  const [selectedTool, setSelectedTool] = useState<string>('dossier.build');
  const [prompt, setPrompt] = useState<string>('Draft a dossier overview for ACME Corp');
  const [conversationId, setConversationId] = useState<string>('demo-seed');
  const [formValues, setFormValues] = useState<Record<string, string | boolean>>({
    subject: 'ACME Corp',
    include_sources: true
  });
  const [messages, setMessages] = useState<ChatMessage[]>([initialMessage]);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const toolConfig = useMemo(() => TOOL_OPTIONS.find((tool) => tool.id === selectedTool) ?? TOOL_OPTIONS[0], [selectedTool]);

  const handleToolChange = (toolId: string) => {
    setSelectedTool(toolId);
    const tool = TOOL_OPTIONS.find((item) => item.id === toolId);
    if (!tool) {
      return;
    }
    const defaults = Object.entries(tool.defaultParams).reduce<Record<string, string | boolean>>((acc, [key, value]) => {
      if (typeof value === 'boolean') {
        acc[key] = value;
      } else {
        acc[key] = String(value ?? '');
      }
      return acc;
    }, {});
    setFormValues(defaults);
  };

  const parseFormValues = () => {
    const params: Record<string, unknown> = {};
    toolConfig.parameters.forEach((param) => {
      const raw = formValues[param.name];
      if (raw === undefined || raw === '') {
        return;
      }
      if (param.type === 'number') {
        const parsed = Number(raw);
        if (!Number.isNaN(parsed)) {
          params[param.name] = parsed;
        }
      } else if (param.type === 'boolean') {
        params[param.name] = raw === true || raw === 'true';
      } else {
        params[param.name] = raw;
      }
    });
    return params;
  };

  useEffect(() => {
    setConversationId(`demo-${Date.now()}`);
  }, []);

  const activeConversationId = conversationId || 'demo-seed';

  const submitPrompt = async () => {
    if (!prompt.trim()) {
      setErrorMessage('Enter a prompt for the agent.');
      return;
    }
    if (!agentEnabled) {
      setErrorMessage('Agent features are disabled.');
      return;
    }

    const params = parseFormValues();
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: prompt.trim()
    };
    const toolMessageId = `tool-${Date.now()}`;
    const toolMessage: ChatMessage = {
      id: toolMessageId,
      role: 'tool',
      content: `tool_call: ${selectedTool}`,
      status: 'pending',
      details: { params }
    };

    setMessages((prev) => [...prev, userMessage, toolMessage]);
    setSubmitting(true);
    setErrorMessage(null);

    try {
      const response = await fetch('/api/agent/mvp-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: prompt.trim(),
          tool: selectedTool,
          toolParams: params,
          conversationId: activeConversationId
        })
      });

      const payload = await response.json();

      if (!response.ok) {
        const policyDetail = payload?.detail;
        const readableError =
          policyDetail?.message || payload?.error || policyDetail?.error || 'Agent request denied.';
        setMessages((prev) =>
          prev.map((message) =>
            message.id === toolMessageId
              ? {
                  ...message,
                  status: 'error',
                  content: `tool_call: ${selectedTool} ❌`,
                  details: { error: readableError, policy: policyDetail }
                }
              : message
          )
        );
        setErrorMessage(readableError);
        return;
      }

      setMessages((prev) =>
        prev.map((message) =>
          message.id === toolMessageId
            ? {
                ...message,
                status: 'success',
                content: `tool_call: ${selectedTool} ✅`,
                details: {
                  params,
                  result: payload.tool_call?.result,
                  steps: payload.steps
                }
              }
            : message
        )
      );

      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: payload.reply || 'No reply returned from agent.',
        details: {
          steps: payload.steps,
          toolCall: payload.tool_call
        }
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      setMessages((prev) =>
        prev.map((message) =>
          message.id === toolMessageId
            ? {
                ...message,
                status: 'error',
                content: `tool_call: ${selectedTool} ❌`,
                details: { error: error?.message ?? 'Unknown failure' }
              }
            : message
        )
      );
      setErrorMessage('Agent connector unreachable.');
    } finally {
      setSubmitting(false);
    }
  };

  if (!agentEnabled) {
    return (
      <DashboardLayout title="Agent MVP" subtitle="Feature flag AGENTS_ENABLED=1 required">
        <div className="mx-auto max-w-2xl rounded-lg border border-dashed border-gray-300 bg-white p-8 text-center shadow-sm">
          <ShieldAlert className="mx-auto mb-4 h-12 w-12 text-amber-500" />
          <h2 className="mb-2 text-xl font-semibold">Agent services disabled</h2>
          <p className="text-sm text-gray-600">
            Enable the agent stack by exporting <code className="rounded bg-gray-100 px-1">AGENTS_ENABLED=1</code> before starting the
            Flowise connector service.
          </p>
          <p className="mt-4 text-sm text-gray-500">
            Review <Link href="/docs" className="text-primary-600 underline">docs/agents/quickstart.md</Link> for setup steps.
          </p>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Agent MVP Chat" subtitle="Single-turn agent demo with mocked tool calls">
      <div className="mx-auto grid max-w-5xl gap-6 lg:grid-cols-[320px,1fr]">
        <section className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold text-gray-800">
            <Bot className="h-5 w-5 text-primary-600" /> Tool configuration
          </h2>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-700">Select Tool</label>
              <select
                className="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none"
                value={selectedTool}
                onChange={(event) => handleToolChange(event.target.value)}
              >
                {TOOL_OPTIONS.map((tool) => (
                  <option key={tool.id} value={tool.id}>
                    {tool.label}
                  </option>
                ))}
              </select>
              <p className="mt-2 text-xs text-gray-500">{toolConfig.description}</p>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700">Prompt</label>
              <textarea
                className="mt-1 h-24 w-full rounded-md border border-gray-300 p-3 text-sm shadow-sm focus:border-primary-500 focus:outline-none"
                value={prompt}
                onChange={(event) => setPrompt(event.target.value)}
              />
            </div>

            <div className="space-y-3">
              {toolConfig.parameters.map((param) => (
                <div key={param.name}>
                  <label className="text-sm font-medium text-gray-700">{param.label}</label>
                  {param.type === 'boolean' ? (
                    <select
                      className="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none"
                      value={formValues[param.name] ? 'true' : 'false'}
                      onChange={(event) =>
                        setFormValues((prev) => ({
                          ...prev,
                          [param.name]: event.target.value === 'true'
                        }))
                      }
                    >
                      <option value="true">true</option>
                      <option value="false">false</option>
                    </select>
                  ) : (
                    <input
                      className="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none"
                      type={param.type === 'number' ? 'number' : 'text'}
                      placeholder={param.placeholder}
                      value={String(formValues[param.name] ?? '')}
                      onChange={(event) =>
                        setFormValues((prev) => ({
                          ...prev,
                          [param.name]: event.target.value
                        }))
                      }
                      required={param.required}
                    />
                  )}
                </div>
              ))}
            </div>

            {errorMessage && (
              <div className="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600">
                {errorMessage}
              </div>
            )}

            <button
              className="flex w-full items-center justify-center gap-2 rounded-md bg-primary-600 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-700 focus:outline-none"
              onClick={submitPrompt}
              disabled={submitting}
            >
              <MessageSquare className="h-4 w-4" /> {submitting ? 'Executing…' : 'Send prompt'}
            </button>
          </div>
        </section>

        <section className="flex flex-col rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-lg font-semibold text-gray-800">Conversation</h2>
          <div className="flex-1 space-y-4 overflow-y-auto">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`rounded-lg border p-4 text-sm shadow-sm ${
                  message.role === 'user'
                    ? 'border-primary-200 bg-primary-50'
                    : message.role === 'assistant'
                    ? 'border-emerald-200 bg-emerald-50'
                    : 'border-gray-200 bg-gray-50'
                }`}
              >
                <div className="mb-2 flex items-center justify-between">
                  <span className="font-semibold capitalize">{message.role}</span>
                  {message.status && (
                    <span
                      className={`text-xs font-medium ${
                        message.status === 'pending'
                          ? 'text-amber-600'
                          : message.status === 'success'
                          ? 'text-emerald-600'
                          : 'text-red-600'
                      }`}
                    >
                      {message.status === 'pending' && 'in progress'}
                      {message.status === 'success' && 'completed'}
                      {message.status === 'error' && 'error'}
                    </span>
                  )}
                </div>
                <p className="whitespace-pre-wrap text-gray-800">{message.content}</p>
                {message.details?.error && (
                  <p className="mt-2 text-xs text-red-600">{message.details.error}</p>
                )}
                {message.details?.result && (
                  <div className="mt-3 rounded-md bg-white/80 p-3 text-xs text-gray-700">
                    <div className="font-semibold">Mock result</div>
                    <p className="mt-1 text-gray-600">{message.details.result.summary}</p>
                  </div>
                )}
                {Array.isArray(message.details?.steps) && message.details.steps.length > 0 && (
                  <ul className="mt-3 space-y-1 text-xs text-gray-600">
                    {message.details.steps.map((step: any, index: number) => (
                      <li key={`${message.id}-step-${index}`} className="flex items-center gap-2">
                        <span className="h-2 w-2 rounded-full bg-emerald-500" aria-hidden />
                        <span>
                          {step.status} – {step.tool} @ {new Date(step.timestamp).toLocaleTimeString()}
                        </span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
          <div className="mt-4 rounded-md border border-dashed border-gray-200 bg-gray-50 p-4 text-xs text-gray-600">
            Conversation ID: <span className="font-mono">{activeConversationId}</span>
          </div>
        </section>
      </div>
      <div className="mx-auto mt-8 max-w-5xl rounded-lg border border-gray-200 bg-white p-4 text-sm text-gray-600 shadow-sm">
        Looking for the full agent console? Return to{' '}
        <button className="text-primary-600 underline" onClick={() => router.push('/agent')}>
          the main agent platform
        </button>
        .
      </div>
    </DashboardLayout>
  );
}
