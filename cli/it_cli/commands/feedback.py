"""User feedback and analytics commands."""
from __future__ import annotations

import asyncio
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="User Feedback & Analytics")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def post(
    message: str = typer.Argument(..., help="Feedback message"),
    category: str = typer.Option("general", "--category", "-c", help="Feedback category"),
    rating: Optional[int] = typer.Option(None, "--rating", "-r", help="Rating (1-5)"),
    tags: List[str] = typer.Option([], "--tag", "-t", help="Feedback tags"),
    component: Optional[str] = typer.Option(None, "--component", help="Related component"),
) -> None:
    """Submit user feedback."""
    if rating and not 1 <= rating <= 5:
        console.print("❌ Rating must be between 1 and 5")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        payload = {
            "message": message,
            "category": category,
            "tags": tags
        }
        if rating:
            payload["rating"] = rating
        if component:
            payload["component"] = component
            
        async with client() as c:
            resp = await c.post(
                f"{settings.feedback_api}/v1/feedback",
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            
            console.print("✅ Feedback submitted")
            console.print(f"ID: {data.get('id')}")
            console.print(f"Category: {data.get('category')}")
            console.print(f"Priority: {data.get('priority', 'Normal')}")
            
            # Show AI analysis if available
            if data.get("analysis"):
                analysis = data.get("analysis", {})
                console.print(f"Sentiment: {analysis.get('sentiment', 'Unknown')}")
                console.print(f"Urgency: {analysis.get('urgency', 'Unknown')}")

    _run(_action)

@app.command()
def list(
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by tag"),
    limit: int = typer.Option(20, "--limit", "-l", help="Results limit"),
    sort: str = typer.Option("created_desc", "--sort", help="Sort order"),
) -> None:
    """List feedback entries."""
    settings = get_settings()

    async def _action():
        params = {
            "limit": limit,
            "sort": sort
        }
        if category:
            params["category"] = category
        if status:
            params["status"] = status
        if tag:
            params["tag"] = tag
            
        async with client() as c:
            resp = await c.get(f"{settings.feedback_api}/v1/feedback", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title=f"Feedback ({data.get('total', 0)})")
            table.add_column("ID")
            table.add_column("Category")
            table.add_column("Message")
            table.add_column("Rating")
            table.add_column("Status")
            table.add_column("Created")
            
            for feedback in data.get("items", []):
                message_preview = feedback.get("message", "")[:50] + "..."
                rating_str = str(feedback.get("rating", "")) if feedback.get("rating") else "-"
                
                table.add_row(
                    str(feedback.get("id", ""))[:8],
                    feedback.get("category", ""),
                    message_preview,
                    rating_str,
                    feedback.get("status", ""),
                    feedback.get("created_at", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def show(
    feedback_id: int = typer.Argument(..., help="Feedback ID"),
) -> None:
    """Show detailed feedback entry."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.feedback_api}/v1/feedback/{feedback_id}")
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"📝 Feedback #{feedback_id}")
            console.print(f"Category: {data.get('category', '')}")
            console.print(f"Status: {data.get('status', '')}")
            console.print(f"Priority: {data.get('priority', '')}")
            console.print(f"Rating: {data.get('rating', 'N/A')}")
            console.print(f"Created: {data.get('created_at', '')}")
            console.print(f"Updated: {data.get('updated_at', '')}")
            
            console.print(f"\nMessage:")
            console.print(f"  {data.get('message', '')}")
            
            # Show tags
            if data.get("tags"):
                tags_str = ", ".join(data.get("tags", []))
                console.print(f"\nTags: {tags_str}")
            
            # Show AI analysis
            if data.get("analysis"):
                analysis = data.get("analysis", {})
                console.print(f"\n🤖 AI Analysis:")
                console.print(f"  Sentiment: {analysis.get('sentiment', 'Unknown')}")
                console.print(f"  Urgency: {analysis.get('urgency', 'Unknown')}")
                console.print(f"  Confidence: {analysis.get('confidence', 0)}")
                
                if analysis.get("extracted_tags"):
                    extracted_tags = ", ".join(analysis.get("extracted_tags", []))
                    console.print(f"  Extracted Tags: {extracted_tags}")
            
            # Show votes
            if data.get("votes"):
                votes = data.get("votes", {})
                console.print(f"\n👍 Votes: +{votes.get('upvotes', 0)} -{votes.get('downvotes', 0)}")

    _run(_action)

@app.command()
def vote(
    feedback_id: int = typer.Argument(..., help="Feedback ID"),
    vote_type: str = typer.Argument(..., help="Vote type: up|down"),
) -> None:
    """Vote on feedback entry."""
    if vote_type not in ["up", "down"]:
        console.print("❌ Vote type must be 'up' or 'down'")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        payload = {"vote_type": vote_type}
        
        async with client() as c:
            resp = await c.post(
                f"{settings.feedback_api}/v1/feedback/{feedback_id}/vote",
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"✅ Vote recorded: {vote_type}")
            console.print(f"Total votes: +{data.get('upvotes', 0)} -{data.get('downvotes', 0)}")

    _run(_action)

@app.command()
def stats(
    period: str = typer.Option("30d", "--period", "-p", help="Time period: 7d|30d|90d"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
) -> None:
    """Show feedback statistics."""
    settings = get_settings()

    async def _action():
        params = {"period": period}
        if category:
            params["category"] = category
            
        async with client() as c:
            resp = await c.get(f"{settings.feedback_api}/v1/feedback/stats", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"📊 Feedback Statistics ({period})")
            
            # Overall stats
            overall = data.get("overall", {})
            console.print(f"Total Feedback: {overall.get('total_count', 0)}")
            console.print(f"Average Rating: {overall.get('average_rating', 0):.1f}")
            console.print(f"Response Rate: {overall.get('response_rate', 0):.1f}%")
            
            # Category breakdown
            if data.get("by_category"):
                table = Table(title="By Category")
                table.add_column("Category")
                table.add_column("Count")
                table.add_column("Avg Rating")
                table.add_column("Sentiment")
                
                for cat_data in data.get("by_category", []):
                    table.add_row(
                        cat_data.get("category", ""),
                        str(cat_data.get("count", 0)),
                        f"{cat_data.get('average_rating', 0):.1f}",
                        cat_data.get("sentiment", ""),
                    )
                
                console.print(table)
            
            # Sentiment analysis
            if data.get("sentiment_breakdown"):
                sentiment = data.get("sentiment_breakdown", {})
                console.print(f"\n😊 Sentiment Breakdown:")
                console.print(f"  Positive: {sentiment.get('positive', 0)}%")
                console.print(f"  Neutral: {sentiment.get('neutral', 0)}%")
                console.print(f"  Negative: {sentiment.get('negative', 0)}%")

    _run(_action)

@app.command()
def trends(
    metric: str = typer.Option("rating", "--metric", "-m", help="Metric: rating|volume|sentiment"),
    period: str = typer.Option("30d", "--period", "-p", help="Time period"),
    granularity: str = typer.Option("daily", "--granularity", "-g", help="Granularity: hourly|daily|weekly"),
) -> None:
    """Show feedback trends over time."""
    settings = get_settings()

    async def _action():
        params = {
            "metric": metric,
            "period": period,
            "granularity": granularity
        }
        
        async with client() as c:
            resp = await c.get(f"{settings.feedback_api}/v1/feedback/trends", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            console.print(f"📈 Feedback Trends: {metric} ({period}, {granularity})")
            
            table = Table(title="Trend Data")
            table.add_column("Date")
            table.add_column("Value")
            table.add_column("Change")
            
            trend_data = data.get("trend_data", [])
            for point in trend_data:
                change_str = ""
                if point.get("change"):
                    change = point.get("change", 0)
                    change_str = f"+{change:.1f}" if change > 0 else f"{change:.1f}"
                
                table.add_row(
                    point.get("date", ""),
                    str(point.get("value", 0)),
                    change_str,
                )
            
            console.print(table)
            
            # Summary
            summary = data.get("summary", {})
            if summary:
                console.print(f"\n📋 Summary:")
                console.print(f"  Overall Trend: {summary.get('trend_direction', 'Unknown')}")
                console.print(f"  Change: {summary.get('total_change', 0):.1f}")

    _run(_action)

@app.command()
def bulk(
    action: str = typer.Argument(..., help="Action: export|import|delete"),
    file: Optional[typer.FileText] = typer.Option(None, "--file", "-f", help="Input/output file"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
) -> None:
    """Bulk operations on feedback."""
    settings = get_settings()

    async def _action():
        if action == "export":
            # Export feedback data
            params = {}
            if category:
                params["category"] = category
            if status:
                params["status"] = status
                
            async with client() as c:
                resp = await c.get(f"{settings.feedback_api}/v1/feedback/bulk", params=params)
                resp.raise_for_status()
                data = resp.json()
                
                if file:
                    import json
                    json.dump(data, file, indent=2)
                    console.print(f"✅ Exported {len(data.get('items', []))} feedback entries")
                else:
                    console.print_json(data=data)
                    
        elif action == "import":
            # Import feedback data
            if not file:
                console.print("❌ File required for import action")
                return
                
            import json
            import_data = json.load(file)
            
            async with client() as c:
                resp = await c.post(
                    f"{settings.feedback_api}/v1/feedback/bulk",
                    json=import_data
                )
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"✅ Imported {result.get('imported_count', 0)} feedback entries")
                
                if result.get("errors"):
                    console.print(f"❌ {len(result.get('errors', []))} errors occurred")
                    
        elif action == "delete":
            # Bulk delete feedback
            params = {}
            if category:
                params["category"] = category
            if status:
                params["status"] = status
                
            # Confirm deletion
            confirm = typer.confirm("Are you sure you want to delete feedback entries?")
            if not confirm:
                console.print("❌ Operation cancelled")
                return
                
            async with client() as c:
                resp = await c.delete(f"{settings.feedback_api}/v1/feedback/bulk", params=params)
                resp.raise_for_status()
                result = resp.json()
                
                console.print(f"🗑️  Deleted {result.get('deleted_count', 0)} feedback entries")

    _run(_action)

@app.command()
def tags(
    popular: bool = typer.Option(False, "--popular", "-p", help="Show popular tags only"),
    limit: int = typer.Option(50, "--limit", "-l", help="Results limit"),
) -> None:
    """List feedback tags."""
    settings = get_settings()

    async def _action():
        params = {"limit": limit}
        if popular:
            params["popular"] = True
            
        async with client() as c:
            resp = await c.get(f"{settings.feedback_api}/v1/feedback/tags", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Feedback Tags")
            table.add_column("Tag")
            table.add_column("Count")
            table.add_column("Category")
            table.add_column("Sentiment")
            
            for tag_data in data.get("tags", []):
                table.add_row(
                    tag_data.get("tag", ""),
                    str(tag_data.get("count", 0)),
                    tag_data.get("category", ""),
                    tag_data.get("sentiment", ""),
                )
            
            console.print(table)

    _run(_action)

@app.command()
def github(
    feedback_id: int = typer.Argument(..., help="Feedback ID"),
    create_issue: bool = typer.Option(False, "--create", "-c", help="Create GitHub issue"),
    repository: Optional[str] = typer.Option(None, "--repo", "-r", help="GitHub repository"),
) -> None:
    """GitHub integration for feedback."""
    settings = get_settings()

    async def _action():
        if create_issue:
            payload = {"create_issue": True}
            if repository:
                payload["repository"] = repository
                
            async with client() as c:
                resp = await c.post(
                    f"{settings.feedback_api}/v1/feedback/{feedback_id}/github",
                    json=payload
                )
                resp.raise_for_status()
                data = resp.json()
                
                console.print(f"✅ GitHub issue created")
                console.print(f"Issue URL: {data.get('issue_url', '')}")
                console.print(f"Issue Number: #{data.get('issue_number', '')}")
        else:
            # Show GitHub integration status
            async with client() as c:
                resp = await c.get(f"{settings.feedback_api}/v1/feedback/{feedback_id}/github")
                resp.raise_for_status()
                data = resp.json()
                
                if data.get("github_issue"):
                    issue = data.get("github_issue", {})
                    console.print(f"🔗 GitHub Issue: #{issue.get('number', '')}")
                    console.print(f"URL: {issue.get('url', '')}")
                    console.print(f"Status: {issue.get('state', '')}")
                else:
                    console.print("❌ No GitHub issue linked")

    _run(_action)
