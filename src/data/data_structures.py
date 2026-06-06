class RiderStageResult:
    """Represents one rider's result for one stage of a Grand Tour."""

    def __init__(
        self,
        race: str,
        year: int,
        stage_number: int,
        stage_type: str,
        distance_km: float,
        rider_name: str,
        team: str,
        time: str,
        gap: str | None,
        rank: int, 
        breakaway: bool = False, 
        breakaway_distance: float = 0.0
    ):
        self.race               = race
        self.year               = year
        self.stage_number       = stage_number
        self.stage_type         = stage_type
        self.distance_km        = distance_km
        self.rider_name         = rider_name
        self.team               = team
        self.time               = time
        self.gap                = gap
        self.rank               = rank
        self.breakaway          = breakaway
        self.breakaway_distance = breakaway_distance

    def __str__(self) -> str:
        """Useful for printing results in a readable format."""
        gap_str = self.gap if self.gap else "winner"
        return_string = f"[{self.race.upper()} {self.year} | Stage {self.stage_number}] "
        return_string += f"P{self.rank} - {self.rider_name} ({self.team}) "
        return_string += f"| {self.time} | GC Gap: {gap_str}"
        if self.breakaway:
            return_string += f" | Distance in break: {self.breakaway_distance}km"
        return (return_string)

    def to_dict(self) -> dict:
        """Convert to a dictionary, useful for CSV/JSON export."""
        return {
            "race":         self.race,
            "year":         self.year,
            "stage_number": self.stage_number,
            "stage_type":   self.stage_type,
            "distance_km":  self.distance_km,
            "rider_name":   self.rider_name,
            "team":         self.team,
            "time":         self.time,
            "gap":          self.gap,
            "rank":         self.rank,
            "breakaway":     self.breakaway,
            "breakaway_distance": self.breakaway_distance
        }