"""
Feedback Aggregation Service

Collects, categorizes, and processes user feedback, bug reports, and feature requests.
Integrates with GitHub Issues for automated ticket creation.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import json
import aioredis
import asyncio
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import logging
from dataclasses import dataclass
import requests
import os
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Feedback Aggregator Service", version="1.0.0")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/feedback_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FeedbackType(str, Enum):
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    USABILITY_ISSUE = "usability_issue"
    PERFORMANCE_ISSUE = "performance_issue"
    DOCUMENTATION_ISSUE = "documentation_issue"
    GENERAL_FEEDBACK = "general_feedback"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Status(str, Enum):
    NEW = "new"
    TRIAGED = "triaged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

# Database Models
class FeedbackEntry(Base):
    __tablename__ = "feedback_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_id = Column(String, index=True, nullable=True)
    feedback_type = Column(String, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    rating = Column(Integer, nullable=True)  # 1-5 scale
    page_url = Column(String)
    user_agent = Column(String)
    browser_info = Column(JSON)
    steps_to_reproduce = Column(Text, nullable=True)
    expected_behavior = Column(Text, nullable=True)
    actual_behavior = Column(Text, nullable=True)
    tags = Column(JSON, default=list)
    priority = Column(String, default=Priority.MEDIUM)
    status = Column(String, default=Status.NEW)
    github_issue_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    votes = Column(Integer, default=0)
    metadata = Column(JSON, default=dict)

class VoteEntry(Base):
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, index=True)
    user_id = Column(String, index=True)
    vote_type = Column(String)  # upvote, downvote
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Pydantic Models
class FeedbackCreate(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    feedback_type: FeedbackType
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)
    rating: Optional[int] = Field(None, ge=1, le=5)
    page_url: str
    user_agent: str
    browser_info: Dict[str, Any] = Field(default_factory=dict)
    steps_to_reproduce: Optional[str] = None
    expected_behavior: Optional[str] = None
    actual_behavior: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

class FeedbackResponse(BaseModel):
    id: int
    feedback_type: str
    title: str
    description: str
    rating: Optional[int]
    priority: str
    status: str
    votes: int
    github_issue_url: Optional[str]
    created_at: datetime
    tags: List[str]

class VoteCreate(BaseModel):
    feedback_id: int
    user_id: str
    vote_type: str  # "upvote" or "downvote"

class FeedbackStats(BaseModel):
    total_feedback: int
    by_type: Dict[str, int]
    by_priority: Dict[str, int]
    by_status: Dict[str, int]
    average_rating: float
    top_tags: List[Dict[str, Any]]
    recent_trends: Dict[str, Any]

# GitHub Integration
class GitHubIssueCreator:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo_owner = os.getenv("GITHUB_REPO_OWNER", "your-username")
        self.repo_name = os.getenv("GITHUB_REPO_NAME", "InfoTerminal")
        self.base_url = "https://api.github.com"
    
    async def create_issue(self, feedback: FeedbackEntry) -> Optional[str]:
        """Create GitHub issue from feedback"""
        if not self.github_token:
            logger.warning("GitHub token not configured, skipping issue creation")
            return None
        
        # Determine labels based on feedback type and priority
        labels = [feedback.feedback_type, f"priority-{feedback.priority}"]
        if feedback.tags:
            labels.extend(feedback.tags[:3])  # Limit to avoid too many labels
        
        # Create issue body
        issue_body = self._format_issue_body(feedback)
        
        # GitHub API payload
        payload = {
            "title": f"[{feedback.feedback_type.upper()}] {feedback.title}",
            "body": issue_body,
            "labels": labels
        }
        
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 201:
                issue_data = response.json()
                logger.info(f"Created GitHub issue #{issue_data['number']} for feedback {feedback.id}")
                return issue_data["html_url"]
            else:
                logger.error(f"Failed to create GitHub issue: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating GitHub issue: {e}")
            return None
    
    def _format_issue_body(self, feedback: FeedbackEntry) -> str:
        """Format feedback as GitHub issue body"""
        body_parts = [
            f"**Feedback Type:** {feedback.feedback_type}",
            f"**Priority:** {feedback.priority}",
            f"**Page:** {feedback.page_url}",
            "",
            "## Description",
            feedback.description,
        ]
        
        if feedback.rating:
            body_parts.extend([
                "",
                f"**User Rating:** {feedback.rating}/5 ⭐"
            ])
        
        if feedback.steps_to_reproduce:
            body_parts.extend([
                "",
                "## Steps to Reproduce",
                feedback.steps_to_reproduce
            ])
        
        if feedback.expected_behavior:
            body_parts.extend([
                "",
                "## Expected Behavior",
                feedback.expected_behavior
            ])
        
        if feedback.actual_behavior:
            body_parts.extend([
                "",
                "## Actual Behavior",
                feedback.actual_behavior
            ])
        
        if feedback.browser_info:
            body_parts.extend([
                "",
                "## Technical Details",
                f"```json",
                json.dumps(feedback.browser_info, indent=2),
                "```"
            ])
        
        body_parts.extend([
            "",
            "---",
            f"*Reported via InfoTerminal Feedback System - ID: {feedback.id}*",
            f"*Session: {feedback.session_id}*",
            f"*Created: {feedback.created_at.isoformat()}*"
        ])
        
        return "\n".join(body_parts)

# Feedback Analyzer
class FeedbackAnalyzer:
    def __init__(self):
        self.sentiment_keywords = {
            "positive": ["good", "great", "excellent", "love", "awesome", "perfect", "helpful"],
            "negative": ["bad", "terrible", "hate", "awful", "broken", "confusing", "slow"],
            "neutral": ["okay", "fine", "decent", "average", "normal"]
        }
        
        self.urgency_keywords = {
            "critical": ["crash", "broken", "error", "fail", "cannot", "unable", "urgent"],
            "high": ["slow", "difficult", "confusing", "missing", "important"],
            "medium": ["improve", "better", "would like", "suggestion"],
            "low": ["minor", "cosmetic", "nice to have", "eventually"]
        }
    
    def analyze_feedback(self, feedback: FeedbackCreate) -> Dict[str, Any]:
        """Analyze feedback content for sentiment, urgency, and categorization"""
        text = f"{feedback.title} {feedback.description}".lower()
        
        analysis = {
            "sentiment": self._analyze_sentiment(text),
            "urgency": self._analyze_urgency(text),
            "suggested_priority": self._suggest_priority(feedback, text),
            "extracted_tags": self._extract_tags(text),
            "estimated_effort": self._estimate_effort(feedback, text)
        }
        
        return analysis
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of feedback text"""
        scores = {"positive": 0, "negative": 0, "neutral": 0}
        
        for sentiment, keywords in self.sentiment_keywords.items():
            scores[sentiment] = sum(1 for keyword in keywords if keyword in text)
        
        return max(scores, key=scores.get)
    
    def _analyze_urgency(self, text: str) -> str:
        """Analyze urgency level from text"""
        scores = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        for urgency, keywords in self.urgency_keywords.items():
            scores[urgency] = sum(1 for keyword in keywords if keyword in text)
        
        return max(scores, key=scores.get)
    
    def _suggest_priority(self, feedback: FeedbackCreate, text: str) -> str:
        """Suggest priority based on feedback type and content analysis"""
        urgency = self._analyze_urgency(text)
        
        priority_mapping = {
            FeedbackType.BUG_REPORT: {
                "critical": Priority.CRITICAL,
                "high": Priority.HIGH,
                "medium": Priority.MEDIUM,
                "low": Priority.LOW
            },
            FeedbackType.PERFORMANCE_ISSUE: {
                "critical": Priority.HIGH,
                "high": Priority.HIGH,
                "medium": Priority.MEDIUM,
                "low": Priority.LOW
            },
            FeedbackType.FEATURE_REQUEST: {
                "critical": Priority.MEDIUM,
                "high": Priority.MEDIUM,
                "medium": Priority.LOW,
                "low": Priority.LOW
            }
        }
        
        default_mapping = {
            "critical": Priority.MEDIUM,
            "high": Priority.MEDIUM,
            "medium": Priority.LOW,
            "low": Priority.LOW
        }
        
        mapping = priority_mapping.get(feedback.feedback_type, default_mapping)
        return mapping.get(urgency, Priority.MEDIUM)
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from feedback text"""
        tag_keywords = {
            "ui": ["interface", "button", "menu", "layout", "design"],
            "performance": ["slow", "fast", "loading", "response", "speed"],
            "search": ["search", "find", "query", "results"],
            "graph": ["graph", "visualization", "network", "nodes"],
            "export": ["export", "download", "save", "file"],
            "mobile": ["mobile", "phone", "tablet", "responsive"],
            "accessibility": ["accessibility", "screen reader", "keyboard", "contrast"]
        }
        
        extracted_tags = []
        for tag, keywords in tag_keywords.items():
            if any(keyword in text for keyword in keywords):
                extracted_tags.append(tag)
        
        return extracted_tags[:5]  # Limit to 5 tags
    
    def _estimate_effort(self, feedback: FeedbackCreate, text: str) -> str:
        """Estimate development effort required"""
        if feedback.feedback_type == FeedbackType.FEATURE_REQUEST:
            if any(word in text for word in ["new", "add", "create", "build"]):
                return "high"
            elif any(word in text for word in ["improve", "enhance", "better"]):
                return "medium"
        elif feedback.feedback_type == FeedbackType.BUG_REPORT:
            return "low"
        
        return "medium"

# Service class
class FeedbackService:
    def __init__(self):
        self.github_creator = GitHubIssueCreator()
        self.analyzer = FeedbackAnalyzer()
        self.redis = None
    
    async def initialize_redis(self):
        """Initialize Redis connection for caching"""
        try:
            self.redis = await aioredis.from_url("redis://localhost:6379")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
    
    def get_db(self) -> Session:
        """Get database session"""
        db = SessionLocal()
        try:
            return db
        finally:
            pass  # Session will be closed by caller
    
    async def create_feedback(self, feedback_data: FeedbackCreate, background_tasks: BackgroundTasks) -> FeedbackResponse:
        """Create new feedback entry with analysis"""
        db = self.get_db()
        
        try:
            # Analyze feedback
            analysis = self.analyzer.analyze_feedback(feedback_data)
            
            # Create database entry
            db_feedback = FeedbackEntry(
                session_id=feedback_data.session_id,
                user_id=feedback_data.user_id,
                feedback_type=feedback_data.feedback_type,
                title=feedback_data.title,
                description=feedback_data.description,
                rating=feedback_data.rating,
                page_url=feedback_data.page_url,
                user_agent=feedback_data.user_agent,
                browser_info=feedback_data.browser_info,
                steps_to_reproduce=feedback_data.steps_to_reproduce,
                expected_behavior=feedback_data.expected_behavior,
                actual_behavior=feedback_data.actual_behavior,
                tags=feedback_data.tags + analysis["extracted_tags"],
                priority=analysis["suggested_priority"],
                metadata=analysis
            )
            
            db.add(db_feedback)
            db.commit()
            db.refresh(db_feedback)
            
            # Schedule GitHub issue creation
            background_tasks.add_task(self._create_github_issue, db_feedback.id)
            
            # Cache for quick access
            if self.redis:
                await self._cache_feedback_stats()
            
            return FeedbackResponse(
                id=db_feedback.id,
                feedback_type=db_feedback.feedback_type,
                title=db_feedback.title,
                description=db_feedback.description,
                rating=db_feedback.rating,
                priority=db_feedback.priority,
                status=db_feedback.status,
                votes=db_feedback.votes,
                github_issue_url=db_feedback.github_issue_url,
                created_at=db_feedback.created_at,
                tags=db_feedback.tags
            )
            
        finally:
            db.close()
    
    async def _create_github_issue(self, feedback_id: int):
        """Background task to create GitHub issue"""
        db = self.get_db()
        
        try:
            feedback = db.query(FeedbackEntry).filter(FeedbackEntry.id == feedback_id).first()
            if not feedback:
                return
            
            github_url = await self.github_creator.create_issue(feedback)
            if github_url:
                feedback.github_issue_url = github_url
                db.commit()
                
        finally:
            db.close()
    
    async def vote_feedback(self, vote_data: VoteCreate) -> bool:
        """Vote on feedback entry"""
        db = self.get_db()
        
        try:
            # Check if user already voted
            existing_vote = db.query(VoteEntry).filter(
                VoteEntry.feedback_id == vote_data.feedback_id,
                VoteEntry.user_id == vote_data.user_id
            ).first()
            
            if existing_vote:
                # Update existing vote
                existing_vote.vote_type = vote_data.vote_type
                existing_vote.created_at = datetime.utcnow()
            else:
                # Create new vote
                new_vote = VoteEntry(
                    feedback_id=vote_data.feedback_id,
                    user_id=vote_data.user_id,
                    vote_type=vote_data.vote_type
                )
                db.add(new_vote)
            
            # Update feedback vote count
            feedback = db.query(FeedbackEntry).filter(FeedbackEntry.id == vote_data.feedback_id).first()
            if feedback:
                vote_count = db.query(VoteEntry).filter(
                    VoteEntry.feedback_id == vote_data.feedback_id,
                    VoteEntry.vote_type == "upvote"
                ).count()
                
                downvote_count = db.query(VoteEntry).filter(
                    VoteEntry.feedback_id == vote_data.feedback_id,
                    VoteEntry.vote_type == "downvote"
                ).count()
                
                feedback.votes = vote_count - downvote_count
            
            db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error voting on feedback: {e}")
            db.rollback()
            return False
            
        finally:
            db.close()
    
    async def get_feedback_stats(self) -> FeedbackStats:
        """Get aggregated feedback statistics"""
        # Try cache first
        if self.redis:
            cached_stats = await self.redis.get("feedback_stats")
            if cached_stats:
                return FeedbackStats.parse_raw(cached_stats)
        
        db = self.get_db()
        
        try:
            total_feedback = db.query(FeedbackEntry).count()
            
            # Group by type
            by_type = defaultdict(int)
            by_priority = defaultdict(int)
            by_status = defaultdict(int)
            
            feedbacks = db.query(FeedbackEntry).all()
            ratings = []
            tag_counts = defaultdict(int)
            
            for feedback in feedbacks:
                by_type[feedback.feedback_type] += 1
                by_priority[feedback.priority] += 1
                by_status[feedback.status] += 1
                
                if feedback.rating:
                    ratings.append(feedback.rating)
                
                for tag in feedback.tags:
                    tag_counts[tag] += 1
            
            # Calculate average rating
            average_rating = sum(ratings) / len(ratings) if ratings else 0
            
            # Top tags
            top_tags = [
                {"tag": tag, "count": count}
                for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            ]
            
            # Recent trends (last 7 days)
            week_ago = datetime.utcnow() - timedelta(days=7)
            recent_feedback = db.query(FeedbackEntry).filter(
                FeedbackEntry.created_at >= week_ago
            ).count()
            
            recent_trends = {
                "this_week": recent_feedback,
                "daily_average": recent_feedback / 7,
                "growth_rate": self._calculate_growth_rate(db)
            }
            
            stats = FeedbackStats(
                total_feedback=total_feedback,
                by_type=dict(by_type),
                by_priority=dict(by_priority),
                by_status=dict(by_status),
                average_rating=round(average_rating, 2),
                top_tags=top_tags,
                recent_trends=recent_trends
            )
            
            # Cache stats
            if self.redis:
                await self.redis.setex("feedback_stats", 300, stats.json())  # Cache for 5 minutes
            
            return stats
            
        finally:
            db.close()
    
    def _calculate_growth_rate(self, db: Session) -> float:
        """Calculate feedback growth rate"""
        this_week = datetime.utcnow() - timedelta(days=7)
        last_week = datetime.utcnow() - timedelta(days=14)
        
        this_week_count = db.query(FeedbackEntry).filter(
            FeedbackEntry.created_at >= this_week
        ).count()
        
        last_week_count = db.query(FeedbackEntry).filter(
            FeedbackEntry.created_at >= last_week,
            FeedbackEntry.created_at < this_week
        ).count()
        
        if last_week_count == 0:
            return 100.0 if this_week_count > 0 else 0.0
        
        return ((this_week_count - last_week_count) / last_week_count) * 100
    
    async def _cache_feedback_stats(self):
        """Cache feedback statistics"""
        if self.redis:
            stats = await self.get_feedback_stats()
            await self.redis.setex("feedback_stats", 300, stats.json())

# Initialize service
feedback_service = FeedbackService()

@app.on_event("startup")
async def startup_event():
    await feedback_service.initialize_redis()

# API Endpoints
@app.post("/feedback", response_model=FeedbackResponse)
async def create_feedback(
    feedback: FeedbackCreate, 
    background_tasks: BackgroundTasks
):
    """Create new feedback entry"""
    return await feedback_service.create_feedback(feedback, background_tasks)

@app.post("/feedback/{feedback_id}/vote")
async def vote_on_feedback(feedback_id: int, vote: VoteCreate):
    """Vote on feedback entry"""
    vote.feedback_id = feedback_id
    success = await feedback_service.vote_feedback(vote)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to vote on feedback")
    return {"message": "Vote recorded successfully"}

@app.get("/feedback/stats", response_model=FeedbackStats)
async def get_feedback_statistics():
    """Get aggregated feedback statistics"""
    return await feedback_service.get_feedback_stats()

@app.get("/feedback")
async def get_feedback_list(
    skip: int = 0, 
    limit: int = 50,
    feedback_type: Optional[FeedbackType] = None,
    priority: Optional[Priority] = None,
    status: Optional[Status] = None
):
    """Get paginated list of feedback entries"""
    db = feedback_service.get_db()
    
    try:
        query = db.query(FeedbackEntry)
        
        if feedback_type:
            query = query.filter(FeedbackEntry.feedback_type == feedback_type)
        if priority:
            query = query.filter(FeedbackEntry.priority == priority)
        if status:
            query = query.filter(FeedbackEntry.status == status)
        
        feedbacks = query.order_by(FeedbackEntry.created_at.desc()).offset(skip).limit(limit).all()
        
        return [
            FeedbackResponse(
                id=f.id,
                feedback_type=f.feedback_type,
                title=f.title,
                description=f.description,
                rating=f.rating,
                priority=f.priority,
                status=f.status,
                votes=f.votes,
                github_issue_url=f.github_issue_url,
                created_at=f.created_at,
                tags=f.tags
            )
            for f in feedbacks
        ]
        
    finally:
        db.close()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "feedback-aggregator"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
