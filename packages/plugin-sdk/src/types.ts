export type JsonSchema = Record<string, any>;

export interface ToolSpec {
  name: string;
  description?: string;
  argsSchema: JsonSchema;
  resultSchema?: JsonSchema;
  timeoutMs?: number;
  auth?: "inherit" | "none";
  permissions?: string[];
}

export interface PluginManifest {
  apiVersion: "v1";
  name: string;
  version: string;
  description?: string;
  provider?: string;
  capabilities: { tools: ToolSpec[] };
  endpoints?: {
    baseUrl: string;
    health?: string; // default: "healthz"
  };
}
