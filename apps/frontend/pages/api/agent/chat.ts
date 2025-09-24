// Agent Chat API Route Handler for InfoTerminal
// Proxies chat requests to the agent-connector service

import type { NextApiRequest, NextApiResponse } from "next";
import { getAgentApis, AGENT_CONFIG } from "@/lib/config";

interface ChatRequest {
  messages: Array<{
    role: "user" | "assistant" | "system";
    content: string;
  }>;
  agent_type?: string;
  session_id?: string;
  max_iterations?: number;
  include_steps?: boolean;
  tools_allowed?: string[];
}

interface ChatResponse {
  reply?: string;
  response?: string;
  steps?: any[];
  references?: any;
  tools_used?: string[];
  confidence?: number;
  execution_time?: number;
  session_id?: string;
  error?: string;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse<ChatResponse>) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const apis = getAgentApis();
    const {
      messages,
      agent_type = AGENT_CONFIG.defaultType,
      session_id,
      max_iterations = AGENT_CONFIG.maxIterations,
      include_steps = AGENT_CONFIG.includeSteps,
      tools_allowed,
    }: ChatRequest = req.body;

    // Validate request
    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return res.status(400).json({ error: "Messages array is required" });
    }

    // Prepare request body for agent service
    const requestBody = {
      messages,
      agent_type,
      session_id,
      max_iterations,
      include_steps,
      tools_allowed: tools_allowed?.length ? tools_allowed : undefined,
    };

    // Forward request to agent service
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), AGENT_CONFIG.timeout);

    const response = await fetch(`${apis.primary}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "User-Agent": "InfoTerminal-Frontend",
      },
      body: JSON.stringify(requestBody),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Agent service error:", response.status, errorText);
      return res.status(response.status).json({
        error: `Agent service error: ${response.status} ${response.statusText}`,
      });
    }

    const data = await response.json();

    // Normalize response format
    const chatResponse: ChatResponse = {
      reply: data.reply || data.response,
      steps: data.steps || [],
      references: data.references,
      tools_used: data.tools_used || [],
      confidence: data.confidence,
      execution_time: data.execution_time,
      session_id: data.session_id || session_id,
    };

    return res.status(200).json(chatResponse);
  } catch (error: any) {
    console.error("Agent chat API error:", error);

    if (error.name === "AbortError") {
      return res.status(408).json({ error: "Request timeout" });
    }

    return res.status(500).json({
      error: "Internal server error",
      ...(AGENT_CONFIG.debugMode && { details: error.message }),
    });
  }
}
