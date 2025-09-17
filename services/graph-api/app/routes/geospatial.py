# Geospatial routes for InfoTerminal Graph API

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel

# Import geospatial from parent directory
import sys
from pathlib import Path
SERVICE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SERVICE_DIR))
from geospatial import GeospatialService, BoundingBox, GeocodeRequest, GeoEntity

router = APIRouter(prefix="/geo", tags=["geospatial"])


class GeocodeNodeRequest(BaseModel):
    node_id: str
    location_field: str = "name"


class NearbyRequest(BaseModel):
    latitude: float
    longitude: float
    radius_km: float = 10.0
    limit: int = 50


class BatchGeocodeRequest(BaseModel):
    node_type: Optional[str] = None
    location_field: str = "name"
    limit: int = 100


@router.get("/entities")
def get_geo_entities(
    request: Request,
    south: float,
    west: float,
    north: float, 
    east: float,
    limit: int = 100
):
    """Get entities within a bounding box."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        bbox = BoundingBox(south=south, west=west, north=north, east=east)
        geo_service = GeospatialService(driver)
        entities = geo_service.get_entities_by_bbox(bbox, limit)
        
        return {
            "bbox": {
                "south": south,
                "west": west, 
                "north": north,
                "east": east
            },
            "entities": [entity.dict() for entity in entities],
            "count": len(entities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geospatial query error: {str(e)}")


@router.post("/entities/nearby")
def get_nearby_entities(request: Request, nearby_request: NearbyRequest):
    """Get entities near a specific point."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        geo_service = GeospatialService(driver)
        entities = geo_service.get_entities_near_point(
            nearby_request.latitude,
            nearby_request.longitude,
            nearby_request.radius_km,
            nearby_request.limit
        )
        
        return {
            "center": {
                "latitude": nearby_request.latitude,
                "longitude": nearby_request.longitude
            },
            "radius_km": nearby_request.radius_km,
            "entities": [entity.dict() for entity in entities],
            "count": len(entities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Nearby query error: {str(e)}")


@router.post("/geocode")
def geocode_location(request: Request, geocode_request: GeocodeRequest):
    """Geocode a location string."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        geo_service = GeospatialService(driver)
        result = geo_service.geocode_location(
            geocode_request.location,
            geocode_request.country_code
        )
        
        if result:
            return {
                "success": True,
                "location": geocode_request.location,
                **result
            }
        else:
            return {
                "success": False,
                "location": geocode_request.location,
                "error": "Geocoding failed"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geocoding error: {str(e)}")


@router.post("/node/geocode")
def geocode_node(request: Request, geocode_node_request: GeocodeNodeRequest):
    """Geocode a specific node and update it with coordinates."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        geo_service = GeospatialService(driver)
        result = geo_service.geocode_and_update_node(
            geocode_node_request.node_id,
            geocode_node_request.location_field
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Node geocoding error: {str(e)}")


@router.post("/batch-geocode")
def batch_geocode(
    request: Request, 
    background_tasks: BackgroundTasks,
    batch_request: BatchGeocodeRequest
):
    """Start batch geocoding of nodes in the background."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        geo_service = GeospatialService(driver)
        
        # Start as background task to avoid timeout
        background_tasks.add_task(
            geo_service.batch_geocode_nodes,
            batch_request.node_type,
            batch_request.location_field,
            batch_request.limit
        )
        
        return {
            "success": True,
            "message": "Batch geocoding started in background",
            "parameters": {
                "node_type": batch_request.node_type,
                "location_field": batch_request.location_field,
                "limit": batch_request.limit
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch geocoding error: {str(e)}")


@router.get("/statistics")
def geo_statistics(request: Request):
    """Get geospatial statistics."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        geo_service = GeospatialService(driver)
        stats = geo_service.get_geo_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Statistics error: {str(e)}")


class CoordinateUpdate(BaseModel):
    node_id: str
    latitude: float
    longitude: float


@router.post("/node/coordinates")
def update_node_coordinates(request: Request, coord_update: CoordinateUpdate):
    """Manually set coordinates for a node."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        geo_service = GeospatialService(driver)
        success = geo_service.add_coordinates_to_node(
            coord_update.node_id,
            coord_update.latitude,
            coord_update.longitude
        )
        
        if success:
            return {
                "success": True,
                "node_id": coord_update.node_id,
                "coordinates": {
                    "latitude": coord_update.latitude,
                    "longitude": coord_update.longitude
                }
            }
        else:
            raise HTTPException(404, "Node not found or update failed")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Coordinate update error: {str(e)}")


@router.get("/heatmap")  
def geo_heatmap(
    request: Request,
    south: float,
    west: float,
    north: float,
    east: float,
    grid_size: int = 20
):
    """Generate heatmap data for entities in a bounding box."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        geo_service = GeospatialService(driver)
        bbox = BoundingBox(south=south, west=west, north=north, east=east)
        entities = geo_service.get_entities_by_bbox(bbox, limit=1000)
        
        # Create a simple grid for heatmap
        lat_step = (north - south) / grid_size
        lon_step = (east - west) / grid_size
        
        heatmap_data = []
        
        for i in range(grid_size):
            for j in range(grid_size):
                grid_south = south + i * lat_step
                grid_north = south + (i + 1) * lat_step
                grid_west = west + j * lon_step
                grid_east = west + (j + 1) * lon_step
                
                # Count entities in this grid cell
                count = sum(1 for entity in entities 
                           if (grid_south <= entity.latitude < grid_north and
                               grid_west <= entity.longitude < grid_east))
                
                if count > 0:
                    heatmap_data.append({
                        "latitude": (grid_south + grid_north) / 2,
                        "longitude": (grid_west + grid_east) / 2,
                        "intensity": count
                    })
        
        return {
            "bbox": bbox.dict(),
            "grid_size": grid_size,
            "heatmap_points": heatmap_data,
            "max_intensity": max((point["intensity"] for point in heatmap_data), default=0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Heatmap error: {str(e)}")
