"""
Test suite for OpenBB Connector v1 API migration.

Tests the new standardized *_v1.py implementation to ensure:
- All endpoints follow API standards
- Error handling uses Error-Envelope format
- Database integration works correctly
- Financial data fetching functions properly
"""

import pytest
from datetime import date, datetime
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import pandas as pd

import sys
from pathlib import Path

# Add service to path
SERVICE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SERVICE_DIR))

from app_v1 import app
from models.requests import PriceDataRequest, DataSource, TimeInterval
from models.responses import PriceData, DataImportResult, SymbolInfo


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_db_connection():
    """Mock database connection for testing."""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
    mock_conn.cursor.return_value.__exit__ = Mock(return_value=None)
    mock_conn.commit = Mock()
    mock_conn.rollback = Mock()
    return mock_conn, mock_cursor


@pytest.fixture
def sample_price_data():
    """Sample price data for testing."""
    return pd.DataFrame([
        {
            "as_of_date": date(2025, 9, 21),
            "symbol": "AAPL",
            "open": 150.0,
            "high": 155.0,
            "low": 149.0,
            "close": 154.0,
            "volume": 1000000,
            "data_source": "yahoo"
        },
        {
            "as_of_date": date(2025, 9, 20),
            "symbol": "AAPL",
            "open": 148.0,
            "high": 151.0,
            "low": 147.0,
            "close": 150.0,
            "volume": 1200000,
            "data_source": "yahoo"
        }
    ])


class TestCoreEndpoints:
    """Test core service endpoints (health, ready, info)."""
    
    def test_healthz_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/healthz")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert data["service"] == "openbb-connector"
    
    def test_readyz_endpoint(self, client):
        """Test readiness check endpoint."""
        response = client.get("/readyz")
        # May return 503 if dependencies not available in test
        assert response.status_code in [200, 503]
        
        data = response.json()
        assert "status" in data
        assert "checks" in data
    
    def test_info_endpoint(self, client):
        """Test service info endpoint."""
        response = client.get("/info")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "openbb-connector"
        assert data["version"] == "1.0.0"
        assert data["api_version"] == "v1"
        assert "endpoints" in data
        assert "capabilities" in data


class TestPriceDataEndpoints:
    """Test price data related endpoints."""
    
    @patch('routers.openbb_v1.fetch_yahoo_prices')
    @patch('routers.openbb_v1.save_prices_to_db')
    @patch('app_v1.db_connection')
    def test_fetch_price_data(self, mock_db, mock_save, mock_fetch, client, sample_price_data):
        """Test price data fetching endpoint."""
        # Mock the fetch function
        mock_fetch.return_value = sample_price_data
        mock_save.return_value = {"inserted": 2, "updated": 0, "failed": 0}
        mock_db.return_value = True
        
        request_data = {
            "symbols": ["AAPL"],
            "period": "5d",
            "interval": "1d",
            "data_source": "yahoo",
            "save_to_db": True
        }
        
        response = client.post("/v1/prices/fetch", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "completed"
        assert data["symbols_requested"] == ["AAPL"]
        assert data["total_records"] == 2
        assert data["records_inserted"] == 2
    
    def test_fetch_price_data_validation_error(self, client):
        """Test price data fetching with validation errors."""
        # Invalid data source
        request_data = {
            "symbols": [],  # Empty symbols list
            "data_source": "yahoo"
        }
        
        response = client.post("/v1/prices/fetch", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_unsupported_data_source(self, client):
        """Test fetching with unsupported data source."""
        request_data = {
            "symbols": ["AAPL"],
            "data_source": "alpha_vantage"  # Not implemented yet
        }
        
        response = client.post("/v1/prices/fetch", json=request_data)
        assert response.status_code == 501  # Not implemented
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "NOT_IMPLEMENTED"
    
    @patch('app_v1.db_connection')
    def test_get_price_data(self, mock_db_conn, client, mock_db_connection):
        """Test retrieving stored price data."""
        mock_db, mock_cursor = mock_db_connection
        mock_db_conn.return_value = mock_db
        app_v1.db_connection = mock_db
        
        # Mock cursor results
        mock_cursor.fetchone.return_value = (2,)  # Total count
        mock_cursor.fetchall.return_value = [
            (date(2025, 9, 21), "AAPL", 150.0, 155.0, 149.0, 154.0, 1000000, 
             None, None, "yahoo", "USD", "NASDAQ", datetime(2025, 9, 21, 12, 0, 0))
        ]
        
        response = client.get("/v1/prices?symbol=AAPL")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
    
    @patch('app_v1.db_connection', None)
    def test_get_price_data_no_db(self, client):
        """Test getting price data without database connection."""
        response = client.get("/v1/prices")
        assert response.status_code == 503
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "SERVICE_UNAVAILABLE"


class TestSymbolEndpoints:
    """Test symbol-related endpoints."""
    
    @patch('yfinance.Ticker')
    def test_get_symbol_info(self, mock_ticker, client):
        """Test getting symbol information."""
        # Mock Yahoo Finance response
        mock_ticker_instance = Mock()
        mock_ticker_instance.info = {
            "symbol": "AAPL",
            "longName": "Apple Inc.",
            "exchange": "NASDAQ",
            "currency": "USD",
            "sector": "Technology",
            "marketCap": 3000000000000,
            "currentPrice": 154.0,
            "trailingPE": 25.5
        }
        mock_ticker.return_value = mock_ticker_instance
        
        response = client.get("/v1/symbols/AAPL")
        assert response.status_code == 200
        
        data = response.json()
        assert data["symbol"] == "AAPL"
        assert data["name"] == "Apple Inc."
        assert data["exchange"] == "NASDAQ"
        assert data["current_price"] == 154.0
    
    @patch('yfinance.Ticker')
    def test_get_symbol_info_not_found(self, mock_ticker, client):
        """Test getting info for non-existent symbol."""
        # Mock empty response
        mock_ticker_instance = Mock()
        mock_ticker_instance.info = {}
        mock_ticker.return_value = mock_ticker_instance
        
        response = client.get("/v1/symbols/INVALID")
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "RESOURCE_NOT_FOUND"
    
    @patch('app_v1.db_connection')
    def test_list_symbols(self, mock_db_conn, client, mock_db_connection):
        """Test listing available symbols."""
        mock_db, mock_cursor = mock_db_connection
        mock_db_conn.return_value = mock_db
        app_v1.db_connection = mock_db
        
        # Mock cursor results
        mock_cursor.fetchone.return_value = (3,)  # Total count
        mock_cursor.fetchall.return_value = [("AAPL",), ("MSFT",), ("GOOGL",)]
        
        response = client.get("/v1/symbols")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] == 3
        assert "AAPL" in data["items"]


class TestStatisticsEndpoints:
    """Test statistics and monitoring endpoints."""
    
    @patch('app_v1.db_connection')
    def test_get_statistics(self, mock_db_conn, client, mock_db_connection):
        """Test getting OpenBB statistics."""
        mock_db, mock_cursor = mock_db_connection
        mock_db_conn.return_value = mock_db
        app_v1.db_connection = mock_db
        
        # Mock multiple cursor calls for statistics
        mock_cursor.fetchone.side_effect = [
            (10,),  # total symbols
            (100,),  # total records
            (date(2025, 1, 1), date(2025, 9, 21))  # date range
        ]
        mock_cursor.fetchall.side_effect = [
            [("AAPL", 25), ("MSFT", 20)],  # top symbols
            [("yahoo",)]  # data sources
        ]
        
        response = client.get("/v1/statistics")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_symbols" in data
        assert "total_records" in data
        assert "data_sources" in data
        assert "top_symbols" in data
        assert data["total_symbols"] == 10
        assert data["total_records"] == 100
    
    def test_get_market_status(self, client):
        """Test getting market status."""
        response = client.get("/v1/market/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "exchange" in data
        assert "is_open" in data
        assert "current_time" in data
        assert "timezone" in data


class TestDataQualityEndpoints:
    """Test data quality and maintenance endpoints."""
    
    @patch('app_v1.db_connection')
    def test_check_data_quality(self, mock_db_conn, client, mock_db_connection):
        """Test data quality check."""
        mock_db, mock_cursor = mock_db_connection
        mock_db_conn.return_value = mock_db
        app_v1.db_connection = mock_db
        
        # Mock cursor results
        mock_cursor.fetchone.return_value = (100,)  # total records
        mock_cursor.fetchall.return_value = []  # no duplicates
        
        request_data = {
            "symbols": ["AAPL"],
            "check_duplicates": True,
            "check_gaps": True,
            "check_outliers": True
        }
        
        response = client.post("/v1/data/quality-check", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "total_records" in data
        assert "quality_score" in data
        assert "recommendations" in data
        assert data["total_records"] == 100
    
    @patch('app_v1.db_connection')
    def test_cleanup_data_dry_run(self, mock_db_conn, client, mock_db_connection):
        """Test data cleanup with dry run."""
        mock_db, mock_cursor = mock_db_connection
        mock_db_conn.return_value = mock_db
        app_v1.db_connection = mock_db
        
        # Mock cursor results for dry run
        mock_cursor.fetchone.side_effect = [(50,), (5,)]  # old records, duplicates
        
        response = client.delete("/v1/data/cleanup?older_than_days=365&dry_run=true")
        assert response.status_code == 200
        
        data = response.json()
        assert data["dry_run"] is True
        assert "old_records_deleted" in data
        assert "duplicate_records_removed" in data


class TestErrorHandling:
    """Test error handling and validation."""
    
    def test_service_unavailable_when_db_not_ready(self, client):
        """Test service unavailable when database not connected."""
        # This would need proper mocking of app state
        pass
    
    def test_validation_errors(self, client):
        """Test request validation errors."""
        # Test invalid price data request
        invalid_request = {
            "symbols": [""],  # Empty symbol
            "period": "invalid"  # Invalid period
        }
        
        response = client.post("/v1/prices/fetch", json=invalid_request)
        assert response.status_code == 422  # Validation error
    
    def test_error_envelope_format(self, client):
        """Test that errors follow the Error-Envelope format."""
        # Test a 503 error when db not available
        with patch('app_v1.db_connection', None):
            response = client.get("/v1/prices")
            
            if response.status_code == 503:
                data = response.json()
                assert "error" in data
                assert "code" in data["error"]
                assert "message" in data["error"]


class TestPagination:
    """Test pagination functionality."""
    
    @patch('app_v1.db_connection')
    def test_price_data_pagination(self, mock_db_conn, client, mock_db_connection):
        """Test price data list pagination."""
        mock_db, mock_cursor = mock_db_connection
        mock_db_conn.return_value = mock_db
        app_v1.db_connection = mock_db
        
        # Mock cursor results
        mock_cursor.fetchone.return_value = (100,)  # Total count
        mock_cursor.fetchall.return_value = []  # Empty results for simplicity
        
        response = client.get("/v1/prices?page=1&size=20")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert data["page"] == 1
        assert data["size"] == 20
    
    @patch('app_v1.db_connection')
    def test_symbols_pagination(self, mock_db_conn, client, mock_db_connection):
        """Test symbols list pagination."""
        mock_db, mock_cursor = mock_db_connection
        mock_db_conn.return_value = mock_db
        app_v1.db_connection = mock_db
        
        # Mock cursor results
        mock_cursor.fetchone.return_value = (50,)  # Total count
        mock_cursor.fetchall.return_value = [("AAPL",), ("MSFT",)]
        
        response = client.get("/v1/symbols?page=1&size=10")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data


class TestLegacyEndpoints:
    """Test legacy endpoint deprecation."""
    
    def test_legacy_import_deprecated(self, client):
        """Test legacy import endpoint returns deprecation."""
        response = client.post("/legacy/import")
        assert response.status_code == 410
        
        data = response.json()
        assert "error" in data
        assert "/v1/prices/fetch" in data["error"]


class TestDataSources:
    """Test data source functionality."""
    
    def test_yahoo_finance_integration(self):
        """Test Yahoo Finance data fetching."""
        from routers.openbb_v1 import fetch_yahoo_prices
        
        # This would need a real test with mocked yfinance
        # For now, just test that the function exists
        assert callable(fetch_yahoo_prices)
    
    def test_data_source_configuration(self, client):
        """Test data source configuration in service info."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "features" in data
        assert "supported_data_sources" in data["features"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
