"""
Claim Extractor for InfoTerminal Verification Service
Extracts verifiable claims from text using NLP models.
"""

import asyncio
import re
import uuid
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import structlog

try:
    import spacy
    import torch
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    from sentence_transformers import SentenceTransformer
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False

logger = structlog.get_logger()

@dataclass
class Claim:
    """A verifiable claim extracted from text."""
    id: str
    text: str
    confidence: float
    claim_type: str  # "factual", "opinion", "prediction", "causal"
    subject: str
    predicate: str
    object_: str
    temporal: Optional[str] = None
    location: Optional[str] = None
    context: Optional[str] = None

class ClaimExtractor:
    """Extracts verifiable claims from text using NLP models."""
    
    def __init__(self):
        self.nlp = None
        self.claim_classifier = None
        self.sentence_embedder = None
        self.is_initialized = False
        
        # Claim patterns (regex-based fallback)
        self.claim_patterns = [
            r"(.+) is (.+)",
            r"(.+) was (.+)",
            r"(.+) will (.+)",
            r"(.+) has (.+)",
            r"(.+) had (.+)",
            r"(.+) does (.+)",
            r"(.+) did (.+)",
            r"(.+) can (.+)",
            r"(.+) cannot (.+)",
            r"(.+) should (.+)",
            r"(.+) must (.+)",
            r"According to (.+), (.+)",
            r"Studies show that (.+)",
            r"Research indicates (.+)",
            r"(.+) reports that (.+)",
            r"(.+) states that (.+)",
            r"(.+) claims that (.+)",
            r"(.+) percent of (.+)",
            r"(.+) increased by (.+)",
            r"(.+) decreased by (.+)",
            r"(.+) caused (.+)",
            r"(.+) resulted in (.+)"
        ]
        
        # Temporal indicators
        self.temporal_patterns = [
            r"\b(yesterday|today|tomorrow)\b",
            r"\b(in|on|at|during|since|until|from|before|after)\s+\d{4}\b",
            r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b",
            r"\b\d{1,2}\/\d{1,2}\/\d{4}\b",
            r"\b(last|next|this)\s+(year|month|week|day)\b",
            r"\b\d+\s+(years?|months?|weeks?|days?)\s+(ago|from now)\b"
        ]
        
        # Location indicators
        self.location_patterns = [
            r"\bin\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b",
            r"\bat\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b",
            r"\bfrom\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b",
            r"\b([A-Z][a-z]+,\s+[A-Z]{2})\b",  # City, State
            r"\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b"  # Proper nouns
        ]
    
    async def initialize(self):
        """Initialize the claim extractor with NLP models."""
        logger.info("Initializing claim extractor")
        
        if not DEPENDENCIES_AVAILABLE:
            logger.warning("NLP dependencies not available, using fallback methods")
            self.is_initialized = True
            return
        
        try:
            # Load spaCy model for basic NLP
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.warning("spaCy model not found, using fallback")
                self.nlp = None
            
            # Load claim classification model (would be fine-tuned for claims)
            try:
                # In production, this would be a custom-trained model
                self.claim_classifier = pipeline(
                    "text-classification",
                    model="microsoft/DialoGPT-medium",
                    return_all_scores=True,
                    device=0 if torch.cuda.is_available() else -1
                )
            except Exception as e:
                logger.warning("Failed to load claim classifier", error=str(e))
                self.claim_classifier = None
            
            # Load sentence embedder for semantic analysis
            try:
                self.sentence_embedder = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                logger.warning("Failed to load sentence embedder", error=str(e))
                self.sentence_embedder = None
            
            self.is_initialized = True
            logger.info("Claim extractor initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize claim extractor", error=str(e))
            self.is_initialized = True  # Continue with fallback methods
    
    async def extract_claims(
        self,
        text: str,
        confidence_threshold: float = 0.7,
        max_claims: int = 10
    ) -> List[Claim]:
        """Extract verifiable claims from text."""
        
        logger.info("Extracting claims", text_length=len(text))
        
        claims = []
        
        # Split text into sentences
        sentences = self._split_into_sentences(text)
        
        for sentence in sentences:
            # Skip very short sentences
            if len(sentence.split()) < 5:
                continue
            
            # Try different extraction methods
            extracted_claims = []
            
            # Method 1: Pattern-based extraction
            pattern_claims = await self._extract_with_patterns(sentence)
            extracted_claims.extend(pattern_claims)
            
            # Method 2: NLP-based extraction (if available)
            if self.nlp:
                nlp_claims = await self._extract_with_nlp(sentence)
                extracted_claims.extend(nlp_claims)
            
            # Method 3: ML-based classification (if available)
            if self.claim_classifier:
                ml_claims = await self._extract_with_ml(sentence)
                extracted_claims.extend(ml_claims)
            
            # Filter by confidence and deduplicate
            for claim in extracted_claims:
                if claim.confidence >= confidence_threshold:
                    # Check for duplicates
                    is_duplicate = any(
                        self._claims_similar(claim, existing_claim)
                        for existing_claim in claims
                    )
                    
                    if not is_duplicate:
                        claims.append(claim)
                        
                        if len(claims) >= max_claims:
                            break
            
            if len(claims) >= max_claims:
                break
        
        # Sort by confidence
        claims.sort(key=lambda x: x.confidence, reverse=True)
        
        logger.info("Claims extracted", count=len(claims))
        return claims[:max_claims]
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        if self.nlp:
            # Use spaCy for better sentence segmentation
            doc = self.nlp(text)
            return [sent.text.strip() for sent in doc.sents]
        else:
            # Simple regex-based splitting
            sentences = re.split(r'[.!?]+\s+', text)
            return [s.strip() for s in sentences if s.strip()]
    
    async def _extract_with_patterns(self, sentence: str) -> List[Claim]:
        """Extract claims using regex patterns."""
        claims = []
        
        for pattern in self.claim_patterns:
            matches = re.finditer(pattern, sentence, re.IGNORECASE)
            
            for match in matches:
                groups = match.groups()
                if len(groups) >= 2:
                    subject = groups[0].strip()
                    predicate_object = groups[1].strip()
                    
                    # Try to split predicate and object
                    parts = predicate_object.split(' ', 1)
                    predicate = parts[0] if parts else predicate_object
                    object_ = parts[1] if len(parts) > 1 else ""
                    
                    # Extract temporal and location information
                    temporal = self._extract_temporal(sentence)
                    location = self._extract_location(sentence)
                    
                    # Determine claim type
                    claim_type = self._classify_claim_type(sentence)
                    
                    # Calculate confidence based on pattern strength
                    confidence = self._calculate_pattern_confidence(pattern, sentence)
                    
                    claim = Claim(
                        id=str(uuid.uuid4()),
                        text=sentence,
                        confidence=confidence,
                        claim_type=claim_type,
                        subject=subject,
                        predicate=predicate,
                        object_=object_,
                        temporal=temporal,
                        location=location,
                        context=sentence
                    )
                    
                    claims.append(claim)
        
        return claims
    
    async def _extract_with_nlp(self, sentence: str) -> List[Claim]:
        """Extract claims using spaCy NLP analysis."""
        if not self.nlp:
            return []
        
        claims = []
        doc = self.nlp(sentence)
        
        # Look for subject-verb-object triples
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                # Find subject
                subject = None
                for child in token.children:
                    if child.dep_ in ["nsubj", "nsubjpass"]:
                        subject = child.text
                        # Include adjectives and compounds
                        subject_tokens = [child.text]
                        for subchild in child.subtree:
                            if subchild != child and subchild.dep_ in ["amod", "compound"]:
                                subject_tokens.append(subchild.text)
                        subject = " ".join(subject_tokens)
                        break
                
                # Find object
                object_ = None
                for child in token.children:
                    if child.dep_ in ["dobj", "pobj", "attr"]:
                        object_ = child.text
                        # Include adjectives and compounds
                        object_tokens = [child.text]
                        for subchild in child.subtree:
                            if subchild != child and subchild.dep_ in ["amod", "compound"]:
                                object_tokens.append(subchild.text)
                        object_ = " ".join(object_tokens)
                        break
                
                if subject and object_:
                    temporal = self._extract_temporal(sentence)
                    location = self._extract_location(sentence)
                    claim_type = self._classify_claim_type(sentence)
                    
                    # Higher confidence for NLP-extracted claims
                    confidence = 0.8
                    
                    claim = Claim(
                        id=str(uuid.uuid4()),
                        text=sentence,
                        confidence=confidence,
                        claim_type=claim_type,
                        subject=subject,
                        predicate=token.lemma_,
                        object_=object_,
                        temporal=temporal,
                        location=location,
                        context=sentence
                    )
                    
                    claims.append(claim)
        
        return claims
    
    async def _extract_with_ml(self, sentence: str) -> List[Claim]:
        """Extract claims using ML classification."""
        if not self.claim_classifier:
            return []
        
        try:
            # Classify if sentence contains a claim
            results = self.claim_classifier(sentence)
            
            # For now, assume any sentence with high confidence is a claim
            # In production, this would use a model trained specifically for claim detection
            max_score = max(result['score'] for result in results) if results else 0
            
            if max_score > 0.7:  # Threshold for claim detection
                # Extract components using simple heuristics
                # In production, this would use more sophisticated extraction
                tokens = sentence.split()
                subject = " ".join(tokens[:3])  # First few words as subject
                predicate = "states"  # Default predicate
                object_ = " ".join(tokens[3:])  # Rest as object
                
                temporal = self._extract_temporal(sentence)
                location = self._extract_location(sentence)
                claim_type = self._classify_claim_type(sentence)
                
                claim = Claim(
                    id=str(uuid.uuid4()),
                    text=sentence,
                    confidence=max_score,
                    claim_type=claim_type,
                    subject=subject,
                    predicate=predicate,
                    object_=object_,
                    temporal=temporal,
                    location=location,
                    context=sentence
                )
                
                return [claim]
        
        except Exception as e:
            logger.error("ML claim extraction failed", error=str(e))
        
        return []
    
    def _extract_temporal(self, text: str) -> Optional[str]:
        """Extract temporal information from text."""
        for pattern in self.temporal_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group().strip()
        return None
    
    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location information from text."""
        for pattern in self.location_patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                return groups[0] if groups else match.group().strip()
        return None
    
    def _classify_claim_type(self, sentence: str) -> str:
        """Classify the type of claim."""
        sentence_lower = sentence.lower()
        
        # Opinion indicators
        opinion_words = ['believe', 'think', 'feel', 'opinion', 'should', 'must', 'better', 'worse']
        if any(word in sentence_lower for word in opinion_words):
            return "opinion"
        
        # Prediction indicators
        prediction_words = ['will', 'would', 'might', 'could', 'predict', 'forecast', 'expect']
        if any(word in sentence_lower for word in prediction_words):
            return "prediction"
        
        # Causal indicators
        causal_words = ['because', 'due to', 'caused', 'resulted', 'led to', 'reason']
        if any(word in sentence_lower for word in causal_words):
            return "causal"
        
        # Default to factual
        return "factual"
    
    def _calculate_pattern_confidence(self, pattern: str, sentence: str) -> float:
        """Calculate confidence score for pattern-based extraction."""
        base_confidence = 0.6
        
        # Boost confidence for stronger patterns
        strong_patterns = [
            r"According to (.+), (.+)",
            r"Studies show that (.+)",
            r"Research indicates (.+)",
            r"(.+) reports that (.+)",
            r"(.+) percent of (.+)"
        ]
        
        if pattern in strong_patterns:
            base_confidence = 0.8
        
        # Boost for numbers and statistics
        if re.search(r'\d+', sentence):
            base_confidence += 0.1
        
        # Boost for proper nouns (organizations, people)
        if re.search(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', sentence):
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _claims_similar(self, claim1: Claim, claim2: Claim) -> bool:
        """Check if two claims are similar (for deduplication)."""
        if self.sentence_embedder:
            try:
                # Use embeddings for semantic similarity
                embeddings = self.sentence_embedder.encode([claim1.text, claim2.text])
                similarity = self.sentence_embedder.similarity(embeddings[0], embeddings[1])
                return similarity > 0.8
            except Exception:
                pass
        
        # Fallback: simple text similarity
        words1 = set(claim1.text.lower().split())
        words2 = set(claim2.text.lower().split())
        jaccard_similarity = len(words1 & words2) / len(words1 | words2) if words1 | words2 else 0
        
        return jaccard_similarity > 0.7
    
    def is_model_loaded(self) -> bool:
        """Check if ML models are loaded and ready."""
        return self.is_initialized and (self.nlp is not None or self.claim_classifier is not None)
    
    async def cleanup(self):
        """Cleanup resources."""
        logger.info("Cleaning up claim extractor")
        
        # Clear models to free memory
        self.nlp = None
        self.claim_classifier = None
        self.sentence_embedder = None
        
        logger.info("Claim extractor cleanup completed")
