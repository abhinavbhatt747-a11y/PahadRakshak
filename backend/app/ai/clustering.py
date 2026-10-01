import math
from typing import List, Dict, Any

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates surface distance in kilometers between two lat/lng coordinates."""
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class ClusterDetector:
    """
    Identifies incident clusters across time and space.
    If multiple reports occur within 3.0 km radius in recent window, 
    flags as an Incident Cluster.
    """

    @classmethod
    def detect_clusters(cls, incidents: List[Dict[str, Any]], radius_km: float = 3.0) -> List[Dict[str, Any]]:
        clusters = []
        visited = set()

        for i, inc1 in enumerate(incidents):
            if inc1["id"] in visited:
                continue

            current_cluster = [inc1]
            visited.add(inc1["id"])

            for j, inc2 in enumerate(incidents):
                if i == j or inc2["id"] in visited:
                    continue

                dist = haversine_distance(
                    inc1["latitude"], inc1["longitude"],
                    inc2["latitude"], inc2["longitude"]
                )

                if dist <= radius_km:
                    current_cluster.append(inc2)
                    visited.add(inc2["id"])

            if len(current_cluster) >= 2:
                # Calculate cluster centroid
                avg_lat = sum(x["latitude"] for x in current_cluster) / len(current_cluster)
                avg_lng = sum(x["longitude"] for x in current_cluster) / len(current_cluster)
                highest_risk = max(x["risk_score"] for x in current_cluster)
                total_affected = sum(x["affected_people"] for x in current_cluster)

                clusters.append({
                    "cluster_id": f"CLS-UK-{len(clusters)+1:03d}",
                    "incidents_count": len(current_cluster),
                    "incidents": [x["incident_code"] for x in current_cluster],
                    "centroid_lat": round(avg_lat, 5),
                    "centroid_lng": round(avg_lng, 5),
                    "radius_km": radius_km,
                    "district": current_cluster[0].get("district", "Chamoli"),
                    "highest_risk_score": highest_risk,
                    "total_affected_people": total_affected,
                    "title": f"Incident Cluster: {current_cluster[0]['type']} Zone ({len(current_cluster)} linked reports)",
                    "summary": f"{len(current_cluster)} incidents reported within {radius_km}km radius affecting {total_affected} people."
                })

        return clusters
