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
        breakaway: bool = False
    ):
        self.race         = race
        self.year         = year
        self.stage_number = stage_number
        self.stage_type   = stage_type
        self.distance_km  = distance_km
        self.rider_name   = rider_name
        self.team         = team
        self.time         = time
        self.gap          = gap
        self.rank         = rank
        self.breakaway     = breakaway

    def __str__(self) -> str:
        """Useful for printing results in a readable format."""
        gap_str = self.gap if self.gap else "winner"
        return (
            f"[{self.race.upper()} {self.year} | Stage {self.stage_number}] "
            f"P{self.rank} - {self.rider_name} ({self.team}) "
            f"| {self.time} | Gap: {gap_str} | Breakaway: {self.breakaway}"
        )

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
        }