// Agent Capabilities API Route Handler
// Provides information about available agent capabilities

import type { NextApiRequest, NextApiResponse } from "next";
import {
  AGENT_CAPABILITIES,
  getCapabilitiesByCategory,
  getCapabilityById,
  type AgentCapability,
} from "@/lib/agent-config";
import { getAgentApis } from "@/lib/config";

interface CapabilitiesResponse {
  capabilities: AgentCapability[];
  categories: string[];
  total: number;
  timestamp: string;
}

interface RunCapabilityRequest {
  capability: string;
  agent_type?: string;
  context?: string;
  session_id?: string;
  tools?: string[];
}

interface RunCapabilityResponse {
  result: string;
  steps?: any[];
  tools_used?: string[];
  execution_time?: number;
  session_id?: string;
  error?: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<CapabilitiesResponse | RunCapabilityResponse | { error: string }>,
) {
  const { method, query } = req;

  try {
    if (method === "GET") {
      // Return available capabilities
      const category = query.category as string | undefined;

      let capabilities: AgentCapability[];
      if (category && category !== "all") {
        capabilities = getCapabilitiesByCategory(category as any);
      } else {
        capabilities = AGENT_CAPABILITIES;
      }

      const categories = [...new Set(AGENT_CAPABILITIES.map((c) => c.category))];

      const response: CapabilitiesResponse = {
        capabilities,
        categories,
        total: capabilities.length,
        timestamp: new Date().toISOString(),
      };

      return res.status(200).json(response);
    } else if (method === "POST") {
      // Run a specific capability
      const apis = getAgentApis();
      const {
        capability: capabilityId,
        agent_type,
        context = "Manual execution",
        session_id,
        tools,
      }: RunCapabilityRequest = req.body;

      if (!capabilityId) {
        return res.status(400).json({ error: "Capability ID is required" });
      }

      const capability = getCapabilityById(capabilityId);
      if (!capability) {
        return res.status(404).json({ error: "Capability not found" });
      }

      // Prepare request for agent service
      const requestBody = {
        capability: capabilityId,
        agent_type: agent_type || capability.name,
        context,
        session_id,
        tools: tools || capability.tools,
        max_iterations: capability.maxIterations || 10,
      };

      const response = await fetch(`${apis.primary}/capabilities/run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "User-Agent": "InfoTerminal-Frontend",
        },
        body: JSON.stringify(requestBody),
        signal: AbortSignal.timeout(60000), // 60 second timeout for capability runs
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Capability execution error:", response.status, errorText);
        return res.status(response.status).json({
          error: `Capability execution failed: ${response.status} ${response.statusText}`,
        });
      }

      const data = await response.json();

      const capabilityResponse: RunCapabilityResponse = {
        result: data.result || data.response || "Capability executed successfully",
        steps: data.steps || [],
        tools_used: data.tools_used || capability.tools,
        execution_time: data.execution_time,
        session_id: data.session_id || session_id,
      };

      return res.status(200).json(capabilityResponse);
    } else {
      return res.status(405).json({ error: "Method not allowed" });
    }
  } catch (error: any) {
    console.error("Capabilities API error:", error);

    if (error.name === "TimeoutError") {
      return res.status(408).json({ error: "Request timeout" });
    }

    return res.status(500).json({
      error: "Internal server error",
    });
  }
}
