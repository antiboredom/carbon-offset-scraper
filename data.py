from dataclasses import dataclass, asdict

@dataclass
class OffsetProject:
    """A normalized carbon offset project"""

    name: str = ""
    location: str = ""
    registry_id: str = ""
    registry_url: str = ""
    project_url: str = ""
    developer: str = ""
    project_type: str = ""
    description: str = ""
    methodology: str = ""
    total_credits: float = 0
    status: str = ""
    registry: str = ""


    dict = asdict
