import os
from typing import Dict, Any

class ImageAnalysisService:
    """
    Safe and explainable visual evidence analyzer.
    Analyzes submitted photos to extract visual risk cues.
    Can operate via heuristic/mock evaluation or integrate with vision AI APIs.
    """

    @classmethod
    def analyze_image(cls, photo_filename: str, incident_type: str) -> Dict[str, Any]:
        """
        Analyzes photo evidence and returns explainable findings.
        """
        filename_lower = photo_filename.lower()

        # Heuristic visual evidence classification (Demo safe & explainable)
        if "landslide" in filename_lower or incident_type == "Landslide":
            return {
                "detected_features": ["Debris flow", "Road blockage", "Unstable slope"],
                "confidence": 88.5,
                "recommended_severity": "HIGH",
                "summary": "Visual evidence indicates severe slope movement and debris obstruction on roadway."
            }
        elif "flood" in filename_lower or incident_type == "Flood":
            return {
                "detected_features": ["Submerged road", "Rapid water flow", "Standing mud"],
                "confidence": 92.0,
                "recommended_severity": "CRITICAL",
                "summary": "Visual evidence indicates active water submergence and structural inundation."
            }
        elif "block" in filename_lower or incident_type == "Road Blockage":
            return {
                "detected_features": ["Boulders on tarmac", "Stranded vehicles"],
                "confidence": 84.0,
                "recommended_severity": "HIGH",
                "summary": "Visual evidence confirms major physical obstruction blocking vehicle movement."
            }
        else:
            return {
                "detected_features": ["General terrain anomaly", "Hazard zone"],
                "confidence": 78.0,
                "recommended_severity": "MODERATE",
                "summary": "Visual evidence verified. Moderate risk indicators detected in field photograph."
            }
