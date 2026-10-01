import math
from typing import Dict, List, Tuple

class RiskEngine:
    """
    AI-Assisted Risk Engine for PahadRakshak.
    Calculates a normalized 0-100 risk score based on multi-factor weighted inputs:
    - Incident Severity (0-25)
    - Environmental/Rainfall factor (0-15)
    - Historical vulnerability factor (0-15)
    - Report Density & Proximity (0-15)
    - Affected Population (0-15)
    - Road Accessibility / Infrastructure Blockage (0-15)
    """

    SEVERITY_WEIGHTS = {
        "LOW": 10.0,
        "MODERATE": 15.0,
        "HIGH": 20.0,
        "CRITICAL": 25.0
    }

    TYPE_WEIGHTS = {
        "Landslide": 1.2,
        "Flood": 1.25,
        "Heavy Rainfall": 1.1,
        "Road Blockage": 1.15,
        "Infrastructure Damage": 1.0,
        "Stranded People": 1.3,
        "Accident": 1.0,
        "Other": 0.9
    }

    @classmethod
    def calculate_risk(
        cls,
        incident_type: str,
        severity: str,
        affected_people: int,
        road_blocked: bool,
        reports_count: int = 1,
        rainfall_mm: float = 45.0, # Simulated or retrieved rainfall signal
        historical_incident_count: int = 2,
        terrain_vulnerability: str = "HIGH"
    ) -> Tuple[float, str, List[str], Dict[str, float]]:

        # 1. Base Severity Factor (0-25)
        base_sev = cls.SEVERITY_WEIGHTS.get(severity.upper(), 15.0)
        type_mult = cls.TYPE_WEIGHTS.get(incident_type, 1.0)
        severity_score = min(25.0, base_sev * type_mult)

        # 2. Environmental / Rainfall Factor (0-15)
        # Heavy mountain rain in Uttarakhand (>50mm/hr) exponentially raises risk
        if rainfall_mm > 75:
            rainfall_score = 15.0
        elif rainfall_mm > 40:
            rainfall_score = 10.0
        elif rainfall_mm > 15:
            rainfall_score = 5.0
        else:
            rainfall_score = 2.0

        # 3. Historical Incident Factor (0-15)
        # Frequently affected zones (e.g. Badrinath highway, Joshimath)
        history_score = min(15.0, historical_incident_count * 4.0)

        # 4. Report Density Factor (0-15)
        # Higher citizen reports within the same area indicate panic or multi-point crisis
        density_score = min(15.0, reports_count * 3.5)

        # 5. Affected Population Factor (0-15)
        if affected_people >= 50:
            affected_score = 15.0
        elif affected_people >= 20:
            affected_score = 12.0
        elif affected_people >= 5:
            affected_score = 8.0
        else:
            affected_score = 3.0

        # 6. Road Accessibility & Terrain Factor (0-15)
        accessibility_score = 15.0 if road_blocked else 5.0

        # Total Raw Score (0 - 100)
        raw_score = (
            severity_score +
            rainfall_score +
            history_score +
            density_score +
            affected_score +
            accessibility_score
        )

        total_score = round(min(100.0, max(0.0, raw_score)), 1)

        # Determine Risk Level
        if total_score >= 76:
            level = "CRITICAL"
        elif total_score >= 51:
            level = "HIGH"
        elif total_score >= 26:
            level = "MODERATE"
        else:
            level = "LOW"

        # Generate Explainable AI Reasons
        reasons = []
        if severity.upper() in ["HIGH", "CRITICAL"]:
            reasons.append(f"High baseline severity tagged for {incident_type} incident.")
        if rainfall_mm >= 40:
            reasons.append(f"Heavy precipitation detected in zone ({rainfall_mm}mm precipitation signal).")
        if historical_incident_count >= 2:
            reasons.append(f"{historical_incident_count} historical incidents recorded in this high-risk zone.")
        if reports_count > 1:
            reasons.append(f"Multiple citizen reports ({reports_count} reports) verified in immediate radius.")
        if affected_people >= 5:
            reasons.append(f"High population impact: {affected_people} individuals reported at risk.")
        if road_blocked:
            reasons.append("Road blockage confirmed — emergency response access obstructed.")

        if not reasons:
            reasons.append("Standard incident report under routine observation.")

        breakdown = {
            "severity_factor": round(severity_score, 1),
            "rainfall_factor": round(rainfall_score, 1),
            "history_factor": round(history_score, 1),
            "density_factor": round(density_score, 1),
            "affected_factor": round(affected_score, 1),
            "accessibility_factor": round(accessibility_score, 1)
        }

        return total_score, level, reasons, breakdown
