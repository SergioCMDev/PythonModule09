from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxigen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(min_length=0, max_length=200)


def show_station_data(station: SpaceStation) -> None:
    status: str = (
        "Operational" if station.is_operational else "not Operational"
    )
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxigen_level}%")
    print(f"Status: {status}")
    print()
    print("========================================")
    print("Expected validation error:")


def main() -> None:
    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxigen_level=92.3,
        last_maintenance=datetime.now(),
        is_operational=True,
        notes="Test station"
    )

    print("Space Station Data Validation")
    print("========================================")
    show_station_data(station)
    print("========================================")
    print("Expected validation error:")
    try:
        station = SpaceStation(
            station_id="2",
            name="International Space Station",
            crew_size=10,
            power_level=85.5,
            oxigen_level=92.3,
            last_maintenance=datetime.now(),
            is_operational=True,
            notes="Test station"
        )
    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
