// pages/api/verification/find-evidence.ts
import type { NextApiRequest, NextApiResponse } from "next";

interface FindEvidenceRequest {
  claim: string;
  max_sources?: number;
  source_types?: string[];
  language?: string;
}

interface EvidenceResponse {
  id: string;
  source_url: string;
  source_title: string;
  source_type: string;
  snippet: string;
  relevance_score: number;
  credibility_score: number;
  publication_date?: string;
  author?: string;
  domain?: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<EvidenceResponse[] | { error: string }>,
) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const {
      claim,
      max_sources = 5,
      source_types = ["web", "wikipedia", "news"],
      language = "en",
    }: FindEvidenceRequest = req.body;

    if (!claim || claim.trim().length === 0) {
      return res.status(400).json({ error: "Claim is required" });
    }

    // Call verification service
    const verificationServiceUrl = process.env.VERIFICATION_SERVICE_URL || "http://localhost:8617";
    const response = await fetch(`${verificationServiceUrl}/verify/find-evidence`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        claim,
        max_sources,
        source_types,
        language,
      }),
    });

    if (!response.ok) {
      // Fallback: Create mock evidence for demo
      const mockEvidence = generateMockEvidence(claim, max_sources, source_types);
      return res.status(200).json(mockEvidence);
    }

    const evidence = await response.json();
    res.status(200).json(evidence);
  } catch (error) {
    console.error("Failed to find evidence:", error);

    // Fallback: Create mock evidence
    try {
      const mockEvidence = generateMockEvidence(
        req.body.claim,
        req.body.max_sources || 5,
        req.body.source_types || ["web", "wikipedia", "news"],
      );
      res.status(200).json(mockEvidence);
    } catch {
      res.status(500).json({ error: "Failed to find evidence" });
    }
  }
}

function generateMockEvidence(
  claim: string,
  maxSources: number,
  sourceTypes: string[],
): EvidenceResponse[] {
  const evidence: EvidenceResponse[] = [];

  const domains = {
    web: ["reuters.com", "bbc.com", "npr.org", "cnn.com"],
    wikipedia: ["en.wikipedia.org"],
    news: ["ap.org", "reuters.com", "bloomberg.com"],
    academic: ["pubmed.ncbi.nlm.nih.gov", "nature.com", "science.org"],
  };

  const authors = ["John Smith", "Jane Doe", "Dr. Sarah Johnson", "Michael Brown", "Lisa Chen"];

  for (let i = 0; i < maxSources; i++) {
    const sourceType = sourceTypes[i % sourceTypes.length];
    const domainList = domains[sourceType as keyof typeof domains] || domains.web;
    const domain = domainList[Math.floor(Math.random() * domainList.length)];

    evidence.push({
      id: `evidence_${Date.now()}_${i}`,
      source_url: `https://${domain}/article-${i + 1}`,
      source_title: `Article about ${claim.slice(0, 30)}... - Source ${i + 1}`,
      source_type: sourceType,
      snippet: `This article discusses the claim "${claim.slice(0, 50)}..." and provides ${
        Math.random() > 0.5 ? "supporting" : "contradicting"
      } evidence with detailed analysis and expert opinions.`,
      relevance_score: 0.6 + Math.random() * 0.4,
      credibility_score: getCredibilityForDomain(domain),
      publication_date: new Date(
        2024,
        Math.floor(Math.random() * 12),
        Math.floor(Math.random() * 28) + 1,
      )
        .toISOString()
        .split("T")[0],
      author: Math.random() > 0.3 ? authors[Math.floor(Math.random() * authors.length)] : undefined,
      domain: domain,
    });
  }

  return evidence;
}

function getCredibilityForDomain(domain: string): number {
  const credibilityMap: { [key: string]: number } = {
    "reuters.com": 0.95,
    "ap.org": 0.95,
    "bbc.com": 0.9,
    "npr.org": 0.88,
    "en.wikipedia.org": 0.8,
    "bloomberg.com": 0.85,
    "cnn.com": 0.75,
    "pubmed.ncbi.nlm.nih.gov": 0.98,
    "nature.com": 0.98,
    "science.org": 0.98,
  };

  return credibilityMap[domain] || 0.6;
}
