"""
API wrapper for 4mir.ir fortune/poetry data.
"""
import logging
from dataclasses import dataclass
from typing import Optional
import requests

log = logging.getLogger("fal_api")

API_URL = "https://4mir.ir/fall/api.php"
TIMEOUT = 12


@dataclass
class FalData:
    number: str
    ghazal: str
    tabir: str
    image_url: str
    voice_url: str
    link: str


def fetch() -> Optional[FalData]:
    try:
        resp = requests.get(API_URL, timeout=TIMEOUT)
        if resp.status_code != 200:
            log.error("HTTP %d from API", resp.status_code)
            return None

        data = resp.json()
        if data.get("status") != 200:
            log.warning("API status not 200: %s", data.get("status"))
            return None

        result = data.get("result", {})
        return FalData(
            number=result.get("number", "—"),
            ghazal=result.get("ghazal", ""),
            tabir=result.get("tabir", ""),
            image_url=result.get("image", ""),
            voice_url=result.get("voice", ""),
            link=result.get("link", ""),
        )
    except Exception as e:
        log.error("fetch error: %s", e)
        return None
