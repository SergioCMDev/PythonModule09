from datetime import datetime
from pydantic import (
    BaseModel, Field, ValidationError, model_validator)
from enum import Enum


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_model_rules(self):
        if (not self.mission_name.startswith("M")):
            raise ValueError("Mision name must start with M")
        any_commander_or_captian = any(crew_member.rank is Rank.captain
                                       or crew_member.rank is Rank.commander
                                       for crew_member in self.crew)
        if (not any_commander_or_captian):
            raise ValueError("Crew Member must have one Commander or Captian")
        experienced_crew: list[CrewMember] = [
           crew_member for crew_member in self.crew
           if crew_member.years_experience >= 5]
        if (self.duration_days > 365
                and not (len(experienced_crew) >= len(self.crew)/2)):
            raise ValueError("Long missions need 50% "
                             "experienced crew (5+ years)")
        any_inactive = any(not crew_member.is_active
                           for crew_member in self.crew)
        if (any_inactive):
            raise ValueError("All crew members must be active")

        return self


def show_info(mission: SpaceMission) -> None:
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: {mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members: ")
    for crew in mission.crew:
        print(f"- {crew.name} ({crew.rank}) - {crew.specialization}")


def main() -> None:
    sarah_connor = CrewMember(
        member_id="AGCGF",
        name="Sarah Connor",
        rank=Rank.commander,
        age=59,
        specialization="Alien killing",
        years_experience=2,
        is_active=True
    )
    neo = CrewMember(
        member_id="NEO",
        name="Neo",
        rank=Rank.cadet,
        age=25,
        specialization="Bullet dogder",
        years_experience=2,
        is_active=True
    )

    mission = SpaceMission(
        mission_id="K1LL_31",
        mission_name="M_Alienean",
        destination="Alien nest",
        launch_date=datetime.now(),
        duration_days=300,
        crew=[sarah_connor, neo],
        mission_status="planned",
        budget_millions=4000
    )
    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    show_info(mission)
    print()
    print("=========================================")
    try:
        smith = CrewMember(
            member_id="AGCGF",
            name="smith",
            rank=Rank.lieutenant,
            age=59,
            specialization="Alien killing",
            years_experience=5,
            is_active=True
        )
        terminator = CrewMember(
            member_id="terminator",
            name="terminator",
            rank=Rank.lieutenant,
            age=25,
            specialization="Bullet dogder",
            years_experience=10,
            is_active=True
        )
        terminator2 = CrewMember(
            member_id="terminator",
            name="terminator",
            rank=Rank.commander,
            age=50,
            specialization="coming back",
            years_experience=2,
            is_active=False
        )
    except ValidationError as e:
        print(e)
        return

    print("Expected validation error:")
    try:
        mission2 = SpaceMission(
            mission_id="K1LL_31",
            mission_name="M_Alienean",
            destination="Alien nest",
            launch_date=datetime.now(),
            duration_days=400,
            crew=[smith, terminator, terminator2],
            mission_status="planned",
            budget_millions=40
        )
        show_info(mission2)
    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
