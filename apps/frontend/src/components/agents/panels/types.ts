// Agent panel types and interfaces
export interface Message { 
  role: 'user' | 'assistant' | 'system'; 
  content: string; 
  steps?: ExecutionStep[]; 
  references?: any;
  timestamp: Date;
  id: string;
  agentType?: string;
  toolsUsed?: string[];
  confidence?: number;
  executionTime?: number;
}

export interface ExecutionStep {
  type: string;
  tool: string;
  parameters: any;
  result: any;
  error?: string;
  timestamp: string;
}

export interface AgentCapability {
  id: string;
  name: string;
  displayName: string;
  description: string;
  icon: any; // LucideIcon
  color: string;
  tools: string[];
  expertise: string[];
}

export interface AgentStatus {
  healthy: boolean;
  version?: string;
  capabilities?: string[];
  uptime?: number;
  lastCheck?: Date;
}

export const CAPABILITY_COLORS = {
  blue: 'bg-blue-50 border-blue-200 text-blue-800 hover:bg-blue-100 dark:bg-blue-900/20 dark:border-blue-900/30 dark:text-blue-300',
  purple: 'bg-purple-50 border-purple-200 text-purple-800 hover:bg-purple-100 dark:bg-purple-900/20 dark:border-purple-900/30 dark:text-purple-300',
  red: 'bg-red-50 border-red-200 text-red-800 hover:bg-red-100 dark:bg-red-900/20 dark:border-red-900/30 dark:text-red-300',
  green: 'bg-green-50 border-green-200 text-green-800 hover:bg-green-100 dark:bg-green-900/20 dark:border-green-900/30 dark:text-green-300',
  indigo: 'bg-indigo-50 border-indigo-200 text-indigo-800 hover:bg-indigo-100 dark:bg-indigo-900/20 dark:border-indigo-900/30 dark:text-indigo-300',
  amber: 'bg-amber-50 border-amber-200 text-amber-800 hover:bg-amber-100 dark:bg-amber-900/20 dark:border-amber-900/30 dark:text-amber-300'
};
