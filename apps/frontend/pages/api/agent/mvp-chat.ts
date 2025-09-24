import type { NextApiRequest, NextApiResponse } from "next";
import { getAgentApis } from "@/lib/config";

interface MvpChatRequest {
  message: string;
  tool?: string;
  toolParams?: Record<string, unknown>;
  conversationId?: string;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { message, tool, toolParams = {}, conversationId }: MvpChatRequest = req.body;

  if (!message || typeof message !== "string") {
    return res.status(400).json({ error: "message is required" });
  }

  const apis = getAgentApis();

  try {
    const response = await fetch(`${apis.primary}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "User-Agent": "InfoTerminal-Agent-MVP",
      },
      body: JSON.stringify({
        message,
        tool,
        tool_params: toolParams,
        conversation_id: conversationId,
      }),
    });

    const text = await response.text();
    let payload: any;
    try {
      payload = text ? JSON.parse(text) : {};
    } catch (error) {
      payload = { detail: text };
    }

    if (!response.ok) {
      const detail = payload?.message || payload?.detail || payload?.error || response.statusText;
      return res.status(response.status).json({ error: detail, detail: payload });
    }

    return res.status(200).json(payload);
  } catch (error: any) {
    return res.status(502).json({ error: "Agent connector unreachable", detail: error?.message });
  }
}
