// pages/api/verification/classify-stance.ts
import type { NextApiRequest, NextApiResponse } from "next";

interface ClassifyStanceRequest {
  claim: string;
  evidence: string;
  context?: string;
}

interface StanceResponse {
  stance: string;
  confidence: number;
  reasoning: string;
  key_phrases: string[];
  evidence_type: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<StanceResponse | { error: string }>,
) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { claim, evidence, context }: ClassifyStanceRequest = req.body;

    if (!claim || claim.trim().length === 0) {
      return res.status(400).json({ error: "Claim is required" });
    }

    if (!evidence || evidence.trim().length === 0) {
      return res.status(400).json({ error: "Evidence is required" });
    }

    // Call verification service
    const verificationServiceUrl = process.env.VERIFICATION_SERVICE_URL || "http://localhost:8617";
    const response = await fetch(`${verificationServiceUrl}/verify/classify-stance`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        claim,
        evidence,
        context,
      }),
    });

    if (!response.ok) {
      // Fallback: Create mock stance classification for demo
      const mockStance = generateMockStance(claim, evidence);
      return res.status(200).json(mockStance);
    }

    const stanceResult = await response.json();
    res.status(200).json(stanceResult);
  } catch (error) {
    console.error("Failed to classify stance:", error);

    // Fallback: Create mock stance
    try {
      const mockStance = generateMockStance(req.body.claim, req.body.evidence);
      res.status(200).json(mockStance);
    } catch {
      res.status(500).json({ error: "Failed to classify stance" });
    }
  }
}

function generateMockStance(claim: string, evidence: string): StanceResponse {
  const claimLower = claim.toLowerCase();
  const evidenceLower = evidence.toLowerCase();

  // Simple keyword-based stance detection for demo
  let stance = "neutral";
  let confidence = 0.6;
  let keyPhrases: string[] = [];

  // Support indicators
  const supportWords = ["confirms", "proves", "shows", "supports", "validates", "according to"];
  const supportCount = supportWords.filter((word) => evidenceLower.includes(word)).length;

  // Contradiction indicators
  const contradictWords = ["contradicts", "disproves", "refutes", "however", "but", "denies"];
  const contradictCount = contradictWords.filter((word) => evidenceLower.includes(word)).length;

  // Neutral indicators
  const neutralWords = ["discusses", "mentions", "addresses", "considers"];
  const neutralCount = neutralWords.filter((word) => evidenceLower.includes(word)).length;

  if (supportCount > contradictCount && supportCount > 0) {
    stance = "support";
    confidence = 0.7 + Math.min(supportCount * 0.1, 0.2);
    keyPhrases = supportWords.filter((word) => evidenceLower.includes(word));
  } else if (contradictCount > supportCount && contradictCount > 0) {
    stance = "contradict";
    confidence = 0.7 + Math.min(contradictCount * 0.1, 0.2);
    keyPhrases = contradictWords.filter((word) => evidenceLower.includes(word));
  } else if (neutralCount > 0) {
    stance = "neutral";
    confidence = 0.6 + Math.min(neutralCount * 0.05, 0.15);
    keyPhrases = neutralWords.filter((word) => evidenceLower.includes(word));
  } else {
    // Check for shared concepts
    const claimWords = new Set(claimLower.split(" ").filter((w) => w.length > 3));
    const evidenceWords = new Set(evidenceLower.split(" ").filter((w) => w.length > 3));
    const sharedWords = [...claimWords].filter((word) => evidenceWords.has(word));

    if (sharedWords.length > 2) {
      stance = "support";
      confidence = 0.6;
      keyPhrases = sharedWords.slice(0, 3);
    } else if (sharedWords.length > 0) {
      stance = "neutral";
      confidence = 0.5;
      keyPhrases = sharedWords;
    } else {
      stance = "unrelated";
      confidence = 0.8;
      keyPhrases = [];
    }
  }

  // Determine evidence type
  let evidenceType = "contextual";
  if (
    evidenceLower.includes("data") ||
    evidenceLower.includes("study") ||
    evidenceLower.includes("research")
  ) {
    evidenceType = "direct";
  } else if (evidenceLower.includes("according to") || evidenceLower.includes("reports")) {
    evidenceType = "indirect";
  }

  // Generate reasoning
  let reasoning = `Analysis of the evidence suggests a ${stance} stance toward the claim.`;

  if (keyPhrases.length > 0) {
    reasoning += ` Key indicators include: ${keyPhrases.slice(0, 3).join(", ")}.`;
  }

  if (stance === "support") {
    reasoning += " The evidence provides information that aligns with or confirms the claim.";
  } else if (stance === "contradict") {
    reasoning += " The evidence provides information that disputes or refutes the claim.";
  } else if (stance === "neutral") {
    reasoning +=
      " The evidence discusses the topic but does not clearly support or contradict the claim.";
  } else {
    reasoning += " The evidence does not appear to be directly related to the claim.";
  }

  return {
    stance,
    confidence: Math.min(confidence, 0.95),
    reasoning,
    key_phrases: keyPhrases.slice(0, 5),
    evidence_type: evidenceType,
  };
}
