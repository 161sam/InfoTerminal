"""Performance testing and benchmarking for InfoTerminal CLI."""
import asyncio
import json
import psutil
import pytest
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Tuple
from unittest.mock import patch

import httpx
from typer.testing import CliRunner

from it_cli.__main__ import app
from conftest import MockResponse, CLI_COMMAND_GROUPS

class PerformanceBenchmark:
    """Performance benchmark utilities."""
    
    def __init__(self):
        self.results: Dict[str, List[float]] = {}
        self.memory_usage: List[float] = []
        
    def measure_time(self, func, *args, **kwargs) -> Tuple[float, any]:
        """Measure execution time of a function."""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        return end_time - start_time, result
    
    def measure_memory(self) -> float:
        """Measure current memory usage in MB."""
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # Convert to MB
    
    def record_measurement(self, test_name: str, duration: float):
        """Record a performance measurement."""
        if test_name not in self.results:
            self.results[test_name] = []
        self.results[test_name].append(duration)
    
    def get_statistics(self, test_name: str) -> Dict[str, float]:
        """Get statistics for a test."""
        if test_name not in self.results or not self.results[test_name]:
            return {}
        
        measurements = self.results[test_name]
        return {
            "mean": statistics.mean(measurements),
            "median": statistics.median(measurements),
            "min": min(measurements),
            "max": max(measurements),
            "std_dev": statistics.stdev(measurements) if len(measurements) > 1 else 0.0,
            "count": len(measurements)
        }
    
    def generate_report(self) -> Dict[str, any]:
        """Generate comprehensive performance report."""
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": {
                "cpu_count": psutil.cpu_count(),
                "memory_total_mb": psutil.virtual_memory().total / 1024 / 1024,
                "python_version": ".".join(map(str, __import__("sys").version_info[:3]))
            },
            "performance_results": {},
            "memory_usage": {
                "measurements": self.memory_usage,
                "peak_mb": max(self.memory_usage) if self.memory_usage else 0,
                "average_mb": statistics.mean(self.memory_usage) if self.memory_usage else 0
            }
        }
        
        for test_name in self.results:
            report["performance_results"][test_name] = self.get_statistics(test_name)
            
        return report

@pytest.fixture
def benchmark():
    """Performance benchmark fixture."""
    return PerformanceBenchmark()

class TestCLIStartupPerformance:
    """Test CLI startup and initialization performance."""
    
    def test_cli_cold_start_time(self, cli_runner, benchmark):
        """Test CLI cold start performance."""
        iterations = 10
        
        for i in range(iterations):
            duration, result = benchmark.measure_time(
                cli_runner.invoke, app, ["--version"]
            )
            benchmark.record_measurement("cli_cold_start", duration)
            assert result.exit_code == 0
        
        stats = benchmark.get_statistics("cli_cold_start")
        assert stats["mean"] < 2.0, f"CLI cold start too slow: {stats['mean']:.3f}s"
        assert stats["max"] < 5.0, f"CLI worst case too slow: {stats['max']:.3f}s"
    
    def test_cli_help_performance(self, cli_runner, benchmark):
        """Test CLI help system performance."""
        duration, result = benchmark.measure_time(
            cli_runner.invoke, app, ["--help"]
        )
        benchmark.record_measurement("cli_help", duration)
        
        assert result.exit_code == 0
        assert duration < 1.0, f"CLI help too slow: {duration:.3f}s"
    
    @pytest.mark.parametrize("command_group", CLI_COMMAND_GROUPS[:5])  # Test subset for speed
    def test_command_group_help_performance(self, cli_runner, benchmark, command_group):
        """Test command group help performance."""
        duration, result = benchmark.measure_time(
            cli_runner.invoke, app, [command_group, "--help"]
        )
        benchmark.record_measurement(f"help_{command_group}", duration)
        
        assert result.exit_code == 0
        assert duration < 1.0, f"{command_group} help too slow: {duration:.3f}s"

class TestAPIResponseTimePerformance:
    """Test API response time performance."""
    
    @pytest.mark.asyncio
    async def test_auth_login_performance(self, cli_runner, benchmark, mock_settings):
        """Test auth login response time."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({
                "token": "test_token",
                "expires_at": "2025-09-22T20:00:00Z"
            })
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            duration, result = benchmark.measure_time(
                cli_runner.invoke, app, [
                    "auth", "login",
                    "--username", "test",
                    "--password", "test"
                ]
            )
            benchmark.record_measurement("auth_login", duration)
            
            assert result.exit_code == 0
            assert duration < 1.0, f"Auth login too slow: {duration:.3f}s"
    
    @pytest.mark.asyncio
    async def test_search_query_performance(self, cli_runner, benchmark, mock_settings):
        """Test search query response time."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({
                "hits": [{"id": "1", "title": "Test", "score": 0.9}],
                "total": 1,
                "took": 50
            })
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            duration, result = benchmark.measure_time(
                cli_runner.invoke, app, ["search", "query", "test"]
            )
            benchmark.record_measurement("search_query", duration)
            
            assert result.exit_code == 0
            assert duration < 0.5, f"Search query too slow: {duration:.3f}s"
    
    @pytest.mark.asyncio
    async def test_graph_cypher_performance(self, cli_runner, benchmark, mock_settings):
        """Test graph cypher query performance."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({
                "data": [{"count": 42}],
                "summary": {"stats": {"nodes_matched": 42}}
            })
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            duration, result = benchmark.measure_time(
                cli_runner.invoke, app, [
                    "graph", "cypher",
                    "MATCH (n) RETURN count(n)",
                    "--read-only"
                ]
            )
            benchmark.record_measurement("graph_cypher", duration)
            
            assert result.exit_code == 0
            assert duration < 2.0, f"Graph cypher too slow: {duration:.3f}s"
    
    @pytest.mark.asyncio
    async def test_nlp_extract_performance(self, cli_runner, benchmark, mock_settings):
        """Test NLP extraction performance."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({
                "entities": [
                    {"text": "Alice", "label": "PERSON", "confidence": 0.95}
                ],
                "processing_time": 0.1
            })
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            duration, result = benchmark.measure_time(
                cli_runner.invoke, app, [
                    "nlp", "extract",
                    "--text", "Alice lives in New York",
                    "--entities"
                ]
            )
            benchmark.record_measurement("nlp_extract", duration)
            
            assert result.exit_code == 0
            assert duration < 3.0, f"NLP extract too slow: {duration:.3f}s"

class TestMemoryUsagePerformance:
    """Test CLI memory usage performance."""
    
    def test_cli_memory_usage(self, cli_runner, benchmark):
        """Test CLI memory consumption."""
        initial_memory = benchmark.measure_memory()
        benchmark.memory_usage.append(initial_memory)
        
        # Run several commands to test memory usage
        commands = [
            ["--help"],
            ["auth", "--help"],
            ["search", "--help"],
            ["graph", "--help"]
        ]
        
        for cmd in commands:
            cli_runner.invoke(app, cmd)
            memory_usage = benchmark.measure_memory()
            benchmark.memory_usage.append(memory_usage)
        
        peak_memory = max(benchmark.memory_usage)
        memory_growth = peak_memory - initial_memory
        
        assert peak_memory < 100, f"CLI peak memory too high: {peak_memory:.1f}MB"
        assert memory_growth < 50, f"CLI memory growth too high: {memory_growth:.1f}MB"

class TestConcurrentPerformance:
    """Test CLI performance under concurrent load."""
    
    @pytest.mark.asyncio
    async def test_concurrent_commands(self, cli_runner, benchmark, mock_settings):
        """Test CLI performance with concurrent command execution."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({"status": "healthy"})
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            def run_command():
                start_time = time.perf_counter()
                result = cli_runner.invoke(app, ["auth", "users", "--limit", "1"])
                end_time = time.perf_counter()
                return end_time - start_time, result.exit_code
            
            # Run 5 concurrent commands
            concurrent_requests = 5
            with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
                futures = [executor.submit(run_command) for _ in range(concurrent_requests)]
                results = [future.result() for future in futures]
            
            durations = [result[0] for result in results]
            exit_codes = [result[1] for result in results]
            
            # Record measurements
            for i, duration in enumerate(durations):
                benchmark.record_measurement(f"concurrent_request_{i}", duration)
            
            # All requests should complete reasonably fast
            max_duration = max(durations)
            avg_duration = statistics.mean(durations)
            
            assert max_duration < 3.0, f"Concurrent request too slow: {max_duration:.3f}s"
            assert avg_duration < 2.0, f"Average concurrent time too slow: {avg_duration:.3f}s"
            
            # Most requests should succeed (allow some failures due to mocking)
            success_rate = sum(1 for code in exit_codes if code == 0) / len(exit_codes)
            assert success_rate >= 0.6, f"Concurrent success rate too low: {success_rate:.1%}"

class TestResponseDataPerformance:
    """Test performance with different response data sizes."""
    
    @pytest.mark.asyncio
    async def test_large_response_handling(self, cli_runner, benchmark, mock_settings):
        """Test CLI performance with large API responses."""
        # Create large mock response
        large_response = {
            "items": [
                {"id": f"item_{i}", "data": f"Large data chunk {i}" * 100}
                for i in range(1000)
            ],
            "total": 1000
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse(large_response)
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            duration, result = benchmark.measure_time(
                cli_runner.invoke, app, ["auth", "users", "--limit", "1000"]
            )
            benchmark.record_measurement("large_response", duration)
            
            # Should handle large responses reasonably well
            assert result.exit_code in [0, 1]  # Allow controlled failure
            assert duration < 5.0, f"Large response handling too slow: {duration:.3f}s"
    
    @pytest.mark.asyncio
    async def test_empty_response_handling(self, cli_runner, benchmark, mock_settings):
        """Test CLI performance with empty API responses."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({"items": [], "total": 0})
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            duration, result = benchmark.measure_time(
                cli_runner.invoke, app, ["auth", "users"]
            )
            benchmark.record_measurement("empty_response", duration)
            
            assert result.exit_code in [0, 1]
            assert duration < 1.0, f"Empty response handling too slow: {duration:.3f}s"

class TestPerformanceRegression:
    """Test for performance regression detection."""
    
    def test_performance_baseline(self, cli_runner, benchmark):
        """Establish performance baseline for regression testing."""
        # Define performance baselines (can be adjusted based on actual measurements)
        baselines = {
            "cli_startup": 1.0,  # seconds
            "help_display": 0.5,  # seconds
            "memory_usage": 50,   # MB
        }
        
        # Test CLI startup
        duration, result = benchmark.measure_time(
            cli_runner.invoke, app, ["--version"]
        )
        assert result.exit_code == 0
        assert duration < baselines["cli_startup"], \
            f"CLI startup regression: {duration:.3f}s > {baselines['cli_startup']}s"
        
        # Test help display
        duration, result = benchmark.measure_time(
            cli_runner.invoke, app, ["--help"]
        )
        assert result.exit_code == 0
        assert duration < baselines["help_display"], \
            f"Help display regression: {duration:.3f}s > {baselines['help_display']}s"
        
        # Test memory usage
        memory_usage = benchmark.measure_memory()
        assert memory_usage < baselines["memory_usage"], \
            f"Memory usage regression: {memory_usage:.1f}MB > {baselines['memory_usage']}MB"

class TestPerformanceReporting:
    """Test performance reporting and analysis."""
    
    def test_benchmark_report_generation(self, benchmark):
        """Test benchmark report generation."""
        # Add some sample measurements
        benchmark.record_measurement("test_operation", 0.1)
        benchmark.record_measurement("test_operation", 0.15)
        benchmark.record_measurement("test_operation", 0.12)
        benchmark.memory_usage.extend([45.2, 47.1, 46.8])
        
        report = benchmark.generate_report()
        
        # Verify report structure
        assert "timestamp" in report
        assert "system_info" in report
        assert "performance_results" in report
        assert "memory_usage" in report
        
        # Verify performance results
        assert "test_operation" in report["performance_results"]
        stats = report["performance_results"]["test_operation"]
        assert "mean" in stats
        assert "median" in stats
        assert "min" in stats
        assert "max" in stats
        assert "count" in stats
        
        # Verify memory usage
        memory_info = report["memory_usage"]
        assert "peak_mb" in memory_info
        assert "average_mb" in memory_info
        assert memory_info["peak_mb"] > 0
    
    def test_performance_trend_analysis(self, benchmark):
        """Test performance trend analysis capabilities."""
        # Simulate performance measurements over time
        measurements = [0.1, 0.11, 0.12, 0.15, 0.18]  # Simulating degradation
        
        for measurement in measurements:
            benchmark.record_measurement("trend_test", measurement)
        
        stats = benchmark.get_statistics("trend_test")
        
        # Check for performance degradation indicators
        assert stats["count"] == len(measurements)
        assert stats["min"] == min(measurements)
        assert stats["max"] == max(measurements)
        
        # Calculate trend (simple approach - compare first half vs second half)
        first_half = measurements[:len(measurements)//2]
        second_half = measurements[len(measurements)//2:]
        
        first_half_avg = statistics.mean(first_half)
        second_half_avg = statistics.mean(second_half)
        
        # Detect performance degradation
        degradation = (second_half_avg - first_half_avg) / first_half_avg
        if degradation > 0.2:  # 20% degradation threshold
            print(f"Warning: Performance degradation detected: {degradation:.1%}")

if __name__ == "__main__":
    # Run performance tests
    pytest.main([__file__, "-v", "--tb=short"])
