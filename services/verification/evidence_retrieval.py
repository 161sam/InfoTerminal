"""
Evidence Retrieval for InfoTerminal Verification Service
Finds supporting evidence for claims from various sources.
"""

import asyncio
import re
import uuid
import hashlib
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from urllib.parse import urlparse, urljoin
import structlog

try:
    import httpx
    import wikipedia
    from bs4 import BeautifulSoup
    from sentence_transformers import SentenceTransformer
    import numpy as np
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False

logger = structlog.get_logger()

@dataclass
class Evidence:
    """Evidence found for a claim."""
    id: str
    source_url: str
    source_title: str
    source_type: str  # "web", "wikipedia", "news", "academic"
    snippet: str
    relevance_score: float
    credibility_score: float
    publication_date: Optional[str] = None
    author: Optional[str] = None
    domain: Optional[str] = None

@dataclass
class CredibilityAssessment:
    """Credibility assessment for a source."""
    credibility_score: float
    bias_rating: str  # "left", "center", "right", "unknown"
    factual_reporting: str  # "high", "medium", "low", "unknown"
    transparency_score: float
    authority_indicators: List[str]
    red_flags: List[str]

class EvidenceRetriever:
    """Retrieves evidence for claims from various sources."""
    
    def __init__(self):
        self.http_client = None
        self.sentence_embedder = None
        self.is_initialized = False
        
        # Known credible sources (domain-based)
        self.credible_domains = {
            # News organizations
            "reuters.com": {"credibility": 0.9, "bias": "center", "factual": "high"},
            "ap.org": {"credibility": 0.9, "bias": "center", "factual": "high"},
            "bbc.com": {"credibility": 0.85, "bias": "center", "factual": "high"},
            "npr.org": {"credibility": 0.85, "bias": "center", "factual": "high"},
            
            # Academic/Research
            "scholar.google.com": {"credibility": 0.95, "bias": "center", "factual": "high"},
            "pubmed.ncbi.nlm.nih.gov": {"credibility": 0.95, "bias": "center", "factual": "high"},
            "nature.com": {"credibility": 0.95, "bias": "center", "factual": "high"},
            "science.org": {"credibility": 0.95, "bias": "center", "factual": "high"},
            
            # Government
            "census.gov": {"credibility": 0.9, "bias": "center", "factual": "high"},
            "cdc.gov": {"credibility": 0.9, "bias": "center", "factual": "high"},
            "fda.gov": {"credibility": 0.9, "bias": "center", "factual": "high"},
            "who.int": {"credibility": 0.9, "bias": "center", "factual": "high"},
            
            # Fact-checking
            "snopes.com": {"credibility": 0.85, "bias": "center", "factual": "high"},
            "factcheck.org": {"credibility": 0.85, "bias": "center", "factual": "high"},
            "politifact.com": {"credibility": 0.8, "bias": "center", "factual": "high"},
        }
        
        # Known problematic sources
        self.unreliable_domains = {
            "example-fake-news.com": {"credibility": 0.2, "bias": "unknown", "factual": "low"},
            # Add known unreliable sources
        }
        
        # Search engines and APIs
        self.search_endpoints = {
            "web": "https://api.duckduckgo.com/",  # Placeholder - would use real API
            "news": "https://newsapi.org/v2/everything",  # Requires API key
            "academic": "https://api.crossref.org/works"
        }
    
    async def initialize(self):
        """Initialize the evidence retriever."""
        logger.info("Initializing evidence retriever")
        
        if not DEPENDENCIES_AVAILABLE:
            logger.warning("Dependencies not available, using mock data")
            self.is_initialized = True
            return
        
        try:
            # Initialize HTTP client
            self.http_client = httpx.AsyncClient(
                timeout=30.0,
                headers={
                    "User-Agent": "InfoTerminal-Verification/0.2.0 (Research Tool)"
                }
            )
            
            # Initialize sentence embedder for relevance scoring
            try:
                self.sentence_embedder = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                logger.warning("Failed to load sentence embedder", error=str(e))
                self.sentence_embedder = None
            
            self.is_initialized = True
            logger.info("Evidence retriever initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize evidence retriever", error=str(e))
            self.is_initialized = True  # Continue with fallback
    
    async def find_evidence(
        self,
        claim: str,
        max_sources: int = 5,
        source_types: List[str] = ["web", "wikipedia", "news"],
        language: str = "en"
    ) -> List[Evidence]:
        """Find evidence for a claim from multiple sources."""
        
        logger.info(
            "Finding evidence for claim",
            claim_length=len(claim),
            max_sources=max_sources,
            source_types=source_types
        )
        
        all_evidence = []
        
        # Search each source type
        for source_type in source_types:
            try:
                if source_type == "wikipedia":
                    evidence = await self._search_wikipedia(claim, max_sources // len(source_types))
                elif source_type == "web":
                    evidence = await self._search_web(claim, max_sources // len(source_types))
                elif source_type == "news":
                    evidence = await self._search_news(claim, max_sources // len(source_types))
                elif source_type == "academic":
                    evidence = await self._search_academic(claim, max_sources // len(source_types))
                else:
                    logger.warning("Unknown source type", source_type=source_type)
                    continue
                
                all_evidence.extend(evidence)
                
            except Exception as e:
                logger.error("Failed to search source", source_type=source_type, error=str(e))
        
        # Calculate relevance scores
        if self.sentence_embedder and all_evidence:
            all_evidence = await self._score_relevance(claim, all_evidence)
        
        # Sort by relevance and credibility
        all_evidence.sort(key=lambda x: (x.relevance_score * x.credibility_score), reverse=True)
        
        # Deduplicate
        deduplicated = self._deduplicate_evidence(all_evidence)
        
        result = deduplicated[:max_sources]
        
        logger.info("Evidence found", count=len(result))
        return result
    
    async def _search_wikipedia(self, claim: str, max_results: int) -> List[Evidence]:
        """Search Wikipedia for evidence."""
        if not DEPENDENCIES_AVAILABLE:
            return self._mock_evidence("wikipedia", max_results)
        
        evidence_list = []
        
        try:
            # Extract key terms from claim for search
            search_terms = self._extract_search_terms(claim)
            
            # Search Wikipedia
            wikipedia.set_lang("en")
            search_results = wikipedia.search(search_terms, results=max_results * 2)
            
            for title in search_results[:max_results]:
                try:
                    page = wikipedia.page(title)
                    
                    # Find relevant snippet
                    snippet = self._find_relevant_snippet(claim, page.content)
                    
                    if snippet:
                        evidence = Evidence(
                            id=str(uuid.uuid4()),
                            source_url=page.url,
                            source_title=page.title,
                            source_type="wikipedia",
                            snippet=snippet,
                            relevance_score=0.7,  # Will be recalculated
                            credibility_score=0.85,  # Wikipedia generally credible
                            domain="wikipedia.org"
                        )
                        evidence_list.append(evidence)
                
                except wikipedia.exceptions.DisambiguationError as e:
                    # Try the first disambiguation option
                    try:
                        page = wikipedia.page(e.options[0])
                        snippet = self._find_relevant_snippet(claim, page.content)
                        if snippet:
                            evidence = Evidence(
                                id=str(uuid.uuid4()),
                                source_url=page.url,
                                source_title=page.title,
                                source_type="wikipedia",
                                snippet=snippet,
                                relevance_score=0.6,
                                credibility_score=0.85,
                                domain="wikipedia.org"
                            )
                            evidence_list.append(evidence)
                    except Exception:
                        continue
                
                except Exception as e:
                    logger.warning("Failed to process Wikipedia page", title=title, error=str(e))
                    continue
        
        except Exception as e:
            logger.error("Wikipedia search failed", error=str(e))
        
        return evidence_list
    
    async def _search_web(self, claim: str, max_results: int) -> List[Evidence]:
        """Search the web for evidence."""
        if not DEPENDENCIES_AVAILABLE or not self.http_client:
            return self._mock_evidence("web", max_results)
        
        evidence_list = []
        
        try:
            search_terms = self._extract_search_terms(claim)
            
            # Mock web search results (in production, use real search API)
            mock_results = [
                {
                    "url": f"https://example.com/article-{i}",
                    "title": f"Article about {search_terms} - {i}",
                    "snippet": f"This article discusses {claim[:50]}... with supporting evidence and analysis.",
                    "domain": "example.com"
                }
                for i in range(max_results)
            ]
            
            for result in mock_results:
                try:
                    # Assess credibility
                    credibility = await self.assess_credibility(result["url"])
                    
                    evidence = Evidence(
                        id=str(uuid.uuid4()),
                        source_url=result["url"],
                        source_title=result["title"],
                        source_type="web",
                        snippet=result["snippet"],
                        relevance_score=0.7,  # Will be recalculated
                        credibility_score=credibility.credibility_score,
                        domain=result["domain"]
                    )
                    evidence_list.append(evidence)
                
                except Exception as e:
                    logger.warning("Failed to process web result", error=str(e))
                    continue
        
        except Exception as e:
            logger.error("Web search failed", error=str(e))
        
        return evidence_list
    
    async def _search_news(self, claim: str, max_results: int) -> List[Evidence]:
        """Search news sources for evidence."""
        return self._mock_evidence("news", max_results)
    
    async def _search_academic(self, claim: str, max_results: int) -> List[Evidence]:
        """Search academic sources for evidence."""
        return self._mock_evidence("academic", max_results)
    
    def _mock_evidence(self, source_type: str, count: int) -> List[Evidence]:
        """Generate mock evidence for testing."""
        evidence_list = []
        
        for i in range(count):
            evidence = Evidence(
                id=str(uuid.uuid4()),
                source_url=f"https://mock-{source_type}.com/article-{i}",
                source_title=f"Mock {source_type} article {i}",
                source_type=source_type,
                snippet=f"This is a mock snippet from {source_type} source discussing relevant information.",
                relevance_score=0.8 - (i * 0.1),
                credibility_score=0.7 + (i % 2) * 0.2,
                domain=f"mock-{source_type}.com"
            )
            evidence_list.append(evidence)
        
        return evidence_list
    
    async def _score_relevance(self, claim: str, evidence_list: List[Evidence]) -> List[Evidence]:
        """Score evidence relevance using semantic similarity."""
        if not self.sentence_embedder:
            return evidence_list
        
        try:
            # Encode claim
            claim_embedding = self.sentence_embedder.encode([claim])
            
            # Encode evidence snippets
            snippets = [evidence.snippet for evidence in evidence_list]
            snippet_embeddings = self.sentence_embedder.encode(snippets)
            
            # Calculate similarities
            similarities = self.sentence_embedder.similarity(claim_embedding, snippet_embeddings)[0]
            
            # Update relevance scores
            for i, evidence in enumerate(evidence_list):
                evidence.relevance_score = float(similarities[i])
        
        except Exception as e:
            logger.error("Failed to score relevance", error=str(e))
        
        return evidence_list
    
    def _extract_search_terms(self, claim: str) -> str:
        """Extract key search terms from a claim."""
        # Remove common stop words and extract key terms
        stop_words = {
            "the", "is", "at", "which", "on", "and", "a", "to", "as", "are",
            "was", "will", "be", "been", "being", "have", "has", "had", "do",
            "does", "did", "can", "could", "should", "would", "may", "might"
        }
        
        words = claim.lower().split()
        key_terms = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Take the most important terms (first few)
        return " ".join(key_terms[:5])
    
    def _find_relevant_snippet(self, claim: str, content: str, max_length: int = 200) -> str:
        """Find the most relevant snippet from content."""
        # Split content into sentences
        sentences = re.split(r'[.!?]+', content)
        
        # Find sentences that contain key terms from the claim
        claim_words = set(self._extract_search_terms(claim).lower().split())
        
        best_sentence = ""
        best_score = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:  # Skip very short sentences
                continue
            
            sentence_words = set(sentence.lower().split())
            overlap = len(claim_words & sentence_words)
            score = overlap / len(claim_words) if claim_words else 0
            
            if score > best_score:
                best_score = score
                best_sentence = sentence
        
        # Truncate if too long
        if len(best_sentence) > max_length:
            best_sentence = best_sentence[:max_length] + "..."
        
        return best_sentence if best_score > 0.1 else content[:max_length] + "..."
    
    def _deduplicate_evidence(self, evidence_list: List[Evidence]) -> List[Evidence]:
        """Remove duplicate evidence based on content similarity."""
        seen_urls = set()
        seen_content_hashes = set()
        deduplicated = []
        
        for evidence in evidence_list:
            # Skip duplicate URLs
            if evidence.source_url in seen_urls:
                continue
            
            # Skip very similar content
            content_hash = hashlib.md5(evidence.snippet.encode()).hexdigest()
            if content_hash in seen_content_hashes:
                continue
            
            seen_urls.add(evidence.source_url)
            seen_content_hashes.add(content_hash)
            deduplicated.append(evidence)
        
        return deduplicated
    
    async def assess_credibility(self, source_url: str) -> CredibilityAssessment:
        """Assess the credibility of a source."""
        
        domain = urlparse(source_url).netloc.lower()
        
        # Check known credible sources
        if domain in self.credible_domains:
            source_info = self.credible_domains[domain]
            return CredibilityAssessment(
                credibility_score=source_info["credibility"],
                bias_rating=source_info["bias"],
                factual_reporting=source_info["factual"],
                transparency_score=0.8,
                authority_indicators=["Known credible source", "Editorial standards"],
                red_flags=[]
            )
        
        # Check known unreliable sources
        if domain in self.unreliable_domains:
            source_info = self.unreliable_domains[domain]
            return CredibilityAssessment(
                credibility_score=source_info["credibility"],
                bias_rating=source_info["bias"],
                factual_reporting=source_info["factual"],
                transparency_score=0.2,
                authority_indicators=[],
                red_flags=["Known unreliable source", "Poor fact-checking record"]
            )
        
        # For unknown sources, use heuristics
        credibility_score = 0.5  # Neutral starting point
        authority_indicators = []
        red_flags = []
        
        # Domain analysis
        if domain.endswith('.edu'):
            credibility_score += 0.3
            authority_indicators.append("Educational institution")
        elif domain.endswith('.gov'):
            credibility_score += 0.4
            authority_indicators.append("Government source")
        elif domain.endswith('.org'):
            credibility_score += 0.1
            authority_indicators.append("Organization")
        
        # Check for HTTPS
        if source_url.startswith('https://'):
            credibility_score += 0.1
            authority_indicators.append("Secure connection")
        else:
            red_flags.append("Insecure connection")
        
        # Check for suspicious patterns
        suspicious_keywords = ['fake', 'clickbait', 'shocking', 'unbelievable']
        if any(keyword in source_url.lower() for keyword in suspicious_keywords):
            credibility_score -= 0.3
            red_flags.append("Suspicious URL keywords")
        
        # Domain age and reputation (would need external API)
        # For now, assume unknown domains have moderate credibility
        
        credibility_score = max(0.0, min(1.0, credibility_score))
        
        return CredibilityAssessment(
            credibility_score=credibility_score,
            bias_rating="unknown",
            factual_reporting="unknown",
            transparency_score=credibility_score * 0.8,
            authority_indicators=authority_indicators,
            red_flags=red_flags
        )
    
    def get_available_sources(self) -> List[str]:
        """Get list of available source types."""
        return ["web", "wikipedia", "news", "academic"]
    
    async def cleanup(self):
        """Cleanup resources."""
        logger.info("Cleaning up evidence retriever")
        
        if self.http_client:
            await self.http_client.aclose()
        
        self.sentence_embedder = None
        
        logger.info("Evidence retriever cleanup completed")
