// NLP panel types and interfaces
import { LucideIcon } from "lucide-react";

export type NLPTab = "entities" | "summary" | "sentiment";
export type Domain = "general" | "legal" | "documents" | "ethics" | "forensics";

export interface EntityResult {
  text: string;
  label: string;
  start: number;
  end: number;
  confidence: number;
}

export interface NERResponse {
  entities: EntityResult[];
  processing_time?: number;
}

export interface SummaryResponse {
  summary: string;
  processing_time?: number;
}

export interface DomainConfig {
  id: Domain;
  name: string;
  icon: LucideIcon;
  color: string;
  description: string;
}

export interface ExampleText {
  title: string;
  text: string;
}

export const DOMAIN_COLORS = {
  blue: "bg-blue-50 text-blue-800 border-blue-200 hover:bg-blue-100 dark:bg-blue-900/20 dark:border-blue-900/30 dark:text-blue-300",
  purple:
    "bg-purple-50 text-purple-800 border-purple-200 hover:bg-purple-100 dark:bg-purple-900/20 dark:border-purple-900/30 dark:text-purple-300",
  green:
    "bg-green-50 text-green-800 border-green-200 hover:bg-green-100 dark:bg-green-900/20 dark:border-green-900/30 dark:text-green-300",
  indigo:
    "bg-indigo-50 text-indigo-800 border-indigo-200 hover:bg-indigo-100 dark:bg-indigo-900/20 dark:border-indigo-900/30 dark:text-indigo-300",
  red: "bg-red-50 text-red-800 border-red-200 hover:bg-red-100 dark:bg-red-900/20 dark:border-red-900/30 dark:text-red-300",
};

export const ENTITY_COLORS: Record<string, string> = {
  PERSON: "bg-blue-100 text-blue-800 border-blue-200",
  ORG: "bg-green-100 text-green-800 border-green-200",
  ORGANIZATION: "bg-green-100 text-green-800 border-green-200",
  GPE: "bg-purple-100 text-purple-800 border-purple-200",
  LOCATION: "bg-purple-100 text-purple-800 border-purple-200",
  MONEY: "bg-yellow-100 text-yellow-800 border-yellow-200",
  DATE: "bg-orange-100 text-orange-800 border-orange-200",
  EMAIL: "bg-pink-100 text-pink-800 border-pink-200",
  LAW: "bg-purple-100 text-purple-800 border-purple-200",
  REGULATION: "bg-indigo-100 text-indigo-800 border-indigo-200",
  DEFAULT: "bg-gray-100 text-gray-800 border-gray-200",
};
