# Geospatial features for InfoTerminal Graph API

from typing import Dict, List, Optional, Any, Tuple
from pydantic import BaseModel
import requests
import time
from utils.neo4j_client import neo_session


class BoundingBox(BaseModel):
    south: float
    west: float  
    north: float
    east: float


class GeocodeRequest(BaseModel):
    location: str
    country_code: Optional[str] = None


class GeoEntity(BaseModel):
    node_id: str
    name: str
    latitude: float
    longitude: float
    labels: List[str]


class GeospatialService:
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver
        self.geocoding_cache = {}
        
    def geocode_location(self, location: str, country_code: str = None) -> Optional[Dict[str, Any]]:
        """Geocode a location string using Nominatim API."""
        cache_key = f"{location}_{country_code or ''}"
        
        if cache_key in self.geocoding_cache:
            return self.geocoding_cache[cache_key]
        
        try:
            # Use OpenStreetMap Nominatim for geocoding
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": location,
                "format": "json",
                "limit": 1,
                "addressdetails": 1
            }
            
            if country_code:
                params["countrycodes"] = country_code
                
            headers = {
                "User-Agent": "InfoTerminal/1.0 (OSINT Platform)"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            results = response.json()
            if results:
                result = results[0]
                geo_data = {
                    "latitude": float(result["lat"]),
                    "longitude": float(result["lon"]),
                    "display_name": result.get("display_name"),
                    "address": result.get("address", {}),
                    "confidence": float(result.get("importance", 0.5))
                }
                
                # Cache the result
                self.geocoding_cache[cache_key] = geo_data
                return geo_data
                
        except Exception as e:
            print(f"Geocoding error for '{location}': {e}")
            
        return None
    
    def add_coordinates_to_node(self, node_id: str, latitude: float, longitude: float) -> bool:
        """Add coordinates to an existing node."""
        try:
            with neo_session(self.driver) as session:
                result = session.run("""
                MATCH (n {id: $node_id})
                SET n.latitude = $lat, n.longitude = $lon, n.has_coordinates = true
                RETURN n
                """, node_id=node_id, lat=latitude, lon=longitude)
                
                return result.single() is not None
        except Exception as e:
            print(f"Error adding coordinates to node {node_id}: {e}")
            return False
    
    def geocode_and_update_node(self, node_id: str, location_field: str = "name") -> Dict[str, Any]:
        """Geocode a node based on its location field and update with coordinates."""
        try:
            with neo_session(self.driver) as session:
                # Get the node's location data
                result = session.run(f"""
                MATCH (n {{id: $node_id}})
                RETURN n.{location_field} as location, n
                """, node_id=node_id).single()
                
                if not result:
                    return {"success": False, "error": "Node not found"}
                
                location = result["location"]
                if not location:
                    return {"success": False, "error": f"No {location_field} found"}
                
                # Geocode the location
                geo_data = self.geocode_location(location)
                if not geo_data:
                    return {"success": False, "error": "Geocoding failed"}
                
                # Update node with coordinates
                session.run("""
                MATCH (n {id: $node_id})
                SET n.latitude = $lat, 
                    n.longitude = $lon,
                    n.has_coordinates = true,
                    n.geocoded_address = $address,
                    n.geocoding_confidence = $confidence
                """, 
                node_id=node_id, 
                lat=geo_data["latitude"], 
                lon=geo_data["longitude"],
                address=geo_data.get("display_name"),
                confidence=geo_data.get("confidence")
                )
                
                return {
                    "success": True,
                    "coordinates": {
                        "latitude": geo_data["latitude"],
                        "longitude": geo_data["longitude"]
                    },
                    "address": geo_data.get("display_name"),
                    "confidence": geo_data.get("confidence")
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_entities_by_bbox(self, bbox: BoundingBox, limit: int = 100) -> List[GeoEntity]:
        """Get entities within a bounding box."""
        try:
            with neo_session(self.driver) as session:
                result = session.run("""
                MATCH (n)
                WHERE n.has_coordinates = true
                  AND n.latitude >= $south AND n.latitude <= $north
                  AND n.longitude >= $west AND n.longitude <= $east
                RETURN n.id as node_id, n.name as name, 
                       n.latitude as latitude, n.longitude as longitude,
                       labels(n) as labels
                LIMIT $limit
                """, 
                south=bbox.south, north=bbox.north, 
                west=bbox.west, east=bbox.east, limit=limit)
                
                entities = []
                for record in result:
                    entities.append(GeoEntity(
                        node_id=record["node_id"],
                        name=record["name"] or "Unknown",
                        latitude=record["latitude"],
                        longitude=record["longitude"],
                        labels=record["labels"] or []
                    ))
                
                return entities
        except Exception as e:
            print(f"Error getting entities by bbox: {e}")
            return []
    
    def get_entities_near_point(self, latitude: float, longitude: float, 
                               radius_km: float = 10.0, limit: int = 50) -> List[GeoEntity]:
        """Get entities near a point within a radius (using Haversine distance approximation)."""
        try:
            with neo_session(self.driver) as session:
                # Simple approximation using lat/lon degree differences
                # 1 degree latitude ≈ 111 km
                # 1 degree longitude ≈ 111 km * cos(latitude)
                import math
                lat_range = radius_km / 111.0
                lon_range = radius_km / (111.0 * math.cos(math.radians(latitude)))
                
                result = session.run("""
                MATCH (n)
                WHERE n.has_coordinates = true
                  AND n.latitude >= $lat_min AND n.latitude <= $lat_max
                  AND n.longitude >= $lon_min AND n.longitude <= $lon_max
                WITH n, 
                     2 * 6371 * asin(sqrt(
                         haversin(radians($lat - n.latitude)) + 
                         cos(radians($lat)) * cos(radians(n.latitude)) * 
                         haversin(radians($lon - n.longitude))
                     )) as distance_km
                WHERE distance_km <= $radius
                RETURN n.id as node_id, n.name as name,
                       n.latitude as latitude, n.longitude as longitude,
                       labels(n) as labels, distance_km
                ORDER BY distance_km
                LIMIT $limit
                """,
                lat=latitude, lon=longitude,
                lat_min=latitude-lat_range, lat_max=latitude+lat_range,
                lon_min=longitude-lon_range, lon_max=longitude+lon_range,
                radius=radius_km, limit=limit)
                
                entities = []
                for record in result:
                    entity = GeoEntity(
                        node_id=record["node_id"],
                        name=record["name"] or "Unknown",
                        latitude=record["latitude"],
                        longitude=record["longitude"],
                        labels=record["labels"] or []
                    )
                    entity.distance_km = record["distance_km"]
                    entities.append(entity)
                
                return entities
        except Exception as e:
            print(f"Error getting entities near point: {e}")
            return []
    
    def get_geo_statistics(self) -> Dict[str, Any]:
        """Get statistics about geocoded entities."""
        try:
            with neo_session(self.driver) as session:
                result = session.run("""
                MATCH (n)
                WITH count(n) as total_nodes,
                     count(CASE WHEN n.has_coordinates THEN 1 END) as geocoded_nodes
                RETURN total_nodes, geocoded_nodes,
                       (geocoded_nodes * 100.0 / total_nodes) as geocoding_percentage
                """).single()
                
                # Get node types with coordinates
                node_types = session.run("""
                MATCH (n)
                WHERE n.has_coordinates = true
                UNWIND labels(n) as label
                RETURN label, count(*) as count
                ORDER BY count DESC
                """)
                
                # Get geographic distribution
                geographic_spread = session.run("""
                MATCH (n)
                WHERE n.has_coordinates = true
                RETURN min(n.latitude) as min_lat, max(n.latitude) as max_lat,
                       min(n.longitude) as min_lon, max(n.longitude) as max_lon,
                       avg(n.latitude) as center_lat, avg(n.longitude) as center_lon
                """).single()
                
                return {
                    "total_nodes": result["total_nodes"],
                    "geocoded_nodes": result["geocoded_nodes"], 
                    "geocoding_percentage": round(result["geocoding_percentage"] or 0, 2),
                    "node_types_with_coordinates": [
                        {"type": record["label"], "count": record["count"]}
                        for record in node_types
                    ],
                    "geographic_bounds": {
                        "min_latitude": geographic_spread["min_lat"],
                        "max_latitude": geographic_spread["max_lat"],
                        "min_longitude": geographic_spread["min_lon"],
                        "max_longitude": geographic_spread["max_lon"],
                        "center_latitude": geographic_spread["center_lat"],
                        "center_longitude": geographic_spread["center_lon"]
                    } if geographic_spread else None
                }
        except Exception as e:
            print(f"Error getting geo statistics: {e}")
            return {"error": str(e)}
    
    def batch_geocode_nodes(self, node_type: str = None, 
                           location_field: str = "name", 
                           limit: int = 100) -> Dict[str, Any]:
        """Batch geocode nodes that don't have coordinates yet."""
        try:
            with neo_session(self.driver) as session:
                # Find nodes without coordinates
                type_filter = f"WHERE '{node_type}' IN labels(n) AND" if node_type else "WHERE"
                
                result = session.run(f"""
                MATCH (n)
                {type_filter} n.has_coordinates IS NULL 
                  AND n.{location_field} IS NOT NULL
                RETURN n.id as node_id, n.{location_field} as location
                LIMIT $limit
                """, limit=limit)
                
                processed = 0
                successful = 0
                failed = 0
                
                for record in result:
                    node_id = record["node_id"]
                    location = record["location"]
                    
                    # Rate limit to be nice to Nominatim
                    time.sleep(1.1)  # Max 1 request per second
                    
                    result = self.geocode_and_update_node(node_id, location_field)
                    processed += 1
                    
                    if result.get("success"):
                        successful += 1
                    else:
                        failed += 1
                        
                    print(f"Processed {processed}: {location} -> {'✓' if result.get('success') else '✗'}")
                
                return {
                    "processed": processed,
                    "successful": successful,
                    "failed": failed,
                    "success_rate": (successful / processed * 100) if processed > 0 else 0
                }
                
        except Exception as e:
            return {"error": str(e)}
