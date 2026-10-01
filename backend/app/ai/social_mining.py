import re
from typing import Dict, Any, List

class SocialMediaMiningService:
    """
    Social Media Disaster & Emergency Intelligence Crawler.
    Extracts disaster and accident reports from X/Twitter, Instagram, and Facebook posts.
    """

    DISASTER_KEYWORDS = [
        "landslide", "flood", "cloudburst", "road blocked", "stranded",
        "rockfall", "heavy rain", "bridge damage", "accident", "truck",
        "graphic era", "dehradun", "chamoli", "helang", "joshimath", "rudraprayag"
    ]

    @classmethod
    def parse_social_post(cls, post_text: str, platform: str = "X (Twitter)", media_url: str = None) -> Dict[str, Any]:
        text_lower = post_text.lower()
        matched_keywords = [kw for kw in cls.DISASTER_KEYWORDS if kw in text_lower]

        # Extract location heuristics
        location = "Dehradun District Corridor"
        if "graphic era" in text_lower or "clement town" in text_lower:
            location = "Near Graphic Era University, Clement Town, Dehradun"
        elif "helang" in text_lower:
            location = "NH-07 Helang Stretch, Chamoli"
        elif "joshimath" in text_lower:
            location = "Joshimath Main Road, Chamoli"
        elif "rudraprayag" in text_lower:
            location = "Rudraprayag Sangam Bypass"
        elif "dehradun" in text_lower:
            location = "Rajpur Road / Sahastradhara, Dehradun"

        # Determine inferred category
        inc_type = "Accident"
        if "landslide" in text_lower or "rockfall" in text_lower:
            inc_type = "Landslide"
        elif "flood" in text_lower or "river" in text_lower:
            inc_type = "Flood"
        elif "stranded" in text_lower or "pilgrim" in text_lower:
            inc_type = "Stranded People"
        elif "rain" in text_lower or "cloudburst" in text_lower:
            inc_type = "Heavy Rainfall"
        elif "accident" in text_lower or "truck" in text_lower or "crash" in text_lower:
            inc_type = "Accident"

        is_disaster_alert = len(matched_keywords) >= 1

        return {
            "is_disaster_alert": is_disaster_alert,
            "platform": platform,
            "inferred_type": inc_type,
            "inferred_location": location,
            "matched_keywords": matched_keywords,
            "confidence_score": 90.0 if is_disaster_alert else 40.0,
            "original_post": post_text,
            "media_url": media_url,
            "summary": f"Social post on {platform} indicates {inc_type} at {location}."
        }
