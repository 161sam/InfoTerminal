/**
 * Interactive Tutorial System
 *
 * Provides guided walkthroughs for OSINT scenarios using intro.js
 * Tracks user progress and adapts to user behavior
 */

import React, { useState, useEffect, useCallback } from "react";
import { introJs } from "intro.js";
import "intro.js/minified/introjs.min.css";
import {
  Play,
  Pause,
  RotateCcw,
  BookOpen,
  CheckCircle,
  AlertCircle,
  HelpCircle,
} from "lucide-react";
import { OSINTScenario, ScenarioStep, StepType } from "@/types/scenarios";
import UserJourneyTracker from "@/lib/user-journey-tracker";

interface TutorialSystemProps {
  scenario: OSINTScenario;
  onComplete: (results: TutorialResults) => void;
  onExit: () => void;
  isVisible: boolean;
}

interface TutorialResults {
  scenarioId: string;
  completed: boolean;
  stepsCompleted: number;
  totalSteps: number;
  timeSpent: number;
  errors: number;
  hintsUsed: number;
  userRating: number;
  feedback: string;
}

interface StepProgress {
  stepId: string;
  status: "pending" | "active" | "completed" | "error";
  startTime?: number;
  endTime?: number;
  hintsUsed: number;
  errors: number;
  userActions: string[];
}

const TutorialSystem: React.FC<TutorialSystemProps> = ({
  scenario,
  onComplete,
  onExit,
  isVisible,
}) => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [stepProgress, setStepProgress] = useState<StepProgress[]>([]);
  const [tutorialStartTime, setTutorialStartTime] = useState<number>(0);
  const [showHints, setShowHints] = useState(false);
  const [showStepPanel, setShowStepPanel] = useState(true);
  const [introInstance, setIntroInstance] = useState<any>(null);
  const [userActions, setUserActions] = useState<string[]>([]);

  const { trackWorkflowStep, trackClick } = UserJourneyTracker.useUserJourney();

  // Initialize tutorial
  useEffect(() => {
    if (isVisible && scenario) {
      initializeTutorial();
    }

    return () => {
      if (introInstance) {
        introInstance.exit();
      }
    };
  }, [isVisible, scenario]);

  const initializeTutorial = () => {
    const progress = scenario.steps.map((step) => ({
      stepId: step.id,
      status: "pending" as const,
      hintsUsed: 0,
      errors: 0,
      userActions: [],
    }));

    setStepProgress(progress);
    setTutorialStartTime(Date.now());
    setCurrentStepIndex(0);

    // Track tutorial start
    trackWorkflowStep(scenario.id, "tutorial_started");
  };

  if (!isVisible) return null;

  return (
    <div className="tutorial-system">
      <div className="tutorial-placeholder">
        <h3>Tutorial System for {scenario.title}</h3>
        <p>This is a placeholder for the interactive tutorial system.</p>
      </div>
    </div>
  );
};

export default TutorialSystem;
