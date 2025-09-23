"""
Standard Pagination Schemas for InfoTerminal APIs

Provides consistent pagination patterns across all services.
All list endpoints MUST use these pagination schemas.
"""

from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field, validator


# Generic type for paginated items
T = TypeVar('T')


class PaginationParams(BaseModel):
    """
    Standard pagination parameters for list endpoints.
    
    Usage:
        @app.get("/v1/documents")
        def list_documents(pagination: PaginationParams = Depends()):
            return paginate_results(documents, pagination)
    """
    page: int = Field(
        default=1, 
        ge=1, 
        description="Page number (1-based)"
    )
    size: int = Field(
        default=20, 
        ge=1, 
        le=100, 
        description="Items per page (max 100)"
    )
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries."""
        return (self.page - 1) * self.size
    
    @property
    def limit(self) -> int:
        """Alias for size for database queries."""
        return self.size


class PaginationMeta(BaseModel):
    """Pagination metadata for responses."""
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standard paginated response format for all InfoTerminal list endpoints.
    
    Example:
    {
        "items": [...],
        "total": 150,
        "page": 1,
        "size": 20,
        "pages": 8,
        "has_next": true,
        "has_prev": false
    }
    """
    items: List[T] = Field(..., description="List of items for current page")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        pagination: PaginationParams
    ) -> 'PaginatedResponse[T]':
        """
        Create a paginated response from items and pagination params.
        
        Args:
            items: List of items for current page
            total: Total number of items across all pages
            pagination: Pagination parameters from request
            
        Returns:
            PaginatedResponse with calculated metadata
        """
        pages = (total + pagination.size - 1) // pagination.size  # Ceiling division
        
        return cls(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=pages,
            has_next=pagination.page < pages,
            has_prev=pagination.page > 1
        )


class FilterParams(BaseModel):
    """
    Standard filter parameters for list endpoints.
    
    Usage:
        @app.get("/v1/entities")
        def list_entities(
            pagination: PaginationParams = Depends(),
            filters: FilterParams = Depends()
        ):
            return filter_and_paginate(entities, filters, pagination)
    """
    q: Optional[str] = Field(
        None, 
        description="Search query string"
    )
    sort: Optional[str] = Field(
        None, 
        description="Sort field (prefix with '-' for descending)"
    )
    filter: Optional[str] = Field(
        None,
        description="JSON filter expression"
    )
    
    @property
    def sort_field(self) -> Optional[str]:
        """Extract sort field name without direction prefix."""
        if not self.sort:
            return None
        return self.sort.lstrip('-')
    
    @property
    def sort_desc(self) -> bool:
        """Check if sort direction is descending."""
        return self.sort and self.sort.startswith('-')


class SortOptions(BaseModel):
    """Standard sort options for list endpoints."""
    field: str = Field(..., description="Field to sort by")
    direction: str = Field(
        default="asc",
        pattern="^(asc|desc)$",
        description="Sort direction: 'asc' or 'desc'"
    )


# Helper functions for common pagination patterns
def paginate_query_results(
    items: List[T],
    total: int,
    pagination: PaginationParams
) -> PaginatedResponse[T]:
    """
    Helper to create paginated response from query results.
    
    Args:
        items: Items for current page (already sliced)
        total: Total count from database
        pagination: Pagination parameters
        
    Returns:
        PaginatedResponse with proper metadata
    """
    return PaginatedResponse.create(items, total, pagination)


def calculate_pagination_bounds(pagination: PaginationParams) -> tuple[int, int]:
    """
    Calculate offset and limit for database queries.
    
    Args:
        pagination: Pagination parameters
        
    Returns:
        Tuple of (offset, limit) for database queries
    """
    offset = (pagination.page - 1) * pagination.size
    limit = pagination.size
    return offset, limit
