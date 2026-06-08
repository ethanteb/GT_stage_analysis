class RiderStageResult:
    """Represents one rider's result for one stage of a Grand Tour."""

    def __init__(
        self,
        race: str,
        year: int,
        stage_number: int,
        stage_type: str,
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
    
    
class StageProfile:
    """Represents the profile of a stage, including type and distance."""
    def __init__(
            self,
            race: str,
            year: int,
            stage_number: int, 
            date: str, 
            start_time: str, 
            avg_speed_winner_kmh: float, 
            classification: str, 
            race_category: str, 
            distance_km: float, 
            gradient_final_km: float, 
            profile_score: int, 
            vertical_metres: int,
            departure_location: str,
            arrival_location: str,
            won_how: str,
            avg_temperature_c: float,
    ):
        self.race = race,
        self.year = year,
        self.stage_number = stage_number,
        self.date = date
        self.start_time = start_time
        self.avg_speed_winner_kmh = avg_speed_winner_kmh
        self.classification = classification
        self.race_category = race_category
        self.distance_km = distance_km
        self.gradient_final_km = gradient_final_km
        self.profile_score = profile_score
        self.vertical_metres = vertical_metres
        self.departure_location = departure_location
        self.arrival_location = arrival_location
        self.won_how = won_how
        self.avg_temperature_c = avg_temperature_c

    def __str__(self) -> str:
        """Useful for printing stage profile in a readable format."""
        return_string = f"[{self.race.upper()} {self.year} | Stage {self.stage_number}] "
        return_string += f"/n Date: {self.date} | Start Time: {self.start_time} | Distance: {self.distance_km}km | Avg. speed winner: {self.avg_speed_winner_kmh}km/h"
        return_string += f"/n Classification: {self.classification} | Race category: {self.race_category} | Gradient final km: {self.gradient_final_km}% | Profile score: {self.profile_score} | Vertical metres: {self.vertical_metres}m"
        return_string += f"/n Departure: {self.departure_location} | Arrival: {self.arrival_location} | Won how: {self.won_how} | Avg. temperature: {self.avg_temperature_c}°C"
        return (return_string)
    
    def to_dict(self) -> dict:
        """Convert to a dictionary, useful for CSV/JSON export."""
        return {
            "race":                 self.race,
            "year":                 self.year,
            "stage_number":         self.stage_number,
            "date":                 self.date,
            "start_time":           self.start_time,
            "avg_speed_winner_kmh": self.avg_speed_winner_kmh,
            "classification":       self.classification,
            "race_category":        self.race_category,
            "distance_km":          self.distance_km,
            "gradient_final_km":    self.gradient_final_km,
            "profile_score":        self.profile_score,
            "vertical_metres":      self.vertical_metres,
            "departure_location":   self.departure_location,
            "arrival_location":     self.arrival_location,
            "won_how":              self.won_how,
            "avg_temperature_c":    self.avg_temperature_c
        }