from datetime import datetime
from typing import Optional
from pydantic import (
    BaseModel, Field, ValidationError, model_validator)
from enum import Enum


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telephatic = "telephatic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=3, max_length=10)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(min_length=0, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_model_rules(self):
        if (not self.contact_id.startswith("AC")):
            raise ValueError("contact_id must begin with AC")
        if (self.contact_type is ContactType.physical
                and not self.is_verified):
            raise ValueError("contact_type must ser verified")

        if (self.contact_type == ContactType.telephatic
                and self.witness_count < 3):
            raise ValueError("Telepathic contact requires at least 3 "
                             "witnesses")

        if (self.signal_strength > 7.0 and len(self.message_received) < 1):
            raise ValueError("strong signal_strength requires to "
                             "include a message")

        return self


def show_info(alien_contact: AlienContact) -> None:
    print(f"ID: {alien_contact.contact_id}")
    print(f"Type: {alien_contact.contact_type}")
    print(f"Location: {alien_contact.location}")
    print(f"Signal: {alien_contact.signal_strength}/10")
    print(f"Duration: {alien_contact.duration_minutes} minutes")
    print(f"Witnesses: {alien_contact.witness_count}")
    print(f"Message: '{alien_contact.message_received}'")


def main() -> None:

    try:
        alien_contact = AlienContact(
            contact_id="AC1",
            timestamp=datetime.now(),
            location="here",
            contact_type=ContactType.physical,
            signal_strength=2,
            duration_minutes=32,
            witness_count=23,
            message_received="F",
            is_verified=True
        )
    except ValidationError as e:
        print(e)
        return

    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    show_info(alien_contact)
    print()
    print("======================================")
    print("Expected validation error:")
    try:
        alien_contact = AlienContact(
            contact_id="AC1",
            timestamp=datetime.now(),
            location="here",
            contact_type=ContactType.physical,
            signal_strength=2,
            duration_minutes=32,
            witness_count=23,
            message_received="F",
            is_verified=True
        )
    except ValidationError as e:
        print(e)
        return


if __name__ == "__main__":
    main()
