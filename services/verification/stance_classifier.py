"""
Stance Classifier for InfoTerminal Verification Service
Classifies the stance of evidence toward claims.
"""

import asyncio
import re
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import structlog

try:
    import torch
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    from sentence_transformers import SentenceTransformer
    import numpy as np
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False

logger = structlog.get_logger()

@dataclass
class StanceResult:
    """Result of stance classification."""
    stance: str  # "support", "contradict", "neutral", "unrelated"
    confidence: float
    reasoning: str
    key_phrases: List[str]
    evidence_type: str  # "direct", "indirect", "contextual"

class StanceClassifier:
    """Classifies the stance of evidence toward claims."""
    
    def __init__(self):
        self.stance_model = None
        self.nli_model = None  # Natural Language Inference model
        self.sentence_embedder = None
        self.is_initialized = False
        
        # Stance keywords
        self.support_keywords = [
            "confirms", "proves", "shows", "demonstrates", "indicates", "supports",
            "validates", "verifies", "corroborates", "substantiates", "affirms",
            "according to", "research shows", "studies indicate", "data reveals"
        ]
        
        self.contradict_keywords = [
            "contradicts", "disproves", "refutes", "denies", "disputes", "challenges",
            "opposes", "rejects", "debunks", "falsifies", "counters", "however",
            "but", "nevertheless", "on the contrary", "in contrast", "despite"
        ]
        
        self.neutral_keywords = [
            "discusses", "mentions", "refers to", "addresses", "considers",
            "examines", "explores", "investigates", "analyzes", "reviews"
        ]
        
        # Certainty indicators
        self.high_certainty = [
            "definitely", "certainly", "absolutely", "undoubtedly", "clearly",
            "obviously", "proven", "confirmed", "established", "documented"
        ]
        
        self.low_certainty = [
            "possibly", "perhaps", "maybe", "might", "could", "potentially",
            "allegedly", "reportedly", "supposedly", "apparently", "seemingly"
        ]
        
        # Logical connectors
        self.causal_connectors = [
            "because", "due to", "as a result", "therefore", "thus", "hence",
            "consequently", "leads to", "causes", "results in"
        ]
        
        self.contrast_connectors = [
            "however", "but", "although", "despite", "while", "whereas",
            "on the other hand", "in contrast", "nevertheless", "nonetheless"
        ]
    
    async def initialize(self):
        """Initialize the stance classifier."""
        logger.info("Initializing stance classifier")
        
        if not DEPENDENCIES_AVAILABLE:
            logger.warning("ML dependencies not available, using rule-based classification")
            self.is_initialized = True
            return
        
        try:
            # Load NLI model for stance detection
            try:
                self.nli_model = pipeline(
                    "text-classification",
                    model="microsoft/DialoGPT-medium",  # In production, use specialized NLI model
                    return_all_scores=True,
                    device=0 if torch.cuda.is_available() else -1
                )
            except Exception as e:
                logger.warning("Failed to load NLI model", error=str(e))
                self.nli_model = None
            
            # Load sentence embedder for semantic similarity
            try:
                self.sentence_embedder = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                logger.warning("Failed to load sentence embedder", error=str(e))
                self.sentence_embedder = None
            
            self.is_initialized = True
            logger.info("Stance classifier initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize stance classifier", error=str(e))
            self.is_initialized = True  # Continue with rule-based approach
    
    async def classify_stance(
        self,
        claim: str,
        evidence: str,
        context: Optional[str] = None
    ) -> StanceResult:
        """Classify the stance of evidence toward a claim."""
        
        logger.info(
            "Classifying stance",
            claim_length=len(claim),
            evidence_length=len(evidence)
        )
        
        # Try different classification methods
        results = []
        
        # Method 1: Rule-based classification
        rule_result = await self._classify_with_rules(claim, evidence, context)
        results.append(rule_result)
        
        # Method 2: ML-based classification (if available)
        if self.nli_model:
            ml_result = await self._classify_with_ml(claim, evidence, context)
            results.append(ml_result)
        
        # Method 3: Semantic similarity-based classification
        if self.sentence_embedder:
            semantic_result = await self._classify_with_semantics(claim, evidence, context)
            results.append(semantic_result)
        
        # Combine results with weighted voting
        final_result = self._combine_results(results)
        
        logger.info(
            "Stance classified",
            stance=final_result.stance,
            confidence=final_result.confidence
        )
        
        return final_result
    
    async def _classify_with_rules(
        self,
        claim: str,
        evidence: str,
        context: Optional[str] = None
    ) -> StanceResult:
        """Classify stance using rule-based approach."""
        
        # Combine evidence and context for analysis
        full_text = evidence
        if context:
            full_text = f"{evidence} {context}"
        
        # Convert to lowercase for keyword matching
        text_lower = full_text.lower()
        claim_lower = claim.lower()
        
        # Extract key phrases
        key_phrases = self._extract_key_phrases(claim, evidence)
        
        # Score different stance indicators
        support_score = 0
        contradict_score = 0
        neutral_score = 0
        
        # Check for direct stance keywords
        for keyword in self.support_keywords:
            if keyword in text_lower:
                support_score += 1
        
        for keyword in self.contradict_keywords:
            if keyword in text_lower:
                contradict_score += 1
        
        for keyword in self.neutral_keywords:
            if keyword in text_lower:
                neutral_score += 0.5
        
        # Check for sentiment alignment
        claim_sentiment = self._analyze_sentiment(claim)
        evidence_sentiment = self._analyze_sentiment(evidence)
        
        if claim_sentiment == evidence_sentiment and claim_sentiment != "neutral":
            support_score += 1
        elif claim_sentiment != evidence_sentiment and "neutral" not in [claim_sentiment, evidence_sentiment]:
            contradict_score += 1
        
        # Check for logical connectors
        if any(connector in text_lower for connector in self.contrast_connectors):
            contradict_score += 0.5
        
        if any(connector in text_lower for connector in self.causal_connectors):
            support_score += 0.5
        
        # Check for shared entities/concepts
        shared_concepts = self._find_shared_concepts(claim, evidence)
        if shared_concepts:
            support_score += len(shared_concepts) * 0.3
        
        # Determine stance
        total_score = support_score + contradict_score + neutral_score
        
        if total_score == 0:
            stance = "unrelated"
            confidence = 0.5
        elif support_score > contradict_score and support_score > neutral_score:
            stance = "support"
            confidence = min(0.9, 0.5 + (support_score / (total_score + 1)))
        elif contradict_score > support_score and contradict_score > neutral_score:
            stance = "contradict"
            confidence = min(0.9, 0.5 + (contradict_score / (total_score + 1)))
        else:
            stance = "neutral"
            confidence = min(0.8, 0.5 + (neutral_score / (total_score + 1)))
        
        # Generate reasoning
        reasoning = self._generate_reasoning(stance, support_score, contradict_score, neutral_score, key_phrases)
        
        # Determine evidence type
        evidence_type = self._classify_evidence_type(evidence)
        
        return StanceResult(
            stance=stance,
            confidence=confidence,
            reasoning=reasoning,
            key_phrases=key_phrases,
            evidence_type=evidence_type
        )
    
    async def _classify_with_ml(
        self,
        claim: str,
        evidence: str,
        context: Optional[str] = None
    ) -> StanceResult:
        """Classify stance using ML models."""
        
        if not self.nli_model:
            return await self._classify_with_rules(claim, evidence, context)
        
        try:
            # Create premise-hypothesis pairs for NLI
            premise = evidence
            hypothesis = claim
            
            if context:
                premise = f"{evidence} {context}"
            
            # Format for NLI model
            input_text = f"{premise} [SEP] {hypothesis}"
            
            # Get predictions
            results = self.nli_model(input_text)
            
            # Map NLI labels to stance
            # Note: This is a simplified mapping - in production, use a model trained specifically for stance detection
            max_result = max(results, key=lambda x: x['score']) if results else None
            
            if not max_result:
                return await self._classify_with_rules(claim, evidence, context)
            
            # Map labels (adjust based on actual model)
            label_mapping = {
                "ENTAILMENT": "support",
                "CONTRADICTION": "contradict",
                "NEUTRAL": "neutral"
            }
            
            stance = label_mapping.get(max_result['label'].upper(), "neutral")
            confidence = max_result['score']
            
            key_phrases = self._extract_key_phrases(claim, evidence)
            reasoning = f"ML model classified as {stance} with {confidence:.2f} confidence"
            evidence_type = self._classify_evidence_type(evidence)
            
            return StanceResult(
                stance=stance,
                confidence=confidence,
                reasoning=reasoning,
                key_phrases=key_phrases,
                evidence_type=evidence_type
            )
        
        except Exception as e:
            logger.error("ML stance classification failed", error=str(e))
            return await self._classify_with_rules(claim, evidence, context)
    
    async def _classify_with_semantics(
        self,
        claim: str,
        evidence: str,
        context: Optional[str] = None
    ) -> StanceResult:
        """Classify stance using semantic similarity."""
        
        if not self.sentence_embedder:
            return await self._classify_with_rules(claim, evidence, context)
        
        try:
            # Encode texts
            claim_embedding = self.sentence_embedder.encode([claim])
            evidence_embedding = self.sentence_embedder.encode([evidence])
            
            # Calculate similarity
            similarity = float(self.sentence_embedder.similarity(claim_embedding, evidence_embedding)[0][0])
            
            # Create opposing version of claim for contradiction detection
            negated_claim = self._negate_claim(claim)
            negated_embedding = self.sentence_embedder.encode([negated_claim])
            negation_similarity = float(self.sentence_embedder.similarity(evidence_embedding, negated_embedding)[0][0])
            
            # Determine stance based on similarities
            if similarity > 0.7:
                stance = "support"
                confidence = similarity
            elif negation_similarity > 0.7:
                stance = "contradict"
                confidence = negation_similarity
            elif similarity > 0.4:
                stance = "neutral"
                confidence = 0.6
            else:
                stance = "unrelated"
                confidence = 0.5
            
            key_phrases = self._extract_key_phrases(claim, evidence)
            reasoning = f"Semantic similarity analysis: {similarity:.2f} support, {negation_similarity:.2f} contradiction"
            evidence_type = self._classify_evidence_type(evidence)
            
            return StanceResult(
                stance=stance,
                confidence=confidence,
                reasoning=reasoning,
                key_phrases=key_phrases,
                evidence_type=evidence_type
            )
        
        except Exception as e:
            logger.error("Semantic stance classification failed", error=str(e))
            return await self._classify_with_rules(claim, evidence, context)
    
    def _combine_results(self, results: List[StanceResult]) -> StanceResult:
        """Combine multiple classification results using weighted voting."""
        
        if not results:
            return StanceResult("unrelated", 0.5, "No classification results", [], "unknown")
        
        if len(results) == 1:
            return results[0]
        
        # Weight results by confidence
        stance_votes = {}
        total_weight = 0
        
        for result in results:
            weight = result.confidence
            stance = result.stance
            
            if stance not in stance_votes:
                stance_votes[stance] = 0
            stance_votes[stance] += weight
            total_weight += weight
        
        # Normalize votes
        if total_weight > 0:
            for stance in stance_votes:
                stance_votes[stance] /= total_weight
        
        # Find winner
        winning_stance = max(stance_votes, key=stance_votes.get) if stance_votes else "neutral"
        winning_confidence = stance_votes.get(winning_stance, 0.5)
        
        # Combine reasoning and key phrases
        all_key_phrases = []
        all_reasoning = []
        
        for result in results:
            all_key_phrases.extend(result.key_phrases)
            all_reasoning.append(result.reasoning)
        
        # Deduplicate key phrases
        unique_key_phrases = list(set(all_key_phrases))
        combined_reasoning = " | ".join(all_reasoning)
        
        # Determine evidence type (use most specific)
        evidence_types = [result.evidence_type for result in results]
        best_evidence_type = "direct" if "direct" in evidence_types else evidence_types[0] if evidence_types else "contextual"
        
        return StanceResult(
            stance=winning_stance,
            confidence=winning_confidence,
            reasoning=f"Combined analysis: {combined_reasoning}",
            key_phrases=unique_key_phrases[:10],  # Limit to top 10
            evidence_type=best_evidence_type
        )
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis."""
        positive_words = ["good", "great", "positive", "success", "increase", "improve", "benefit"]
        negative_words = ["bad", "terrible", "negative", "failure", "decrease", "worsen", "harm"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _find_shared_concepts(self, claim: str, evidence: str) -> List[str]:
        """Find shared concepts between claim and evidence."""
        # Simple word overlap analysis
        claim_words = set(claim.lower().split())
        evidence_words = set(evidence.lower().split())
        
        # Remove common stop words
        stop_words = {"the", "is", "at", "which", "on", "and", "a", "to", "as", "are", "was"}
        claim_words -= stop_words
        evidence_words -= stop_words
        
        # Find overlap
        shared = claim_words & evidence_words
        return [word for word in shared if len(word) > 2]  # Filter out very short words
    
    def _extract_key_phrases(self, claim: str, evidence: str) -> List[str]:
        """Extract key phrases that indicate stance."""
        key_phrases = []
        text = f"{claim} {evidence}".lower()
        
        # Find stance keywords
        for keyword in self.support_keywords + self.contradict_keywords + self.neutral_keywords:
            if keyword in text:
                key_phrases.append(keyword)
        
        # Find certainty indicators
        for indicator in self.high_certainty + self.low_certainty:
            if indicator in text:
                key_phrases.append(indicator)
        
        # Find logical connectors
        for connector in self.causal_connectors + self.contrast_connectors:
            if connector in text:
                key_phrases.append(connector)
        
        return list(set(key_phrases))  # Remove duplicates
    
    def _generate_reasoning(
        self,
        stance: str,
        support_score: float,
        contradict_score: float,
        neutral_score: float,
        key_phrases: List[str]
    ) -> str:
        """Generate human-readable reasoning for the stance classification."""
        
        reasoning_parts = []
        
        if stance == "support":
            reasoning_parts.append(f"Evidence supports the claim (score: {support_score:.1f})")
            if "confirms" in key_phrases or "proves" in key_phrases:
                reasoning_parts.append("Contains confirmatory language")
        elif stance == "contradict":
            reasoning_parts.append(f"Evidence contradicts the claim (score: {contradict_score:.1f})")
            if "however" in key_phrases or "but" in key_phrases:
                reasoning_parts.append("Contains contradictory language")
        elif stance == "neutral":
            reasoning_parts.append(f"Evidence is neutral toward the claim (score: {neutral_score:.1f})")
        else:
            reasoning_parts.append("Evidence appears unrelated to the claim")
        
        if key_phrases:
            reasoning_parts.append(f"Key indicators: {', '.join(key_phrases[:3])}")
        
        return ". ".join(reasoning_parts)
    
    def _classify_evidence_type(self, evidence: str) -> str:
        """Classify the type of evidence."""
        evidence_lower = evidence.lower()
        
        # Direct evidence indicators
        if any(phrase in evidence_lower for phrase in ["data shows", "statistics", "study found", "research indicates"]):
            return "direct"
        
        # Indirect evidence indicators
        if any(phrase in evidence_lower for phrase in ["according to", "reports suggest", "experts believe"]):
            return "indirect"
        
        # Default to contextual
        return "contextual"
    
    def _negate_claim(self, claim: str) -> str:
        """Create a negated version of a claim for contradiction detection."""
        claim_lower = claim.lower()
        
        # Simple negation patterns
        if " is " in claim_lower:
            return claim.replace(" is ", " is not ")
        elif " are " in claim_lower:
            return claim.replace(" are ", " are not ")
        elif " will " in claim_lower:
            return claim.replace(" will ", " will not ")
        elif " has " in claim_lower:
            return claim.replace(" has ", " does not have ")
        elif " can " in claim_lower:
            return claim.replace(" can ", " cannot ")
        else:
            return f"It is not true that {claim.lower()}"
    
    def is_model_loaded(self) -> bool:
        """Check if ML models are loaded and ready."""
        return self.is_initialized and (self.nli_model is not None or self.sentence_embedder is not None)
    
    async def cleanup(self):
        """Cleanup resources."""
        logger.info("Cleaning up stance classifier")
        
        # Clear models to free memory
        self.stance_model = None
        self.nli_model = None
        self.sentence_embedder = None
        
        logger.info("Stance classifier cleanup completed")
