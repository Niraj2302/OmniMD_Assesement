from pydantic import BaseModel

class EventPayload(BaseModel):
    prospect_id: str
    event_trigger: str