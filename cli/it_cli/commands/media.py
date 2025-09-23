"""Media forensics and analysis commands."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..http import client

app = typer.Typer(help="Media Forensics & Analysis")
console = Console()

def _run(action):
    asyncio.run(action())

@app.command()
def analyze(
    file: Path = typer.Argument(..., help="Media file to analyze"),
    format_check: bool = typer.Option(True, "--format", "-f", help="Check file format"),
    metadata: bool = typer.Option(True, "--metadata", "-m", help="Extract metadata"),
    forensics: bool = typer.Option(True, "--forensics", help="Forensic analysis"),
) -> None:
    """Analyze media file for forensic evidence."""
    if not file.exists():
        console.print(f"❌ File not found: {file}")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        # Read file content
        file_content = file.read_bytes()
        
        # Prepare analysis options
        options = {
            "format_check": format_check,
            "extract_metadata": metadata,
            "forensic_analysis": forensics
        }
        
        async with client() as c:
            # Use multipart form data for file upload
            files = {"file": (file.name, file_content)}
            data = {"options": options}
            
            resp = await c.post(
                f"{settings.media_forensics_api}/v1/images/analyze",
                files=files,
                data=data
            )
            resp.raise_for_status()
            result = resp.json()
            
            console.print(f"📷 Media Analysis: {file.name}")
            console.print(f"File Type: {result.get('file_type', 'Unknown')}")
            console.print(f"Size: {result.get('file_size', 0)} bytes")
            console.print(f"Hash (SHA256): {result.get('sha256', '')}")
            
            # Show metadata if extracted
            if result.get("metadata"):
                table = Table(title="Metadata")
                table.add_column("Field")
                table.add_column("Value")
                
                metadata_dict = result.get("metadata", {})
                for key, value in metadata_dict.items():
                    table.add_row(key.replace("_", " ").title(), str(value))
                
                console.print(table)
            
            # Show forensic analysis
            if result.get("forensic_analysis"):
                forensic = result.get("forensic_analysis", {})
                console.print("\n🔍 Forensic Analysis:")
                console.print(f"Manipulation Score: {forensic.get('manipulation_score', 0)}")
                console.print(f"Authenticity: {forensic.get('authenticity', 'Unknown')}")
                
                if forensic.get("findings"):
                    console.print("Findings:")
                    for finding in forensic.get("findings", []):
                        console.print(f"  • {finding}")

    _run(_action)

@app.command()
def compare(
    file1: Path = typer.Argument(..., help="First media file"),
    file2: Path = typer.Argument(..., help="Second media file"),
    method: str = typer.Option("perceptual", "--method", "-m", help="Comparison method"),
    threshold: float = typer.Option(0.8, "--threshold", "-t", help="Similarity threshold"),
) -> None:
    """Compare two media files for similarity."""
    if not file1.exists():
        console.print(f"❌ File not found: {file1}")
        raise typer.Exit(1)
    
    if not file2.exists():
        console.print(f"❌ File not found: {file2}")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        # Read file contents
        file1_content = file1.read_bytes()
        file2_content = file2.read_bytes()
        
        async with client() as c:
            # Use multipart form data for file uploads
            files = {
                "file1": (file1.name, file1_content),
                "file2": (file2.name, file2_content)
            }
            data = {
                "method": method,
                "threshold": threshold
            }
            
            resp = await c.post(
                f"{settings.media_forensics_api}/v1/images/compare",
                files=files,
                data=data
            )
            resp.raise_for_status()
            result = resp.json()
            
            console.print(f"🔍 Media Comparison")
            console.print(f"File 1: {file1.name}")
            console.print(f"File 2: {file2.name}")
            console.print(f"Method: {method}")
            console.print(f"Similarity Score: {result.get('similarity_score', 0)}")
            console.print(f"Is Match: {'✅' if result.get('is_match', False) else '❌'}")
            
            # Show detailed comparison
            if result.get("comparison_details"):
                details = result.get("comparison_details", {})
                
                table = Table(title="Comparison Details")
                table.add_column("Metric")
                table.add_column("Value")
                
                for key, value in details.items():
                    table.add_row(key.replace("_", " ").title(), str(value))
                
                console.print(table)

    _run(_action)

@app.command()
def similar(
    file: Path = typer.Argument(..., help="Media file to find similar matches"),
    limit: int = typer.Option(10, "--limit", "-l", help="Results limit"),
    threshold: float = typer.Option(0.7, "--threshold", "-t", help="Similarity threshold"),
) -> None:
    """Find similar media files."""
    if not file.exists():
        console.print(f"❌ File not found: {file}")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        # Read file content
        file_content = file.read_bytes()
        
        async with client() as c:
            # Upload file and get hash first
            files = {"file": (file.name, file_content)}
            resp = await c.post(
                f"{settings.media_forensics_api}/v1/images/analyze",
                files=files
            )
            resp.raise_for_status()
            analysis = resp.json()
            
            file_hash = analysis.get("sha256", "")
            if not file_hash:
                console.print("❌ Could not generate file hash")
                return
            
            # Search for similar files
            params = {
                "limit": limit,
                "threshold": threshold
            }
            
            resp = await c.get(
                f"{settings.media_forensics_api}/v1/images/similar/{file_hash}",
                params=params
            )
            resp.raise_for_status()
            result = resp.json()
            
            similar_files = result.get("similar_files", [])
            
            console.print(f"🔍 Similar Files for: {file.name}")
            console.print(f"Found: {len(similar_files)} matches")
            
            if similar_files:
                table = Table(title="Similar Files")
                table.add_column("File")
                table.add_column("Similarity")
                table.add_column("Hash")
                table.add_column("Source")
                
                for similar in similar_files:
                    table.add_row(
                        similar.get("filename", "")[:30],
                        str(similar.get("similarity_score", 0)),
                        similar.get("hash", "")[:16] + "...",
                        similar.get("source", "")[:20],
                    )
                
                console.print(table)

    _run(_action)

@app.command()
def batch(
    directory: Path = typer.Argument(..., help="Directory containing media files"),
    pattern: str = typer.Option("*", "--pattern", "-p", help="File pattern"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
    max_files: int = typer.Option(10, "--max", "-m", help="Maximum files to process"),
) -> None:
    """Batch analyze multiple media files."""
    if not directory.exists():
        console.print(f"❌ Directory not found: {directory}")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        # Find files matching pattern
        files = list(directory.glob(pattern))[:max_files]
        
        if not files:
            console.print(f"❌ No files found matching pattern: {pattern}")
            return
        
        console.print(f"📁 Processing {len(files)} files from: {directory}")
        
        # Prepare files for batch upload
        file_data = []
        for file_path in files:
            if file_path.is_file():
                file_data.append({
                    "filename": file_path.name,
                    "content": file_path.read_bytes()
                })
        
        async with client() as c:
            # Use batch analysis endpoint
            files_upload = [
                ("files", (f["filename"], f["content"]))
                for f in file_data
            ]
            
            resp = await c.post(
                f"{settings.media_forensics_api}/v1/images/batch/analyze",
                files=files_upload
            )
            resp.raise_for_status()
            result = resp.json()
            
            # Display results
            table = Table(title="Batch Analysis Results")
            table.add_column("File")
            table.add_column("Status")
            table.add_column("Type")
            table.add_column("Size")
            table.add_column("Manipulation")
            
            for analysis in result.get("results", []):
                manipulation = analysis.get("forensic_analysis", {}).get("manipulation_score", 0)
                table.add_row(
                    analysis.get("filename", "")[:25],
                    "✅" if analysis.get("success", False) else "❌",
                    analysis.get("file_type", ""),
                    str(analysis.get("file_size", 0)),
                    str(manipulation),
                )
            
            console.print(table)
            
            # Save results if output specified
            if output:
                import json
                output.write_text(json.dumps(result, indent=2), encoding="utf-8")
                console.print(f"✅ Results saved to: {output}")

    _run(_action)

@app.command()
def formats() -> None:
    """List supported media formats."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.media_forensics_api}/v1/formats")
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Supported Media Formats")
            table.add_column("Format")
            table.add_column("Extensions")
            table.add_column("Analysis Support")
            table.add_column("Comparison Support")
            
            for format_info in data.get("formats", []):
                extensions = ", ".join(format_info.get("extensions", []))
                table.add_row(
                    format_info.get("name", ""),
                    extensions,
                    "✅" if format_info.get("analysis_supported", False) else "❌",
                    "✅" if format_info.get("comparison_supported", False) else "❌",
                )
            
            console.print(table)

    _run(_action)

@app.command()
def metadata(
    file: Path = typer.Argument(..., help="Media file"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table|json"),
) -> None:
    """Extract detailed metadata from media file."""
    if not file.exists():
        console.print(f"❌ File not found: {file}")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        # Read file content
        file_content = file.read_bytes()
        
        async with client() as c:
            # Upload file and get hash first
            files = {"file": (file.name, file_content)}
            resp = await c.post(
                f"{settings.media_forensics_api}/v1/images/analyze",
                files=files
            )
            resp.raise_for_status()
            analysis = resp.json()
            
            file_hash = analysis.get("sha256", "")
            if not file_hash:
                console.print("❌ Could not generate file hash")
                return
            
            # Get detailed metadata
            resp = await c.get(f"{settings.media_forensics_api}/v1/images/{file_hash}/metadata")
            resp.raise_for_status()
            result = resp.json()
            
            if format == "json":
                console.print_json(data=result)
            else:
                console.print(f"📷 Metadata for: {file.name}")
                
                metadata = result.get("metadata", {})
                
                # Basic info
                console.print(f"Hash: {file_hash}")
                console.print(f"Size: {metadata.get('file_size', 0)} bytes")
                console.print(f"Format: {metadata.get('format', 'Unknown')}")
                
                # EXIF data if available
                if metadata.get("exif"):
                    table = Table(title="EXIF Data")
                    table.add_column("Field")
                    table.add_column("Value")
                    
                    exif_data = metadata.get("exif", {})
                    for key, value in exif_data.items():
                        table.add_row(key.replace("_", " ").title(), str(value))
                    
                    console.print(table)
                
                # Technical details
                if metadata.get("technical"):
                    table = Table(title="Technical Details")
                    table.add_column("Property")
                    table.add_column("Value")
                    
                    technical = metadata.get("technical", {})
                    for key, value in technical.items():
                        table.add_row(key.replace("_", " ").title(), str(value))
                    
                    console.print(table)

    _run(_action)

@app.command()
def hashes(
    file: Path = typer.Argument(..., help="Media file"),
    algorithms: List[str] = typer.Option(["sha256"], "--algo", "-a", help="Hash algorithms"),
) -> None:
    """Generate multiple hashes for media file."""
    if not file.exists():
        console.print(f"❌ File not found: {file}")
        raise typer.Exit(1)

    settings = get_settings()

    async def _action():
        # Read file content
        file_content = file.read_bytes()
        
        async with client() as c:
            files = {"file": (file.name, file_content)}
            data = {"algorithms": algorithms}
            
            resp = await c.post(
                f"{settings.media_forensics_api}/v1/images/hashes",
                files=files,
                data=data
            )
            resp.raise_for_status()
            result = resp.json()
            
            console.print(f"🔐 Hashes for: {file.name}")
            
            table = Table(title="File Hashes")
            table.add_column("Algorithm")
            table.add_column("Hash")
            
            hashes = result.get("hashes", {})
            for algo, hash_value in hashes.items():
                table.add_row(algo.upper(), hash_value)
            
            console.print(table)

    _run(_action)

@app.command()
def stats() -> None:
    """Show media forensics statistics."""
    settings = get_settings()

    async def _action():
        async with client() as c:
            resp = await c.get(f"{settings.media_forensics_api}/v1/stats")
            resp.raise_for_status()
            data = resp.json()
            
            table = Table(title="Media Forensics Statistics")
            table.add_column("Metric")
            table.add_column("Value")
            
            stats = data.get("stats", {})
            for key, value in stats.items():
                table.add_row(key.replace("_", " ").title(), str(value))
            
            console.print(table)

    _run(_action)
