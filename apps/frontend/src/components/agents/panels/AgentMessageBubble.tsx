import React from "react";
import {
  Bot,
  User,
  Settings,
  Clock,
  Copy,
  AlertCircle,
  CheckCircle,
  ChevronDown,
  ChevronRight,
} from "lucide-react";
import { Message, AgentCapability, CAPABILITY_COLORS } from "./types";

interface AgentMessageBubbleProps {
  message: Message;
  showSteps: { [key: string]: boolean };
  setShowSteps: React.Dispatch<React.SetStateAction<{ [key: string]: boolean }>>;
  copyToClipboard: (text: string) => void;
  agentCapabilities: AgentCapability[];
}

export default function AgentMessageBubble({
  message,
  showSteps,
  setShowSteps,
  copyToClipboard,
  agentCapabilities,
}: AgentMessageBubbleProps) {
  const isUser = message.role === "user";
  const isSystem = message.role === "system";
  const capability = agentCapabilities.find((c) => c.id === message.agentType);

  const toggleSteps = () => {
    setShowSteps((prev) => ({
      ...prev,
      [message.id]: !prev[message.id],
    }));
  };

  return (
    <div className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div
          className={`flex items-center justify-center w-8 h-8 rounded-full flex-shrink-0 ${
            isSystem
              ? "bg-orange-100 text-orange-600 dark:bg-orange-900/20 dark:text-orange-400"
              : capability
                ? CAPABILITY_COLORS[capability.color as keyof typeof CAPABILITY_COLORS]
                : "bg-blue-100 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400"
          }`}
        >
          {isSystem ? (
            <Settings size={16} />
          ) : capability ? (
            <capability.icon size={16} />
          ) : (
            <Bot size={16} />
          )}
        </div>
      )}

      <div className={`max-w-3xl ${isUser ? "order-first" : ""}`}>
        <div
          className={`p-3 rounded-lg ${
            isUser
              ? "bg-primary-600 text-white"
              : isSystem
                ? "bg-orange-50 text-orange-900 border border-orange-200 dark:bg-orange-900/20 dark:text-orange-300 dark:border-orange-900/30"
                : "bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-100"
          }`}
        >
          <div className="prose prose-sm max-w-none">
            <p className="whitespace-pre-wrap m-0">{message.content}</p>
          </div>
        </div>

        {/* Message Metadata */}
        <div className="flex items-center gap-2 mt-1 text-xs text-gray-500 dark:text-slate-400 flex-wrap">
          <span>{message.timestamp.toLocaleTimeString()}</span>

          {message.role === "assistant" && capability && (
            <>
              <span>•</span>
              <span className="inline-flex items-center gap-1">
                <capability.icon size={12} />
                {capability.displayName}
              </span>
            </>
          )}

          {message.toolsUsed && message.toolsUsed.length > 0 && (
            <>
              <span>•</span>
              <div className="flex flex-wrap gap-1">
                {message.toolsUsed.map((tool) => (
                  <span
                    key={tool}
                    className="px-1 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-xs"
                  >
                    {tool}
                  </span>
                ))}
              </div>
            </>
          )}

          {message.executionTime && (
            <>
              <span>•</span>
              <span className="inline-flex items-center gap-1">
                <Clock size={12} />
                {message.executionTime.toFixed(2)}s
              </span>
            </>
          )}

          <button
            onClick={() => copyToClipboard(message.content)}
            className="ml-auto p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded"
            title="Copy message"
          >
            <Copy size={12} />
          </button>
        </div>

        {/* Enhanced Steps and References */}
        {(message.steps?.length || message.references) && (
          <div className="mt-2 space-y-2">
            {message.steps && message.steps.length > 0 && (
              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg">
                <button
                  onClick={toggleSteps}
                  className="w-full flex items-center justify-between p-2 text-xs font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
                >
                  <span>Execution Steps ({message.steps.length})</span>
                  {showSteps[message.id] ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                </button>

                {showSteps[message.id] && (
                  <div className="p-2 space-y-2 border-t border-gray-200 dark:border-gray-700">
                    {message.steps.map((step, idx) => (
                      <div key={idx} className="flex items-start gap-2">
                        {step.error ? (
                          <AlertCircle className="h-3 w-3 text-red-500 mt-0.5" />
                        ) : (
                          <CheckCircle className="h-3 w-3 text-green-500 mt-0.5" />
                        )}
                        <div className="flex-1 text-xs">
                          <div className="font-medium">{step.tool}</div>
                          {step.error ? (
                            <div className="text-red-600 dark:text-red-400">{step.error}</div>
                          ) : (
                            <div className="text-gray-600 dark:text-gray-400">
                              {step.result ? "Completed successfully" : "Processing..."}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {message.references && (
              <details className="bg-gray-50 dark:bg-gray-900 rounded-lg">
                <summary className="cursor-pointer p-2 text-xs font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg">
                  References & Citations
                </summary>
                <pre className="mt-1 p-2 text-xs overflow-auto border-t border-gray-200 dark:border-gray-700">
                  {JSON.stringify(message.references, null, 2)}
                </pre>
              </details>
            )}
          </div>
        )}
      </div>

      {isUser && (
        <div className="flex items-center justify-center w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex-shrink-0 dark:bg-primary-900/20 dark:text-primary-400">
          <User size={16} />
        </div>
      )}
    </div>
  );
}
