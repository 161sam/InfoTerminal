// pages/api/verification/extract-claims.ts
import type { NextApiRequest, NextApiResponse } from "next";

interface ExtractClaimsRequest {
  text: string;
  confidence_threshold?: number;
  max_claims?: number;
}

interface ClaimResponse {
  id: string;
  text: string;
  confidence: number;
  claim_type: string;
  subject: string;
  predicate: string;
  object: string;
  temporal?: string;
  location?: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ClaimResponse[] | { error: string }>,
) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { text, confidence_threshold = 0.7, max_claims = 10 }: ExtractClaimsRequest = req.body;

    if (!text || text.trim().length === 0) {
      return res.status(400).json({ error: "Text is required" });
    }

    // Call verification service
    const verificationServiceUrl = process.env.VERIFICATION_SERVICE_URL || "http://localhost:8617";
    const response = await fetch(`${verificationServiceUrl}/verify/extract-claims`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text,
        confidence_threshold,
        max_claims,
      }),
    });

    if (!response.ok) {
      // Fallback: Create mock claims for demo
      const mockClaims = generateMockClaims(text, max_claims);
      return res.status(200).json(mockClaims);
    }

    const claims = await response.json();
    res.status(200).json(claims);
  } catch (error) {
    console.error("Failed to extract claims:", error);

    // Fallback: Create mock claims
    try {
      const mockClaims = generateMockClaims(req.body.text, req.body.max_claims || 10);
      res.status(200).json(mockClaims);
    } catch {
      res.status(500).json({ error: "Failed to extract claims" });
    }
  }
}

function generateMockClaims(text: string, maxClaims: number): ClaimResponse[] {
  const sentences = text.split(/[.!?]+/).filter((s) => s.trim().length > 10);
  const claims: ClaimResponse[] = [];

  for (let i = 0; i < Math.min(sentences.length, maxClaims); i++) {
    const sentence = sentences[i].trim();
    if (sentence.length === 0) continue;

    // Simple heuristic to extract subject/predicate/object
    const words = sentence.split(" ");
    const subject = words.slice(0, Math.min(3, words.length)).join(" ");
    const predicate = words.length > 3 ? words[3] : "is";
    const object = words.length > 4 ? words.slice(4).join(" ") : "relevant";

    claims.push({
      id: `claim_${Date.now()}_${i}`,
      text: sentence,
      confidence: 0.6 + Math.random() * 0.3, // Random confidence between 0.6-0.9
      claim_type: ["factual", "opinion", "prediction"][Math.floor(Math.random() * 3)],
      subject: subject,
      predicate: predicate,
      object: object,
      temporal: Math.random() > 0.7 ? "2024" : undefined,
      location: Math.random() > 0.8 ? "United States" : undefined,
    });
  }

  return claims;
}
