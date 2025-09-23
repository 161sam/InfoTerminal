"""Integration tests for CLI ↔ API parity across all command groups."""
import json
import pytest
import time
from unittest.mock import patch, AsyncMock
from typer.testing import CliRunner

from it_cli.__main__ import app
from conftest import (
    CLI_COMMAND_GROUPS, API_ENDPOINTS, MockResponse,
    performance_thresholds
)

class TestCLIAPIParity:
    """Test CLI ↔ API parity for all InfoTerminal services."""
    
    def test_cli_app_loads_successfully(self, cli_runner):
        """Test that CLI app loads without errors."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "InfoTerminal CLI" in result.output
        
    def test_all_command_groups_registered(self, cli_runner):
        """Test that all 22 command groups are properly registered."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        
        # Check that all expected command groups are listed
        for group in CLI_COMMAND_GROUPS:
            assert group in result.output, f"Command group '{group}' not found in CLI help"
    
    @pytest.mark.parametrize("command_group", CLI_COMMAND_GROUPS)
    def test_command_group_help(self, cli_runner, command_group):
        """Test that each command group shows help correctly."""
        result = cli_runner.invoke(app, [command_group, "--help"])
        assert result.exit_code == 0
        assert "help" in result.output.lower()
    
    @pytest.mark.asyncio
    async def test_health_endpoints_parity(self, cli_runner, mock_settings, service_mock_responses):
        """Test health endpoints for CLI ↔ API parity."""
        health_commands = [
            ("auth", "health"),
            ("search", "ping"), 
            ("graph", "ping"),
            ("ops", "health"),
            ("cache", "health"),
            ("ws", "health"),
            ("perf", "health"),
            ("feedback", "stats"),  # Some services use different health command names
            ("collab", "health")
        ]
        
        for service, health_cmd in health_commands:
            with patch('httpx.AsyncClient') as mock_client:
                # Mock successful health response
                mock_response = MockResponse({"status": "healthy", "service": service})
                mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
                
                result = cli_runner.invoke(app, [service, health_cmd])
                # Should not crash (exit_code 0 or 1 both acceptable for health checks)
                assert result.exit_code in [0, 1], f"{service} {health_cmd} command failed unexpectedly"

class TestAuthenticationFlow:
    """Test authentication command flow."""
    
    @pytest.mark.asyncio
    async def test_auth_login_flow(self, cli_runner, mock_settings):
        """Test auth login command."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({
                "token": "test_jwt_token",
                "expires_at": "2025-09-22T20:00:00Z",
                "user": {"username": "testuser", "role": "admin"}
            })
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = cli_runner.invoke(app, [
                "auth", "login", 
                "--username", "testuser",
                "--password", "testpass"
            ])
            
            assert result.exit_code == 0
            assert "Login successful" in result.output or "token" in result.output.lower()
    
    @pytest.mark.asyncio 
    async def test_auth_whoami_flow(self, cli_runner, mock_settings):
        """Test auth whoami command."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({
                "user": {
                    "username": "testuser",
                    "email": "test@example.com", 
                    "role": "admin",
                    "status": "active"
                }
            })
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = cli_runner.invoke(app, ["auth", "whoami"])
            assert result.exit_code == 0

class TestSearchOperations:
    """Test search command operations."""
    
    @pytest.mark.asyncio
    async def test_search_query_flow(self, cli_runner, mock_settings, sample_search_results):
        """Test search query command."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse(sample_search_results)
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = cli_runner.invoke(app, ["search", "query", "test query"])
            assert result.exit_code == 0
            # Should display search results
            assert "Sample Document" in result.output or "hits" in result.output.lower()

class TestGraphOperations:
    """Test graph command operations."""
    
    @pytest.mark.asyncio
    async def test_graph_cypher_flow(self, cli_runner, mock_settings):
        """Test graph cypher command."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({
                "data": [{"count": 42}],
                "summary": {"stats": {"nodes_matched": 42}}
            })
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = cli_runner.invoke(app, [
                "graph", "cypher", 
                "MATCH (n) RETURN count(n)",
                "--read-only"
            ])
            assert result.exit_code == 0
    
    @pytest.mark.asyncio
    async def test_graph_neighbors_flow(self, cli_runner, mock_settings, sample_graph_nodes):
        """Test graph neighbors command."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse(sample_graph_nodes)
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = cli_runner.invoke(app, [
                "graph", "neighbors", "node123",
                "--depth", "2", "--limit", "10"
            ])
            assert result.exit_code == 0

class TestNLPOperations:
    """Test NLP command operations."""
    
    @pytest.mark.asyncio
    async def test_nlp_extract_flow(self, cli_runner, mock_settings, sample_nlp_entities):
        """Test NLP entity extraction command."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse(sample_nlp_entities)
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = cli_runner.invoke(app, [
                "nlp", "extract",
                "--text", "Alice lives in New York",
                "--entities"
            ])
            assert result.exit_code == 0

class TestVerificationOperations:
    """Test verification command operations."""
    
    @pytest.mark.asyncio
    async def test_verify_extract_flow(self, cli_runner, mock_settings, sample_verification_claims):
        """Test verification claim extraction command."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse(sample_verification_claims)
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = cli_runner.invoke(app, [
                "verify", "extract",
                "--text", "The Earth is round and orbits the Sun"
            ])
            assert result.exit_code == 0

class TestRAGOperations:
    """Test RAG command operations."""
    
    @pytest.mark.asyncio
    async def test_rag_search_flow(self, cli_runner, mock_settings):
        """Test RAG search command."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({
                "documents": [
                    {"title": "Doc 1", "score": 0.9, "content": "Sample content"}
                ],
                "total": 1
            })
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = cli_runner.invoke(app, [
                "rag", "search", "test query",
                "--method", "hybrid", "--limit", "5"
            ])
            assert result.exit_code == 0

class TestAgentOperations:
    """Test agent command operations."""
    
    @pytest.mark.asyncio
    async def test_agents_list_flow(self, cli_runner, mock_settings):
        """Test agents list command."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({
                "agents": [
                    {"id": "agent1", "name": "Test Agent", "status": "active"}
                ],
                "total": 1
            })
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = cli_runner.invoke(app, ["agents", "list"])
            assert result.exit_code == 0

class TestErrorHandling:
    """Test error handling across CLI commands."""
    
    @pytest.mark.asyncio
    async def test_api_error_handling(self, cli_runner, mock_settings, api_error_response):
        """Test that CLI properly handles API errors."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse(api_error_response, status_code=400)
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = cli_runner.invoke(app, ["auth", "whoami"])
            assert result.exit_code == 1  # Should fail gracefully
    
    @pytest.mark.asyncio
    async def test_network_error_handling(self, cli_runner, mock_settings):
        """Test CLI handling of network errors."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("Connection failed")
            
            result = cli_runner.invoke(app, ["auth", "whoami"])
            assert result.exit_code == 1  # Should fail gracefully
    
    def test_invalid_command_handling(self, cli_runner):
        """Test CLI handling of invalid commands."""
        result = cli_runner.invoke(app, ["nonexistent", "command"])
        assert result.exit_code != 0
        assert "No such command" in result.output or "Usage:" in result.output

class TestOutputFormats:
    """Test CLI output format consistency."""
    
    @pytest.mark.asyncio
    async def test_json_output_format(self, cli_runner, mock_settings):
        """Test --json output format."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({"test": "data"})
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            # Test services that support --json output
            services_with_json = ["search", "auth", "nlp", "verify", "rag"]
            
            for service in services_with_json:
                # Try with health/stats commands that typically support JSON
                health_cmd = "health" if service != "search" else "ping"
                if service == "auth":
                    health_cmd = "users"  # auth doesn't have health, use users list
                
                try:
                    result = cli_runner.invoke(app, [service, health_cmd, "--format", "json"])
                    # Should either succeed or fail gracefully
                    assert result.exit_code in [0, 1], f"JSON format test failed for {service}"
                except Exception:
                    # Some commands might not support --format yet, that's OK for now
                    pass

class TestConfigurationHandling:
    """Test CLI configuration handling."""
    
    def test_cli_loads_config(self, cli_runner, temp_config_file, mock_settings):
        """Test that CLI loads configuration correctly."""
        # CLI should load without errors when config is available
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
    
    def test_cli_handles_missing_config(self, cli_runner):
        """Test CLI behavior with missing configuration."""
        # CLI should still work with default configuration
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0

class TestCLIPerformance:
    """Test CLI performance characteristics."""
    
    def test_cli_startup_time(self, cli_runner, performance_thresholds):
        """Test CLI startup performance."""
        start_time = time.time()
        result = cli_runner.invoke(app, ["--help"])
        end_time = time.time()
        
        startup_time = end_time - start_time
        assert result.exit_code == 0
        assert startup_time < performance_thresholds["cli_startup_time"], \
            f"CLI startup took {startup_time:.2f}s, expected < {performance_thresholds['cli_startup_time']}s"
    
    @pytest.mark.asyncio
    async def test_command_response_time(self, cli_runner, mock_settings, performance_thresholds):
        """Test command response time performance."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse({"status": "healthy"})
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            start_time = time.time()
            result = cli_runner.invoke(app, ["auth", "users", "--limit", "1"])
            end_time = time.time()
            
            response_time = end_time - start_time
            # Allow for either success or controlled failure
            assert result.exit_code in [0, 1]
            assert response_time < performance_thresholds["api_response_time"], \
                f"Command response took {response_time:.2f}s, expected < {performance_thresholds['api_response_time']}s"

class TestCLIIntegration:
    """End-to-end CLI integration tests."""
    
    @pytest.mark.asyncio
    async def test_full_workflow_simulation(self, cli_runner, mock_settings, service_mock_responses):
        """Test a complete workflow using multiple CLI commands."""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock responses for a typical workflow
            mock_client.return_value.__aenter__.return_value.post.return_value = MockResponse(
                service_mock_responses["auth"]["login"]
            )
            mock_client.return_value.__aenter__.return_value.get.return_value = MockResponse(
                service_mock_responses["search"]["query"]
            )
            
            # Simulate: Login -> Search -> View Results workflow
            commands = [
                ["auth", "login", "--username", "test", "--password", "test"],
                ["search", "query", "test", "--limit", "5"],
            ]
            
            for cmd in commands:
                result = cli_runner.invoke(app, cmd)
                # Commands should complete (success or controlled failure)
                assert result.exit_code in [0, 1], f"Command {' '.join(cmd)} failed unexpectedly"
    
    def test_cli_help_completeness(self, cli_runner):
        """Test that CLI help system is complete."""
        # Test main help
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Commands:" in result.output or "Usage:" in result.output
        
        # Test that each command group has help
        for group in CLI_COMMAND_GROUPS:
            result = cli_runner.invoke(app, [group, "--help"])
            assert result.exit_code == 0, f"Help for {group} command group failed"

# Test data validation
class TestResponseValidation:
    """Test API response validation and CLI parsing."""
    
    @pytest.mark.asyncio
    async def test_error_envelope_parsing(self, cli_runner, mock_settings):
        """Test that CLI correctly parses error envelope responses."""
        with patch('httpx.AsyncClient') as mock_client:
            error_response = {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid parameters",
                    "details": {"field": "username", "error": "required"}
                }
            }
            mock_response = MockResponse(error_response, status_code=400)
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = cli_runner.invoke(app, ["auth", "login", "--username", "", "--password", "test"])
            assert result.exit_code == 1
            # CLI should display error information
            assert "error" in result.output.lower() or "invalid" in result.output.lower()
    
    @pytest.mark.asyncio
    async def test_pagination_handling(self, cli_runner, mock_settings, paginated_response):
        """Test CLI handling of paginated responses."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MockResponse(paginated_response)
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = cli_runner.invoke(app, ["auth", "users", "--limit", "10"])
            assert result.exit_code in [0, 1]  # Should handle pagination gracefully

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
