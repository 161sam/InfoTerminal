export type StepType = "info" | "action" | "checkpoint";

export interface ScenarioStep {
  id: string;
  title: string;
  description?: string;
  type: StepType;
}

export interface OSINTScenario {
  id: string;
  name: string;
  steps: ScenarioStep[];
}

