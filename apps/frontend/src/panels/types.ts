export interface Entity {
  id: string;
  name: string;
  type?: string;
  // Optional analytics fields used in mock/entity samples
  mentions?: number;
  confidence?: number;
  firstSeen?: string;
  lastSeen?: string;
  sources?: string[];
  verified?: boolean;
  description?: string;
  aliases?: string[];
  connections?: number;
  riskScore?: number;
  tags?: string[];
}

export interface AgentCapability {
  id: string;
  name: string;
  description?: string;
}

export interface DomainConfig {
  id: string;
  name: string;
}

export type Domain = string;

export interface ExampleText {
  id: string;
  text: string;
}
